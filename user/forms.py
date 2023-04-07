from django.contrib.auth.forms import UserCreationForm
from . models import IdentityForm, SocialLink, User, UserDeleteRecords
from django import forms
from django.forms import ModelForm,Textarea
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import Group, Permission

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control floating mt-2  '}))
    email = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control floating mt-2 ','type':'email'}))
    password1 = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control floating mt-2 ','type':'password'}))
    password2 = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control floating mt-2 ','type':'password'}))
    display_name = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control floating mt-2  '}))

    class Meta:
        model = User
        fields = ('email','username','display_name','password1','password2')


class CustomUserChangeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['language_one'].label = "Language"
        self.base_fields['gender'].initial = 'Male'

    email = forms.CharField(widget=forms.TextInput(attrs={'type':'email'}))
    overview=forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = User
        fields = ('email','username','avatar','title','display_name','availability','language_one','gender','contact','overview','hourly_rate','address','state','country','zipcode')

     

class AdminUserChangeForm(ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'type':'email'}))
    language_one = forms.CharField(label="Language",required=False)
    verified = forms.BooleanField(label="Verify User",required=False)
    class Meta:
        model = User
        fields = ('email','username','avatar','verified','is_active','title','display_name','language_one','gender','contact','overview','hourly_rate','address','state','country','zipcode')

        widgets = {
            'overview': Textarea(attrs={'cols': 80, 'rows': 4}),
        }

class SocialLinkForm(ModelForm):
    class Meta:
        model = SocialLink
        exclude=('user',)
  
class IdentiyuserForm(ModelForm):
    class Meta:
        model = IdentityForm
        exclude=('user','document')


class UserDeleteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserDeleteForm, self).__init__(*args, **kwargs)
        self.fields['reason'].label = "Please Explain Further"
        #self.fields['reason'].widget.attrs['rows'] = 3
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = UserDeleteRecords
        fields = ['reason', 'password', ]
        exclude = ['email']

        widget = {
            'reason': forms.Textarea(attrs={'rows': 3}),

        }
  

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name",)