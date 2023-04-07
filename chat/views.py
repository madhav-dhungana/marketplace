from email import message
from django.shortcuts import get_object_or_404, render
from django.views import View
from .serializers import MessageSerializer
from mainproject.pagination import CustomPagination
from user.mixins import PaginateView
from .models import Message, PrivateChat
from django.db.models import Q
from user.mixins import BaseViewMixin
from user.models import User
from rest_framework.views import APIView
# Create your views here.
from rest_framework.response import Response

class PrivateChatView(BaseViewMixin):
    def get(self, request, username):
        me = request.user
        chatting_with = get_object_or_404(User, username=username)
        c = PrivateChat.objects.create_room_if_none(me, chatting_with)
        get_room = PrivateChat.objects.filter(
            Q(user1=me, user2=chatting_with) | Q(user1=chatting_with, user2=me)
        ).first()
        message = Message.objects.by_room(get_room)
        all_messages = message[:20:-1]
        has_second_page = message.count() > 20
        recent_rooms = PrivateChat.objects.filter(Q(user1=me) | Q(user2=me))[:6]
        context = {
            "me": me,
            "chatting_with": chatting_with,
            "messages": all_messages,
            "recent_rooms": recent_rooms,
            "has_second_page":has_second_page
        }
        return render(request, "chat/project_chat.html", context)

class ChatPaginatedAPI(APIView):
  
    def get(self,request,username):
        print('user name is ',username)
        me = self.request.user
        chatting_with = get_object_or_404(User, username=username)
        c = PrivateChat.objects.create_room_if_none(me, chatting_with)
        get_room = PrivateChat.objects.filter(
            Q(user1=me, user2=chatting_with) | Q(user1=chatting_with, user2=me)
        ).first()
        all_messages = Message.objects.by_room(get_room)
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(all_messages,request)
        serializer = MessageSerializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
      
class ChatHomeView(BaseViewMixin):
    def get(self, request):
        me = request.user
        recent_rooms = PrivateChat.objects.select_related('user1').filter(Q(user1=me) | Q(user2=me))[:6]
        context = {
            "recent_rooms": recent_rooms,
        }
        return render(request, "chat/chat_home.html", context)