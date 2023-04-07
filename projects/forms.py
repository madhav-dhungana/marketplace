from dataclasses import fields
from .models import InviteModel, Project, Proposal
from django import forms
from ckeditor.widgets import CKEditorWidget
from datetime import date, datetime


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['detail'].label = 'Write Description of Projects'
        self.fields['detail'].required = True

    end_date = forms.CharField(label='Estimated End Date', required=False,
                               widget=forms.TextInput(attrs={'type': 'date'}))
    expires_on = forms.CharField(
        label='Project Expires On', required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    start_date = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'date'}))
    start_time = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'time'}))
    end_time = forms.CharField(widget=forms.TextInput(attrs={'type': 'time'}))
    experience_needed = forms.IntegerField(
        label='Experience Needed (in years)', required=False)
    price = forms.IntegerField(required=True)

    class Meta:
        model = Project
        fields = ('title', 'pricing_type', 'category',
                  'start_date', 'end_date',
                  'start_time', 'end_time',
                  'location', 'address',
                  'expires_on', 'price',
                  'status',
                  'experience_needed', 'detail'
                  )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        expires_on = cleaned_data.get("expires_on")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        msg = 'Start date is after end date !'
        today = date.today()
        if start_date > end_date:
            self.add_error('start_date', msg)
            self.add_error('end_date', msg)
        if (expires_on < start_date) or (expires_on > end_date):
            self.add_error(
                'expires_on', 'Expire date must be between Start Date and End Date')

        if start_time > end_time:
            self.add_error(
                'start_time', 'Start time should be less than end time')

        detail = cleaned_data.get('detail')
        if not detail:
            self.add_error(None, 'Description Required')


class ProposalForm(forms.ModelForm):
    detail = forms.CharField(label="Cover letter", widget=CKEditorWidget())

    class Meta:
        model = Proposal
        exclude = ('user', 'project')


class InviteForm(forms.ModelForm):
    detail = forms.CharField(widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = user.my_projects.filter(
            status="Active")

    class Meta:
        model = InviteModel
        fields = ["project", 'estimated_price', 'estimated_duration', 'detail']
