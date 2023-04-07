from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages, auth
from user.mixins import AccessMixinView, BaseViewMixin
from django.views.generic import ListView
from projects.models import Project, Reviews
from blog.models import Blog, Subscriber
from user.models import User
from django.db.models import Count, Min, Max
import re


class IndexView(View):
    def get(self, request):
        total_batuwa = Project.objects.available().filter(
            status__icontains='Active').count()
        completed_project = Project.objects.filter(
            status__icontains='COM').count()
        all_projects = Project.objects.available()[:8]
        blog = Blog.objects.all().order_by('-created_at')[:3]
        mostHired = User.objects.filter(role='Freelancer')
        jobCount = Project.objects.values('posted_by').order_by().annotate(project_count=Count(
            'posted_by')).aggregate(min_val=Min('project_count'), max_val=Max('project_count'))
        reviews = Reviews.objects.filter(
            is_approved=True, is_trash=False).order_by('-id')[:5]
        context = {'total_batuwa': total_batuwa, 'completed_task': completed_project,
                   'blog': blog, 'projects': all_projects, 'mosthired': mostHired, 'reviews': reviews, 'minJobCount': jobCount['min_val'], 'maxJobCount': jobCount['max_val']}
        return render(request, 'index.html', context)


class SubscribeView(View):
    def post(self, request):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        email = request.POST.get('email', None)
        if email:
            if re.search(regex, email):
                qs = Subscriber.objects.filter(email=email)
                if qs:
                    messages.error(request, 'Email is already subscribed')
                    return redirect('index')
                else:
                    Subscriber.objects.create(email=email)
                    messages.success(
                        request, 'Email is successfully subscribed')
                    return redirect('index')
            else:
                messages.error(request, 'Invalid email address')
                return redirect('index')
        else:
            messages.error(request, 'Invalid email address')
            return redirect('index')
        return redirect('index')

    def get(self, request):
        return redirect('index')
