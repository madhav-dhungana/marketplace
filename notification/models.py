from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    action=models.CharField(max_length=100)
    title=models.CharField(max_length=100,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    action_by=models.ForeignKey("user.User", on_delete=models.SET_NULL,null=True, related_name='notification_by')
    action_to=models.ForeignKey("user.User",related_name="notification_to",on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    user_has_seen=models.BooleanField(default=False)

    class Meta:
        ordering=['-id']