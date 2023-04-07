from django.db import models
from django_countries.fields import CountryField
from allauth.socialaccount.models import SocialApp
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class SiteSetting(models.Model):
    CHOICES = (
        ('Live', 'Live'),
        ('Down', 'Down'),
        ('Maintainance', 'Maintainance'),
    )
    site_name=models.CharField(default="batuwa",max_length=100,null=True, blank=True)
    logo_image=models.ImageField(upload_to='siteoption', null=True, blank=True)
    contact_email=models.CharField(max_length=100,null=True, blank=True)
    mode=models.CharField(max_length=20, choices=CHOICES, default='Live')
    favicon = models.ImageField(upload_to='siteoption',null=True, blank=True)
    address_1 = models.CharField( max_length=100,null=True, blank=True)
    address_2 = models.CharField( max_length=100,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=100,null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    country = CountryField(null=True, blank=True, blank_label="Select Country")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class LocalizationSetting(models.Model):
    time_zone=models.CharField(max_length=100,null=True, blank=True)
    date_format=models.CharField(max_length=100,null=True, blank=True)
    time_format = models.CharField( max_length=100,null=True, blank=True)
    symbol = models.CharField( max_length=100,null=True, blank=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class PaymentSetting(models.Model):
    CHOICES = (
        ('Sandbox', 'Sandbox'),
        ('Live', 'Live'),
    )
    mode=models.CharField(max_length=20, choices=CHOICES, default='Sandbox')
    gateway_name=models.CharField(max_length=100,null=True, blank=True)
    api_key=models.CharField(max_length=100,null=True, blank=True)
    rest_key = models.CharField( max_length=100,null=True, blank=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class EmailSetting(models.Model):
    CHOICES = (
        ('Live', 'Live'),
        ('Down', 'Down'),
        ('Maintainance', 'Maintainance'),
    )
    email_address=models.CharField(max_length=100,null=True, blank=True)
    password=models.CharField(max_length=100,null=True, blank=True)
    mode=models.CharField(max_length=20, choices=CHOICES, default='Live')
    host = models.CharField( max_length=100,null=True, blank=True)
    port = models.CharField( max_length=100,null=True, blank=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ExtendedSocialSetting(SocialApp):
    is_active = models.BooleanField(default=True)

    @classmethod
    def google_load(cls):
        obj, created = cls.objects.get_or_create(provider__icontains='Google')
        return obj

    @classmethod
    def twitter_load(cls):
        obj, created = cls.objects.get_or_create(provider__icontains='Twitter')
        return obj

    @classmethod
    def facebook_load(cls):
        obj, created = cls.objects.get_or_create(provider__icontains='Facebook')
        return obj
    
    @classmethod
    def linkdin_load(cls):
        obj, created = cls.objects.get_or_create(provider__icontains='linkedin')
        return obj
    
    @classmethod
    def google_fetch(cls):
        obj = cls.objects.get(provider__icontains='Google')
        return obj

    @classmethod
    def twitter_fetch(cls):
        obj = cls.objects.get(provider__icontains='Twitter')
        return obj

    @classmethod
    def facebook_fetch(cls):
        obj = cls.objects.get(provider__icontains='Facebook')
        return obj
    
    @classmethod
    def linkdin_fetch(cls):
        obj = cls.objects.get(provider__icontains='linkedin')
        return obj
    
    def __str__(self):
        return f"{self.name} --> {self.provider}"



# class SocialSetting(models.Model):
#     SOCIAL_CHOICES = (
#         ('Google', 'Google'),
#         ('Facebook', 'Facebook'),
#         ('Twitter', 'Twitter'),
#         ('Linkdin', 'Linkdin'),
#     )
#     CHOICES = (
#         ('Active', 'Active'),
#         ('Inactive', 'Inactive'),
#     )
#     mode=models.CharField(max_length=20, choices=CHOICES, default='Inactive')
#     media=models.CharField(max_length=20, choices=SOCIAL_CHOICES)
#     id_number=models.CharField(max_length=100,null=True, blank=True)
#     key=models.CharField(max_length=100,null=True, blank=True)

#     # def save(self, *args, **kwargs):
#     #     self.pk = 1
#     #     super().save(*args, **kwargs)

#     def delete(self, *args, **kwargs):
#         pass

#     @classmethod
#     def google_load(cls):
#         obj, created = cls.objects.get_or_create(media__icontains='Google')
#         return obj

#     @classmethod
#     def twitter_load(cls):
#         obj, created = cls.objects.get_or_create(media__icontains='Twitter')
#         return obj

#     @classmethod
#     def facebook_load(cls):
#         obj, created = cls.objects.get_or_create(media__icontains='Facebook')
#         return obj
    
#     @classmethod
#     def linkdin_load(cls):
#         obj, created = cls.objects.get_or_create(media__icontains='Linkdin')
#         return obj
    
#     @classmethod
#     def google_fetch(cls):
#         obj = cls.objects.get(media__icontains='Google')
#         return obj

#     @classmethod
#     def twitter_fetch(cls):
#         obj = cls.objects.get(media__icontains='Twitter')
#         return obj

#     @classmethod
#     def facebook_fetch(cls):
#         obj = cls.objects.get(media__icontains='Facebook')
#         return obj
    
#     @classmethod
#     def linkdin_fetch(cls):
#         obj = cls.objects.get(media__icontains='Linkdin')
#         return obj
    
#     def __str__(self):
#         return f"{self.id} --> {self.media}"

class SEOSetting(models.Model):
    title=models.CharField(max_length=100,null=True, blank=True)
    keywords=models.TextField(max_length=100,null=True, blank=True)
    description = models.TextField( max_length=200,null=True, blank=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class OtherSetting(models.Model):
    SOCIAL_CHOICES = (
        ('Google_Analytics', 'Google_Analytics'),
        ('Google_Adsense', 'Google_Adsense'),
        ('Facebook_Messenger', 'Facebook_Messenger'),
        ('Facebook_Pixel', 'Facebook_Pixel'),
        ('Google_Recaptcha', 'Google_Recaptcha'),
        ('Cookies_Agreement', 'Cookies_Agreement'),
    )
    CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    mode=models.CharField(max_length=20, choices=CHOICES, default='Inactive')
    media = models.CharField(max_length=20, choices=SOCIAL_CHOICES, blank=True, null=True)
    descriptions=models.CharField(max_length=100,null=True, blank=True)
    key=models.CharField(max_length=100,null=True, blank=True)
    site_key=models.CharField(max_length=100,null=True, blank=True)
    secret_key=models.CharField(max_length=100,null=True, blank=True)


    # def delete(self, *args, **kwargs):
    #     pass

    @classmethod
    def google_analytics_load(cls):
        obj, created = cls.objects.get_or_create(media__icontains='Google_Analytics')
        return obj

    @classmethod
    def google_adsense_load(cls):
        obj, created = cls.objects.get_or_create(media__icontains='Google_Adsense')
        return obj

    @classmethod
    def facebook_messenger_load(cls):
        obj, created = cls.objects.get_or_create(media__icontains='Facebook_Messenger')
        return obj

    @classmethod
    def facebook_pixel_load(cls):
        obj, created = cls.objects.get_or_create(media__icontains='Facebook_Pixel')
        return obj
    
    @classmethod
    def google_rechaptcha_load(cls):
        obj, created = cls.objects.get_or_create(media__icontains='Google_Recaptcha')
        return obj
    
    @classmethod
    def cookie_agreement_load(cls):
        obj, created = cls.objects.get_or_create(media__icontains='Cookies_Agreement')
        return obj


    @classmethod
    def google_analytics_fetch(cls):
        obj = cls.objects.get(media__icontains='Google_Analytics')
        return obj

    @classmethod
    def google_adsense_fetch(cls):
        obj = cls.objects.get(media__icontains='Google_Adsense')
        return obj

    @classmethod
    def facebook_messenger_fetch(cls):
        obj = cls.objects.get(media__icontains='Facebook_Messenger')
        return obj

    @classmethod
    def facebook_pixel_fetch(cls):
        obj = cls.objects.get(media__icontains='Facebook_Pixel')
        return obj
    
    @classmethod
    def google_rechaptcha_fetch(cls):
        obj = cls.objects.get(media__icontains='Google_Recaptcha')
        return obj
    
    @classmethod
    def cookie_agreement_fetch(cls):
        obj = cls.objects.get(media__icontains='Cookies_Agreement')
        return obj