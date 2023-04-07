from django.contrib import admin
from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
class WeekDayInline(admin.StackedInline):
    model = WeekDayAvailable
    fields = ('name', 'user','available_from','available_to')

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    list_display = ('email', 'is_staff', 'is_active','role')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
          (None, {'fields': ('email', 'password','username','role','avatar','user_ratings','user_ratings_floor','overview','verified','availability','address','state','zipcode','country','skills')}),
        ('Permissions', {'fields': ('is_staff','is_superuser', 'is_active','groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','password1', 'password2', )}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    inlines = (WeekDayInline,)


admin.site.register(User, CustomUserAdmin)


admin.site.register(Languages)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(IdentityForm)
admin.site.register(ActivityLog)
admin.site.register(Awards)
admin.site.register(SocialLink)
admin.site.register(Followers)
admin.site.register(Portfolio)
admin.site.register(PortfolioDocument)
