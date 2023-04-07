from django import forms
from .models import Membership


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        autocomplete_fields = ("plans",)
        exclude = ("slug",)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slogan': forms.TextInput(attrs={'class': 'form-control'}),
            'membership_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_period': forms.Select(attrs={'class': 'form-control'}),
            'plans': forms.SelectMultiple(attrs={'class': 'form-control', 'style':'height:auto; width:auto'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'check'}),
        }
    

    # def save(self, validated_data):
    #     data = Membership(**validated_data)
    #     data.save()
    #     return data

    # def __init__(self, *args, **kwargs):
    #     super(__class__, self).__init__(*args, **kwargs)
    #     for i in self.fields.values():
    #         print(i)
            # if 'CharField' in i.name:
            #     self.fields[i].widget.attrs.update({'class': 'form-control'})