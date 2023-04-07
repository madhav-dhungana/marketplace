from .models import DesiredExpertise

def give_or_create_skills(queryset):
    return [DesiredExpertise.objects.get_or_create(skill_name=i)[0] for i in queryset.split(',')]

def firstError(form):
    return list(form.error_messages.values())[0]