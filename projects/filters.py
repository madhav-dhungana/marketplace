from django.forms import DateInput, NumberInput, TextInput
import django_filters
from django_filters import DateFilter, CharFilter, MultipleChoiceFilter, ModelChoiceFilter, RangeFilter
from user.models import User, Experience
from .models import Project, Reviews, DesiredExpertise
from django import forms
from django.db.models import Q
from django.forms.widgets import HiddenInput


class ProjectFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title',
                       lookup_expr='icontains', label='Title')
    address = CharFilter(field_name='address',
                         lookup_expr='icontains', label='Address')
    start_date = DateFilter(lookup_expr='gte', label='Start Date (greater or equal)',
                            widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Project
        fields = ['price']


class ReviewFilter(django_filters.FilterSet):
    review = CharFilter(field_name='review',
                        lookup_expr='icontains', label='review')

    class Meta:
        model = Reviews
        fields = ['review', 'review_to', 'review_by', 'rating']


class UserFilter(django_filters.FilterSet):
    email = CharFilter(lookup_expr='icontains', label="Email Address")
    username = CharFilter(lookup_expr='icontains', label="Username")

    class Meta:
        model = User
        fields = ['email', 'role', 'hourly_rate', 'gender']


class TravellerFilter(django_filters.FilterSet):
    keyword = CharFilter(method='custom_filter', label='Keyword')
    location = CharFilter(lookup_expr='icontains', label='Location')
    skills = ModelChoiceFilter(queryset=DesiredExpertise.objects.all())
    # experience = RangeFilter(method='experience_filter', label='Experience')
    # category = CharFilter(lookup_expr='icontains', label='Category', field_name='')

    def custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(email__icontains=value) |
            Q(username__icontains=value) |
            Q(title__icontains=vlaue) |
            Q(address__icontains=value) |
            Q(state__icontains=value) |
            Q(country__name__icontains=value) |
            Q(display_name__icontains=value)
        )
    
    class Meta:
        model = User
        fields = ['location', 'skills']

