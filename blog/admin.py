from django.contrib import admin
from .models import *

admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(BlogImage)
admin.site.register(Review)