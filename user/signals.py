from django.dispatch import receiver    
from django.db.models.signals import post_save,post_delete,pre_save
from django.template.loader import render_to_string
from user.api.tasks import background_email_send
from .models import User


# @receiver(post_delete,sender=User)
# def deleted_user_signal(sender, instance, *args, **kwargs):
#     email = instance.email
#     title = "Account Deleted"
#     email_data = {
#                 "site_name": "Batuwa",
#             }
#     message = render_to_string('email/user_deleted_email.html', email_data)
#     background_email_send.delay(title,message,[email])

# @receiver(post_save,sender=User)
# def user_created_signals(sender, instance,created, *args, **kwargs):
#     if created:
#         if not instance.display_name:
#             User.objects.filter(id=instance.id).update(display_name=instance.username)

