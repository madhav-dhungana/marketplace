
from django.urls import path
from .views import PrivateChatView,ChatHomeView,ChatPaginatedAPI


urlpatterns = [
   path('',ChatHomeView.as_view(), name='home_chat'),
   path('<str:username>/',PrivateChatView.as_view(), name='project_chat'),
   path('c/<str:username>/',ChatPaginatedAPI.as_view(), name='c_project_chat'),
]