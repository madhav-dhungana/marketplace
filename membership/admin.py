from django.contrib import admin
from .models import *


admin.site.register(Membership)
admin.site.register(PaymentHistory)
admin.site.register(UserMembership)
admin.site.register(Subscription)
admin.site.register(Plan)