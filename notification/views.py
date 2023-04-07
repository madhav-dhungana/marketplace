from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from notification.models import Notification
from user.api.tasks import read_user_unread_notification
from user.mixins import BaseViewMixin,PaginateView
from rest_framework.views import APIView
from rest_framework.response import Response
import copy

class MyNotificationView(BaseViewMixin):
    template_name="notification/user/all_notification.html"
    paginate_by = 15
    context_object_name = 'page_obj'

    def get(self,request):
        notices = self.request.user.notification_to.all()
        res = PaginateView()
        page = self.request.GET.get("page")
        response = res.give_paginated_response(page, notices, 20)
        unread_notice = notices.filter(user_has_seen=False)
        unread_notice.update(user_has_seen=True)
        context={"page_obj":response}
        context['check_arrs'] = ["Project","InviteModel"]
        return render(request,self.template_name,context)

class ReadUnreadNotification(APIView):
    def get(self,request):
        request.user.notification_to.filter(user_has_seen=False).update(user_has_seen=True)
        unread_notice_count = request.user.notification_to.filter(user_has_seen=False).count()
        return Response({"unread_notice_count":unread_notice_count})

class LastFourNotification(BaseViewMixin):
    def get(self,request):
        notice = self.request.user.notification_to.filter(user_has_seen=False)[:4]
        notification = copy.deepcopy(notice)
        # read_user_unread_notification.delay(request.user.id)

        context ={"notification":notification}        
        self.request.user.notification_to.filter(user_has_seen=False).update(user_has_seen=True)
        return render(request,'notification/user/htmx_notice.html',context)