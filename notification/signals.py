import json
from django.dispatch import receiver    
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Notification
from channels.layers import get_channel_layer

@receiver(post_save,sender=Notification)
def create_notification(sender, instance, created, *args, **kwargs):
    for_user = instance.action_to.username
    noti_count = Notification.objects.filter(
        action_to=instance.action_to,
        user_has_seen=False
        ).count()
   
    if created:
        url =instance.content_object.get_absolute_url()
        cc = ["Project","InviteModel"]
        if instance.content_object.__class__.__name__ in cc:
            print('changni for freelancer')
            if instance.action_to.role == 'Freelancer':
                url = instance.content_object.get_absolute_for_freelancer()

        channel_layer = get_channel_layer()
        created_time = instance.date_created.strftime("%b %d %H:%M %p")
        img_url = instance.action_by.avatar.url if instance.action_by else None
        async_to_sync(channel_layer.group_send)(
        f'notify_{for_user}',
            {
                "type":"send_notification",
                "message":f" {instance.title}",
                "count":noti_count,
                "time":created_time,
                "action_by_url":img_url,
                "notification_url":url
            }
        )