from django.shortcuts import get_object_or_404
from rest_framework import permissions

from projects.models import Project

class IsUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user

class IsBatuwaAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == "Admin"

        
class RequestUserOrAdminEdit(permissions.BasePermission):
    message = 'Only the person himself or Admin are Allowed to Edit .'

    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return True if request.user == obj or request.user.role == "Admin" else False


class InviteUserOrAdminPerm(permissions.BasePermission):
    message = "You don't have enough permission for this !"

    def has_permission(self, request, view):
        user= request.user
        if user.role == "Admin":
            return True

        if request.method in permissions.SAFE_METHODS:
            return user.is_authenticated
        
        if request.method == "POST":
            if user.role == "Freelancer":
                return False
            #check if the project is created by the user as employer cannot create project for other project
            project = get_object_or_404(Project,id=request.data.get("project_id"))
            if project.posted_by != request.user:
                self.message = "Project not found !"
                return False
            return True
    
    def has_object_permission(self, request,view, obj):
        
        if request.user.role == "Admin" or request.user == obj.sent_by:
            return True
        if request.method in permissions.SAFE_METHODS:
            if obj.sent_to == request.user:
                return True
        return False 
        

class OwnerOrAdminEdit(permissions.BasePermission):
    message = "You don't have enough permission for this !"

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request,view, obj):
        model_name =obj.__class__.__name__
        if request.method in permissions.SAFE_METHODS:
            return True
        if model_name == "Project" or model_name=="Reviews":
            return True if request.user == obj.posted_by or request.user.role == "Admin" else False

