from datetime import timedelta
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from mainproject.pagination import CustomPagination
from projects.models import *
from .serializers import *
from rest_framework import viewsets, filters,status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from user.models import User
from rest_framework.status import HTTP_201_CREATED
from user.api.permissions import RequestUserOrAdminEdit,InviteUserOrAdminPerm,OwnerOrAdminEdit
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from rest_framework.permissions import  IsAuthenticated



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = ("status", "title")
    permission_classes=[OwnerOrAdminEdit]
    pagination_class = CustomPagination
    

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)
    
    def get_queryset(self,*args, **kwargs):
        queryset = super().get_queryset()
        if self.request.user.role == "Admin":
            return queryset
        elif self.request.user.role == "Employer":
            return queryset.filter(posted_by=self.request.user)
        else:
            queryset = queryset.filter(hired=self.request.user)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"Deleted":True},status=status.HTTP_200_OK)
   

class OverallProjectInfo(APIView):
    def get(self,request):
        projects=Project.objects.all()
        if request.user.role == "Employer":
            projects = request.user.my_projects.all()
        if request.user.role == "Freelancer":
            projects = request.user.hired_projects.all()
        
        on_count = projects.filter(status="ON").count()
        can_count = projects.filter(status="CAN").count()
        com_count = projects.filter(status="COM").count()
        pen_count = projects.filter(status="PEN").count()

        info ={
            "total":projects.count(),
            "ongoing":on_count,
            "cancelled":can_count,
            "completed":com_count,
           
        }
        if request.user.role != "Freelancer":
            info["pending"] =pen_count
            info["active"] = projects.filter(status="Active").count()

        return Response(info)


class CategoryViewset(viewsets.ModelViewSet):
    queryset = ProjectCategory.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend,)
    search_fields = ("name",)


class GetAllReviews(ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        return Reviews.objects.all()


class ReviewDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    lookup_url_kwarg = "id"
    lookup_field = "id"
    permission_classes = [RequestUserOrAdminEdit]

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(
            {
                "deleted": True,
                "id": kwargs.get("id"),
                "msg": "Successfully Deleted Review",
            }
        )


class ReviewGotApi(ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination

    def get_queryset(self, request, *args, **kwargs):
        return request.user.reviews_got.all()


class ReviewGivenApi(ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination

    def get_queryset(self, request, *args, **kwargs):
        return request.user.reviews_given.all()


class CreateReview(APIView):
    def post(self, request):
        data = request.data
        review = data.get("review")
        rating = data.get("rating")
        project_id = data.get("project_id")
        project = get_object_or_404(Project, id=project_id)
        review_to = data.get("username")
        review_to_user = get_object_or_404(User, username=review_to)

        r = Reviews.objects.create(
            review_by=request.user,
            review_to=review_to_user,
            review=review,
            rating=rating,
            for_project=project,
        )
        serializer = ReviewSerializer(r)
        return Response(serializer.data)

class InviteViewSet(viewsets.GenericViewSet):
    queryset = InviteModel.objects.all()
    serializer_class = InviteSerializer
    pagination_class = CustomPagination
    permission_classes=[InviteUserOrAdminPerm]
    # filter_backends = (DjangoFilterBackend,)
    # search_fields = ("name",)

    def list(self,*args, **kwargs):
        queryset = super().get_queryset()
        if self.request.user.role == "Freelancer":
            queryset = queryset.filter(sent_to=self.request.user)
        else:
            queryset = queryset.filter(sent_by=self.request.user)
        serializer = InviteSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sent_to = get_object_or_404(User,id=serializer.validated_data.get("sent_to_id"))
        project = get_object_or_404(Project,id=serializer.validated_data.get("project_id"))
        serializer.save(sent_by=user,sent_to=sent_to,project=project)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        
    
    def update(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data,instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    def delete(self,request,*args, **kwargs):
        self.get_object().delete()
        return Response({'Deleted':True})
    
   


class ChangeProjectStatus(APIView):
    only_role="Employer"
    permission_classes=[OwnerOrAdminEdit]
    
    @transaction.atomic
    def post(self,request,id):
        status = request.data.get('status')
        project = get_object_or_404(Project,id=id)
        self.check_object_permissions(request, project)
        project.status =status
        project.save()
        status_ =project.get_status_display()
        project.notify.create(
            action_by=project.posted_by,
            action_to=project.hired,
            action="changed status",
            title=f"{project.posted_by} changed the status of project {project.id} to {status_}.",
        )
        return Response({"msg":f'Successfully Changed Status to {status_}',"status":status_})    


class CheckMyAvailability(APIView):
    """
        View to check whether logged in user can apply or create proposal on project
    """
    permission_classes=[IsAuthenticated]
    
    def post(self,request):
        ids =request.data.get("id")
        if not request.user.availability:
            return Response({"can_apply":False,"reason":"Availability is turned off."})
        project = get_object_or_404(Project,id=ids)

        start_date = project.start_date
        end_date = project.end_date
        start_time = project.start_time
        end_time = project.end_time
        delta = end_date - start_date 
        not_available=[]
        for i in range(6):
            # no need to go further if all week days is checked

            gg = start_date + timedelta(days=i)
            day =gg.strftime("%A")
            obj = request.user.weekdayavailable_set.get(name=day)
            if obj.available_from and obj.available_to:
                ss = obj.available_from <= start_time <= obj.available_to
                ee = obj.available_from <= end_time <= obj.available_to
                if not (ss and ee):
                    not_available.append({
                        "day":obj.name,
                        "date":gg,
                        "project_time":f'{start_time} {end_time}',
                        "my_time":f'{obj.available_from} {obj.available_to}',
                    })

        if len(not_available):
            return Response({"can_apply":False,"reason":not_available})
        return Response({"can_apply":True})
        

class AnswerInviteAPI(APIView):
    # permission_classes=[InviteUserOrAdminPerm]

    def post(self, request):
        invite_model = get_object_or_404(InviteModel, id=request.POST.get("u_id"))
        if invite_model.sent_to ==request.user or request.user.role == "Admin":
            if invite_model.project.hired:
                invite_model.answered=True
                invite_model.save()
                return Response({
                    "id":invite_model.id,
                    "msg":"Sorry !This project hired someone else !"
                })
            accepted = None
            data = request.data
            if data.get("accept_invite") == "true":
                accepted = True
            else:
                accepted = False
            invite_model.answer_invite(accepted, request.user)
            accept_status = "accepted" if accepted else "declined"
            return Response(
                {
                    "id": invite_model.id,
                    "status":accept_status,
                    "accepted": accepted,
                    "msg": f"Successfully {accept_status} the invite by {invite_model.sent_by}",
                }
            )
        else:
            return Response({
                "detail":"You are not invited for this project !"
            },status=status.HTTP_400_BAD_REQUEST)
