from django.shortcuts import redirect
from django.http import Http404
from django.core.exceptions import PermissionDenied




def only_non_authorized(func):
    def wrap(request,*args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.is_patient:
                return redirect("dashboard")
        else:
            return func(request,*args, **kwargs)
    return wrap

