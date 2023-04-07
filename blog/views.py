from django.contrib import auth, messages
from django.http import (Http404, HttpResponse, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import render
from django.views import View
from user.mixins import AccessMixinView, BaseViewMixin
from datetime import datetime, timedelta

from .models import *


class BlogListView(View):
    def get(self, request):
        blogData = Blog.objects.all()
        listBlogData = blogData.filter(is_list=True)
        latestPost = blogData.filter(
            created_at__gte=datetime.today() - timedelta(days=3)).order_by('-created_at')
        categoryData = Category.objects.all()
        tagData = Tag.objects.all()
        context = {'listBlogData': listBlogData, 'categoryData': categoryData,
                   'tagData': tagData, 'latestPost': latestPost}
        return render(request, 'blog-list.html', context)


class BlogGridView(View):
    def get(self, request):
        blogData = Blog.objects.all()
        blogData = blogData.filter(is_list=False)
        latestPost = Blog.objects.filter(
            created_at__gte=datetime.today() - timedelta(days=3)).order_by('-created_at')
        categoryData = Category.objects.all()
        tagData = Tag.objects.all()
        context = {'blogData': blogData, 'categoryData': categoryData,
                   'tagData': tagData, 'latestPost': latestPost}
        return render(request, 'blog-grid.html', context)


class BlogDetailView(View):
    def get(self, request, slug=None):
        blogData = Blog.objects.filter(slug=slug)
        latestPost = Blog.objects.filter(
            created_at__gte=datetime.today() - timedelta(days=3)).order_by('-created_at').exclude(slug=slug)
        categoryData = Category.objects.all()
        tagData = Tag.objects.all()
        print(blogData)
        context = {'blogData': blogData, 'categoryData': categoryData,
                   'tagData': tagData, 'latestPost': latestPost}
        return render(request, 'blog-details.html', context)
