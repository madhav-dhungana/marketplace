from django.urls import path, include
from .views import *

urlpatterns = [
    path('blog-list', BlogListView.as_view(), name='blog_list_page'),
    path('blog-grid', BlogGridView.as_view(), name='blog_grid_page'),
    path('blog-detail/<str:slug>/', BlogDetailView.as_view(), name='blog_detail'),
]