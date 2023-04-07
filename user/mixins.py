from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views import View
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

class BaseViewMixin(LoginRequiredMixin,View):
    """
        Base View Mixin which will inherit common views
    """


class UnAuthorizedView(View):
    """
     Only unauthenticated user can view (eg . register , login page)
    """
    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

class NonAdminView(LoginRequiredMixin,View):
    """
     Admin cannot view this . Only freelancer or employer can view 
     Because this view has condition set up for non admin user
    """
    def dispatch(self,request,*args, **kwargs):
        if request.user.role== "Admin":
            raise Http404
        return super().dispatch(request, *args, **kwargs)

class AccessMixinView(LoginRequiredMixin,View):
    """
     Only given role are allowed to access view else 404 error is raised 
    """
    only_role = None
    def dispatch(self,request,*args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        #admin can access anything
        # if request.user.role == "Admin":
        #     return super().dispatch(request, *args, **kwargs)
        
        if request.user.role != self.only_role:
            raise Http404
        return super().dispatch(request, *args, **kwargs)



class PaginateView:
    def give_paginated_response(self,page,qs,num=5):
        paginator = Paginator(qs, num)
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)
        
        return response


class AdminOnlyView(AccessMixinView):
    only_role = "Admin"

class FreelancerView(AccessMixinView):
    only_role = "Freelancer"

class EmployerView(AccessMixinView):
    only_role = "Employer"