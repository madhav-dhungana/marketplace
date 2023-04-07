from django.urls import path
from .views import MyNotificationView,ReadUnreadNotification,LastFourNotification

urlpatterns = [
   path('notifications',MyNotificationView.as_view(), name='my_notifications'),
   path('last-notification',LastFourNotification.as_view(), name='last_four_notification'),
   path('read-notification',ReadUnreadNotification.as_view(), name='read_unread_notification'), 
]