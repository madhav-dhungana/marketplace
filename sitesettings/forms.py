from django import forms
from user.models import SocialLink, User

from .models import (EmailSetting, LocalizationSetting, OtherSetting,
                     PaymentSetting, SEOSetting, SiteSetting, ExtendedSocialSetting)


class SiteBasicForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields=('site_name',)
  
class SiteAddressForm(forms.ModelForm):
    address_1 = forms.CharField(label="Primary Address", widget=forms.TextInput(attrs={'placeholder': 'Enter Primary address'}), required=False)
    address_2 = forms.CharField(label="Secondary Address", widget=forms.TextInput(attrs={'placeholder': 'Enter Secondary address'}), required=False)
    city = forms.CharField(label="City", widget=forms.TextInput(attrs={'placeholder': 'Enter city'}), required=False)
    state = forms.CharField(label="State", widget=forms.TextInput(attrs={'placeholder': 'Enter state name'}), required=False)
    zipcode = forms.CharField(label="Zipcode", widget=forms.TextInput(attrs={'placeholder': 'Enter zipcode'}), required=False)
    class Meta:
        model = SiteSetting
        fields=('address_1','address_2','city','state','zipcode','country')

class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentSetting
        fields=('gateway_name','api_key','rest_key')

class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailSetting
        fields=('email_address','password','host','port')

class SEOForm(forms.ModelForm):
    class Meta:
        model = SEOSetting
        fields=('title','keywords','description') 


class LocalizationSettingForm(forms.ModelForm):
    class Meta:
        model = LocalizationSetting
        fields = ('time_zone','date_format','time_format','symbol')


class SocialSettingForm(forms.ModelForm):
    class Meta:
        model = ExtendedSocialSetting
        fields = ("is_active","name","client_id","secret")


class GoogleSocialSettingForm(forms.ModelForm):
    class Meta:
        model = ExtendedSocialSetting
        fields = ("is_active","name","client_id","secret")
    

class FacebookSocialSettingForm(forms.ModelForm):
    class Meta:
        model = ExtendedSocialSetting
        fields = ("is_active","name","client_id","secret")
    


class TwitterSocialSettingForm(forms.ModelForm):
    class Meta:
        model = ExtendedSocialSetting
        fields = ("is_active","name","client_id","secret")
    
        

class LinkdinSocialSettingForm(forms.ModelForm):
    class Meta:
        model = ExtendedSocialSetting
        fields = ("is_active","name","client_id","secret")


class SocialLinkSettingForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ('facebook','linkedin','twitter')


class GoogleAnalyticsForm(forms.ModelForm):
    class Meta:
        model = OtherSetting
        fields = ('descriptions',)

class GoogleAdsenseForm(forms.ModelForm):
    class Meta:
        model = OtherSetting
        fields = ('descriptions',)

class FacebookMessengerForm(forms.ModelForm):
    class Meta:
        model = OtherSetting
        fields = ('descriptions',)

class FacebookPixelForm(forms.ModelForm):
    class Meta:
        model = OtherSetting
        fields = ('descriptions',)


class GoogleRecaptchaForm(forms.ModelForm):
    class Meta:
        model = OtherSetting
        fields = ('site_key','secret_key')


class CookieAgreement(forms.ModelForm):
    class Meta:
        model = OtherSetting
        fields = ("descriptions",)