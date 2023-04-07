from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages, auth
from user.api.mixins import SendEmailMixin
from user.models import User
from .utils import firstError, give_or_create_skills
from .forms import InviteForm, ProjectForm
from .models import (
    DesiredExpertise,
    HiredModel,
    InviteModel,
    Project,
    ProjectDocument,
    Reviews,
)
from user.mixins import AccessMixinView, BaseViewMixin
from django.views.generic import ListView


class CreateProject(AccessMixinView):
    only_role = "Employer"
    template_name = "projects/create_project.html"

    def get(self, request):
        print('-------------')
        form = ProjectForm()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            files = request.FILES.getlist("project_files")
            print("files are ", files)
            f = form.save(commit=False)
            f.posted_by = request.user
            skills = request.POST.getlist("desired_skills")
            f.save()
            f.desired_skills.set(give_or_create_skills("".join(skills)))
            if files:
                ProjectDocument.objects.bulk_create(
                    [ProjectDocument(project=f, documents=i) for i in files]
                )
            messages.success(request, f"Project was successfully created !")
            # return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            return redirect('project_payment',id=f.id)

        print(form.errors)
        skills = request.POST.getlist("desired_skills")
        context = {"form": form, 'skills':skills}
        return render(request, self.template_name, context)


class EditProject(AccessMixinView):
    only_role = "Employer"

    def get(self, request, id):
        project = get_object_or_404(Project, id=id)
        form = ProjectForm(instance=project)
        context = {"project": project, "form": form}
        return render(request, "projects/employer/edit_project.html", context)

    def post(self, request, id):
        project = get_object_or_404(Project, id=id)
        form = ProjectForm(request.POST, instance=project)
        skills = request.POST.getlist("desired_skills")
        files = request.FILES.getlist("project_files")

        if form.is_valid():
            if project.posted_by == request.user:
                f = form.save()
                f.desired_skills.set(give_or_create_skills("".join(skills)))
                for i in files:
                    ProjectDocument.objects.create(project=f, documents=i)
                messages.success(request, f"Successfully updated project !")
        else:
            messages.error(request, "Invalid data Added !")
        context = {"project": project, "form": form}
        return render(request, "projects/employer/edit_project.html", context)


project_type_map = {
    "all": "all",
    "ongoing": "ON",
    "completed": "COM",
    "cancelled": "CAN",
    "pending": "PEN",
}


class AllProjects(ListView, AccessMixinView):
    template_name = "projects/employer/projects.html"
    paginate_by = 5
    context_object_name = "project_list"
    only_role = "Employer"
    

    def get_queryset(self, *args, **kwargs):
        type = self.kwargs["project_type"]
        has_type = project_type_map.get(type)
        if not has_type:
            raise Http404
        if type.lower() == "all":
            return self.request.user.my_projects.all()
        else:
            return self.request.user.my_projects.filter(
                status=project_type_map.get(type)
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = self.kwargs.get("project_type")
        return context


class ProjectDetail(AccessMixinView):
    only_role = "Employer"

    def get(self, request, id):
        project = get_object_or_404(request.user.my_projects.all(), id=id)
        project_proposals = project.proposals.all()
        my_review = request.user.reviews_given.filter(for_project=project)
        has_reviewed = my_review.exists()
        context = {
            "project": project,
            "project_proposals": project_proposals,
            "my_review": my_review.first(),
            "has_reviewed": has_reviewed,
        }
        return render(request, "projects/employer/project_detail.html", context)

    def post(self, request, id):
        project = get_object_or_404(Project, id=id)
        if "hire" in request.POST:
            to_hire = get_object_or_404(User, id=request.POST.get("hire_user"))
            HiredModel.objects.create(
                project=project, hired_by=request.user, got_hired=to_hire
            )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class CompletedProjects(AccessMixinView):
    only_role = "Employer"

    def get(self, request):
        project_list = request.user.my_projects.filter(status="COM")
        context = {"project_list": project_list}
        return render(request, "projects/employer/completed_projects.html", context)


class OngoingProjects(AccessMixinView):
    only_role = "Employer"

    def get(self, request):
        project_list = request.user.my_projects.filter(status="ON")
        context = {"project_list": project_list}
        return render(request, "projects/employer/ongoing_projects.html", context)


class PendingProjects(AccessMixinView):
    only_role = "Employer"

    def get(self, request):
        project_list = request.user.my_projects.filter(status="PEN")
        context = {"project_list": project_list}
        return render(request, "projects/employer/pending_projects.html", context)


class CancelledProjects(AccessMixinView):
    only_role = "Employer"

    def get(self, request):
        project_list = request.user.my_projects.filter(status="CAN")
        context = {"project_list": project_list}
        return render(request, "projects/employer/cancelled_projects.html", context)


class AddReviewForProject(AccessMixinView):
    only_role = "Employer"

    def post(self, request, id):
        rating = request.POST.get("rating_val")
        review = request.POST.get("review")
        project = get_object_or_404(Project, id=id)
        my_review = Reviews.objects.create(
            review_by=request.user,
            review_to=project.hired,
            for_project=project,
            review=review,
            rating=int(rating),
        )
        return render(request, "projects/htmx/review.html", {"my_review": my_review})


class CreateInvite(AccessMixinView, SendEmailMixin):
    only_role = "Employer"
    email_template_name = "email/generic_email.html"
    mail_subject = "Invited on a project"

    def post(self, request):
        form = InviteForm(request.POST, user=request.user)
        if form.is_valid():
            f = form.save(commit=False)
            u_id = request.POST.get("u_id")
            sent_to = get_object_or_404(User, id=u_id)
            project = form.cleaned_data["project"]
            if InviteModel.objects.filter(
                sent_to=sent_to, sent_by=request.user, project=project
            ).exists():
                messages.error(
                    request, f"You have already invited {sent_to} for this project !"
                )
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

            f.sent_to = sent_to
            f.sent_by = request.user
            f.save()
            domain = request.META["HTTP_HOST"]
            email_data = {
                "site_name": "Batuwa",
                "for_user": sent_to.display_name,
                "message": f"You were invited by {request.user} for a project .",
            }
            self.send_email_temp(email_data, form.cleaned_data.get("email"))
            messages.success(request, f"{sent_to} was successfully invited !")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            # return JsonResponse({"Sent":True,"msg":f"Successfully invited {sent_to} for your project"})
        else:
            messages.error(request, f"{form.errors}")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


from user.mixins import AdminOnlyView

class SkillPage(AdminOnlyView):
    def get(self, request):
        skills = DesiredExpertise.objects.all()
        context = {"page_obj": skills}
        return render(request, "projects/skills.html", context)


from rest_framework import status,viewsets
from rest_framework.response import Response
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from mainproject.pagination import CustomPagination
from user.api.permissions import IsBatuwaAdminOnly

class FeeViewset(viewsets.ModelViewSet):
    queryset = DesiredExpertise.objects.all()
    serializer_class = SkillsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    permission_classes  =[IsBatuwaAdminOnly]
    search_fields = ("skill_name",)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        pk = instance.id
        self.perform_destroy(instance)
        return Response( {'type':'delete','id':pk}, status=status.HTTP_200_OK)



class ReviewApprove(AccessMixinView):
    only_role = "Admin"

    def get(self, request, id):
        review = get_object_or_404(Reviews, id=id)
        review.is_approved = True
        review.save()
        return redirect('dashboard')

class ReviewTrash(AccessMixinView):
    only_role = "Admin"

    def get(self, request, id):
        is_restore = request.GET.get('restore')
        if is_restore:
            review = get_object_or_404(Reviews, id=id)
            review.is_trash = False
        else:
            review = get_object_or_404(Reviews, id=id)
            review.is_trash = True
        review.save()
        return redirect('dashboard')