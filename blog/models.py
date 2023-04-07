from django.db import models
from user.models import User
from django.template.defaultfilters import slugify
import uuid

class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Blog(models.Model):
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=300)
    thumbnail = models.FileField(null=True, blank=True)
    description = models.TextField(max_length=50000)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True)
    tag = models.ManyToManyField(Tag)
    slug = models.SlugField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    is_list = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class BlogImage(models.Model):
    image = models.FileField(upload_to='blog/images')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.blog.title


class Review(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reply = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)


class Subscriber(models.Model):
    email = models.EmailField()
    created_at = models.DateField(auto_now_add=True, editable=False)
    updated_at = models.DateField(auto_now=True, editable=False)
    token = models.UUIDField(editable=False, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.email}"
    
    def save(self, *args, **kwargs):  # new
        if not self.token:
            self.token = uuid.uuid4()
        return super().save(*args, **kwargs)
