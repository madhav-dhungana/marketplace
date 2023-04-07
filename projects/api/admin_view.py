
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from mainproject.pagination import CustomPagination
from projects.models import *
from .serializers import *
from rest_framework import viewsets, filters
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from user.models import User,IdentityForm
from rest_framework.status import HTTP_201_CREATED
from user.api.permissions import RequestUserOrAdminEdit,IsBatuwaAdminOnly
from django_filters.rest_framework import DjangoFilterBackend



class AnswerIdentiyRequest(APIView):
    permission_classes=[IsBatuwaAdminOnly]
    def post(self, request):
        data=request.data
        form_id = data.get("form_id")
        user_id = data.get("user_id")
        form = get_object_or_404(IdentityForm,id=form_id)
        user = get_object_or_404(User,id=user_id)
        accept = data.get("accept")
        status = "accepted" if accept=="true" else "rejected"
        if accept == "true":
            form.accept_or_reject_user(True)
        else:
            form.accept_or_reject_user(False)
    
        msg = f"Successfully Verified  {user}" if accept == "true" else f"Successfully Rejected {user}" 
        return Response({"status":status,"id":form_id,"msg":msg})


class ApproveProject(APIView):
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        project.status = "Active"
        project.save()
        project.notify.create(
            # action_by=project.posted_by,
            action_to=project.posted_by,
            action="approved",
            title=f"Your project {project_id} has been approved.",
        )
        return Response(
            {
                "change_status": True,
                "id": project_id,
                "msg": f"Project {project_id} was successfully approved",
            }
        )