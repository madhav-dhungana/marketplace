
from django import forms
from projects.models import DesiredExpertise
from .models import IdentityForm, User

import django_filters
from django_filters import RangeFilter, CharFilter,MultipleChoiceFilter,ModelMultipleChoiceFilter


class IdentiyFormFilter(django_filters.FilterSet):
    identiy_num = django_filters.CharFilter(lookup_expr='icontains',label="Identity Id")
    
    class Meta:
        model = IdentityForm
        fields =['identiy_num','user','answered','status']
    

class FreelancerFilter(django_filters.FilterSet):
    username = CharFilter(lookup_expr='icontains',label="Username")
    hourly_rate = RangeFilter(lookup_expr='range',label="Hourly Rate")
    skills = ModelMultipleChoiceFilter(queryset=DesiredExpertise.objects.all(),label="Skills",widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model = User
        fields =['skills','hourly_rate','gender']    