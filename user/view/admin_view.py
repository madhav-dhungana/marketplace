import re
from django.http import (
    Http404,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from projects.utils import firstError
from user.filters import IdentiyFormFilter
from projects.models import ProjectDocument, Reviews
from projects.utils import give_or_create_skills
from projects.forms import ProjectForm
from user.forms import CustomUserCreationForm
from projects.filters import ProjectFilter, UserFilter, ReviewFilter
from user.mixins import AccessMixinView
from projects.models import ProjectCategory
from projects.models import Project
from user.models import User, IdentityForm
from user.mixins import BaseViewMixin, PaginateView
from django.contrib import messages
from django.core.paginator import Paginator
from ..forms import AdminUserChangeForm, GroupForm
from django.contrib.auth.models import Group, Permission
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny


class Dashboard(AccessMixinView, BaseViewMixin):
    only_role = "Admin"

    def get(self, request):
        user_count = User.objects.count()
        projects = Project.objects.all()
        on_projects = Project.objects.filter(status="ON")
        on_projects_count = on_projects.count()
        comp_projects = Project.objects.filter(status="COM")
        comp_projects_count = comp_projects.count()
        pen_count = projects.filter(status="PEN").count()
        can_count = projects.filter(status="CAN").count()
        pending_projects = projects.filter(status="PEN")[:10]
        recent_users = User.objects.values(
            'id', 'email', 'role', 'display_name').order_by("-id")[:8]
        active = projects.filter(status="Active").count()

        chart_data = [active, pen_count, on_projects_count,
                      comp_projects_count, can_count]
        chart_label = ["Active", "Pending",
                       "Ongoing", "Completed", "Cancelled"]

        a = Reviews.objects.all()
        reviews = a.filter(is_trash=False)
        active_reviews = a.filter(is_approved=True, is_trash=False)
        pending_reviews = a.filter(is_approved=False, is_trash=False)
        trash_reviews = a.filter(is_trash=True)

        context = {
            "on_projects": on_projects,
            "recent_users": recent_users,
            "user_count": user_count,
            "pending_projects": pending_projects,
            "on_projects_count": on_projects_count,
            "comp_projects_count": comp_projects_count,
            "chart_data": chart_data,
            "chart_label": chart_label,
            "reviews": reviews,
            "active_reviews": active_reviews,
            "pending_reviews": pending_reviews,
            "trash_reviews": trash_reviews,
            "all_review_count": reviews.count(),
            "active_reviews_count": active_reviews.count(),
            "pending_reviews_count": pending_reviews.count(),
            "trash_reviews_count": trash_reviews.count()
        }

        return render(request, "user/admin/dashboard.html", context)


class InvoiceView(AccessMixinView, BaseViewMixin):
    only_role = "Admin"

    def get(self, request):
        return render(request, "user/admin/invoice.html")


class ReportsView(AccessMixinView, BaseViewMixin):
    only_role = "Admin"

    def get(self, request):
        return render(request, "user/admin/reports.html")


class RoleSettingsView(AccessMixinView, BaseViewMixin):
    only_role = "Admin"

    def get(self, request):
        groupData = Group.objects.all()
        context = {'data': groupData}
        return render(request, "user/admin/role_settings.html", context)

    def post(self, request):
        groupData = Group.objects.all()
        context = {'data': groupData}
        if 'delete_role' in request.POST:
            group = Group.objects.filter(id=request.POST['role_id'])
            if group[0].name == 'Admin' or group[0].name =='Batuwa' or group[0].name=='Guide':
                messages.error(request, f"Unable to delete this role")
                return render(request, "user/admin/role_settings.html", context)
            else:
                group.delete()
                messages.success(request, f"Role successfully deleted")
                groupData = Group.objects.all()
                context = {'data': groupData}
                return render(request, "user/admin/role_settings.html", context)
        if 'edit_role' in request.POST:
            group_obj = Group.objects.get(id=request.POST['role_id'])
            group_obj.name = request.POST['role_name']
            group_obj.save()

        else:
            try:
                name = request.POST['name']
            except:
                messages.success(request, f"Please enter role name")
                return render(request, "user/admin/role_settings.html", context)
            group = Group.objects.filter(name__iexact = name)
            if group:
                messages.success(request, f"Role name {name} already exists")
                return render(request, "user/admin/role_settings.html", context)
            else:
                group = Group.objects.create(name=name)
                messages.success(request, f"Role {name} created successfully")
                groupData = Group.objects.all()
                context = {'data': groupData}
                return render(request, "user/admin/role_settings.html", context)
            groupData = Group.objects.all()
            context = {'data': groupData}
            return render(request, "user/admin/role_settings.html", context)
        groupData = Group.objects.all()
        context = {'data': groupData}
        return render(request, "user/admin/role_settings.html", context)


class PermissionSettingsView(AccessMixinView, BaseViewMixin):
    only_role = "Admin"

    def get(self, request, role_id=None):
        groupData = Group.objects.all()
        permission = Permission.objects.all()
        context = {'data': groupData, 'permissions': permission}
        return render(request, "user/admin/roles_permission.html", context)

    def post(self, request, role_id=None):
        print(request.POST)
        groupData = Group.objects.filter(id=role_id)
        permission = Permission.objects.all()
        context = {'data': groupData, 'permissions': permission}
        return render(request, "user/admin/roles_permission.html", context)


class CategoryView(AccessMixinView, BaseViewMixin):
    only_role = "Admin"

    def get(self, request):
        categories = ProjectCategory.objects.all()
        name = request.GET.get('category_name')

        if name:
            categories = categories.filter(name__icontains=name)
        res = PaginateView()
        page = self.request.GET.get("page")
        response = res.give_paginated_response(page, categories, 10)
        context = {"page_obj": response, 'category_name': name}
        return render(request, "user/admin/categories.html", context)

    def post(self, request):
        if "add_category" in request.POST:
            name = request.POST.get("name")
            ProjectCategory.objects.create(name=name)
            messages.success(request, f"Category was successfully created !")

        if "edit_category" in request.POST:
            category = get_object_or_404(
                ProjectCategory, id=request.POST.get("category_id")
            )
            category.name = request.POST.get("name")
            category.save()
            messages.success(request, f"Category was successfully edited !")

        if "delete_category" in request.POST:
            category = get_object_or_404(
                ProjectCategory, id=request.POST.get("category_id")
            )
            category.delete()
            messages.success(request, f"Category was successfully deleted !")

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class UserListView(AccessMixinView, BaseViewMixin):
    only_role = "Admin"

    def get(self, request):
        user_filter = request.GET.get('user_filter')

        if user_filter == 'a':
            users = User.objects.filter(role='Admin')
        elif user_filter == 'f':
            users = User.objects.filter(role='Freelancer')
        elif user_filter == 'e':
            users = User.objects.filter(role='Employer')
        else:
            users = User.objects.all()

        form = CustomUserCreationForm()

        f = UserFilter(self.request.GET, queryset=users)
        res = PaginateView()
        page = self.request.GET.get("page")
        response = res.give_paginated_response(page, f.qs, 10)
        context = {"page_obj": response, "searchForm": f,
                   "form": form, 'user_filter': user_filter}
        return render(request, "user/admin/users.html", context)

    def post(self, request):

        user_id = request.POST.get("u_id")
        if "create_user" in request.POST:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form_obj = form.save(commit=False)
                role = request.POST.get("role")
                form_obj.role = role
                form_obj.save()
                messages.success(request, f"User was successfully created !")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            else:
                messages.error(request, list(form.errors.values())[-1])
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        if "delete_user" in request.POST:
            try:
                user = get_object_or_404(User, id=user_id)
                user.delete()
                return JsonResponse({"deleted": True, "id": user_id})
            except:
                return JsonResponse({"deleted": False})
        return JsonResponse({"res": "ponse"})


project_type_map = {
    "all": "all",
    "ongoing": "ON",
    "completed": "COM",
    "cancelled": "CAN",
    "pending": "PEN",
}


class ProjectListView(AccessMixinView):
    only_role = "Admin"

    def get(self, request, project_type):
        all_projects = Project.objects.all()
        has_type = project_type_map.get(project_type)
        if not has_type:
            raise Http404
        if project_type.lower() == "all":
            projects = Project.objects.all()
        else:
            projects = Project.objects.filter(
                status=project_type_map[project_type])

        all_count = all_projects.count()
        on_count = all_projects.filter(status="ON").count()
        com_count = all_projects.filter(status="COM").count()
        can_count = all_projects.filter(status="CAN").count()
        pen_count = all_projects.filter(status="PEN").count()

        f = ProjectFilter(self.request.GET, queryset=projects)
        page = self.request.GET.get("page")
        res = PaginateView()
        response = res.give_paginated_response(page, f.qs, 10)

        context = {
            "projects": projects,
            "project_type": project_type,
            "all_count": all_count,
            "on_count": on_count,
            "can_count": can_count,
            "com_count": com_count,
            "pen_count": pen_count,
        }
        context["page_obj"] = response
        context["searchForm"] = f

        return render(request, "user/admin/projects.html", context)

    def post(self, request, project_type):
        if "delete_project" in request.POST:
            p_id = request.POST.get("project_id")
            project = get_object_or_404(Project, id=p_id)
            project.delete()
            messages.success(
                request, f"Project({p_id}) was successfully deleted !")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class UserDetailView(AccessMixinView):
    only_role = "Admin"

    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        activities = user.activities.all()
        res = PaginateView()
        page = self.request.GET.get("page")
        response = res.give_paginated_response(page, activities, 10)
        context = {"page_obj": response, "user": user}
        return render(request, "user/admin/userdetail.html", context)


class ProjectEditView(AccessMixinView):
    only_role = "Admin"

    def get(self, request, id):
        project = get_object_or_404(Project, id=id)
        form = ProjectForm(instance=project)
        context = {"project": project, "form": form}
        return render(request, "user/admin/project_edit.html", context)

    def post(self, request, id):
        project = get_object_or_404(Project, id=id)
        form = ProjectForm(request.POST, instance=project)
        skills = request.POST.getlist('desired_skills')
        files = request.FILES.getlist('project_files')

        if form.is_valid():
            print('form valid')
            if request.user.role == "Admin":
                f = form.save()
                f.desired_skills.set(give_or_create_skills(''.join(skills)))
                for i in files:
                    ProjectDocument.objects.create(project=f, documents=i)
                messages.success(request, f"Project was successfully edited !")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        messages.success(request, f"{form.errors} !")
        context = {"project": project, "form": form}
        return render(request, 'user/admin/project_edit.html', context)


class UserEditView(AccessMixinView):
    only_role = "Admin"

    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        form = AdminUserChangeForm(instance=user)
        context = {"user": user, "form": form}
        return render(request, "user/admin/user_edit.html", context)

    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        form = AdminUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            f = form.save(commit=False)
            profile_img = request.FILES.get("profile_img")
            banner_img = request.FILES.get("banner_img")
            if profile_img:
                f.avatar = profile_img
            if banner_img:
                f.banner_image = banner_img
            f.save()
            messages.success(request, "Profile successfully updated !")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        context = {"form": form}
        return render(request, "user/admin/user_edit.html", context)


class DeleteProject(AccessMixinView):
    only_role = "Admin"

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        return JsonResponse(
            {
                "delted": True,
                "id": project_id,
                "msg": f"Project {project_id} successfully deleted !",
            }
        )


class IdentyFormList(AccessMixinView):
    only_role = "Admin"

    def get(self, request):
        forms = IdentityForm.objects.all()
        f = IdentiyFormFilter(self.request.GET, queryset=forms)
        res = PaginateView()
        page = self.request.GET.get("page")
        response = res.give_paginated_response(page, f.qs, 10)
        context = {"page_obj": response, "searchForm": f}
        return render(request, "user/admin/identity_form.html", context)


class UserDeleteAdmin(AccessMixinView):
    only_role = "Admin"

    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        user.delete()
        messages.success(
            request, f"User {user.display_name} successfully deleted !")
        return redirect('user_list')


class ReviewAdminList(AccessMixinView):
    only_role = "Admin"

    def get(self, request):

        reviews = Reviews.objects.all()
        f = ReviewFilter(self.request.GET, queryset=reviews)
        res = PaginateView()
        page = self.request.GET.get("page")
        response = res.give_paginated_response(page, f.qs, 10)
        context = {"page_obj": response, "searchForm": f}
        return render(request, "user/admin/reviews.html", context)


class PermissionStatusUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        group_id = request.data.get('group_id')
        permission_id = request.data.get('permission_id')
        group = Group.objects.get(id=group_id)
        permission = Permission.objects.get(id=permission_id)
        group.permissions.add(permission)
        group.save()
        return JsonResponse({'message':'success'}, safe=False)