from django.db import models
from user.models import User
from django.db.models import Q



class MessageManager(models.Manager):
    def by_room(self, room):
        messages = Message.objects.filter(room=room)
        return messages

class PrivateChatManager(models.Manager):
    def create_room_if_none(self,u1,u2):
        has_room = PrivateChat.objects.filter(Q(user1=u1 ,user2=u2)| Q(user1=u2,user2=u1)).first()
        if not has_room:
            PrivateChat.objects.create(user1=u1,user2=u2)
        return has_room  
    



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PrivateChat(BaseModel):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")
    connected_users = models.ManyToManyField(
        User, blank=True, related_name="connected_users")
    is_active = models.BooleanField(default=False)
    objects = PrivateChatManager()

    def __str__(self) -> str:
        return f'Room of {self.user1} - {self.user2}'
    
    #to track if user is in the chat room
    def connect_or_leave(self,user):
        if not user in self.connected_users.all():
            self.connected_users.add(user)
        else:
            self.connected_users.remove(user)

    
    def last_msg(self):
        msg =self.message_set.all()
        return msg.first() # message is ordered from -id


class Message(BaseModel):
    room = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)
    objects = MessageManager()

    def __str__(self) -> str:
        return f'From <Room - {self.room}>'
    
    class Meta:
        ordering=['-id']