from django.contrib import admin
# Register your models here.
from .models import *

admin.site.register(SiteSetting)
admin.site.register(LocalizationSetting)
admin.site.register(PaymentSetting)
admin.site.register(EmailSetting)
admin.site.register(ExtendedSocialSetting)
admin.site.register(SEOSetting)
admin.site.register(OtherSetting)
# admin.site.register(SocialApplication)