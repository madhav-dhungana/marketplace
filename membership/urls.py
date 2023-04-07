from django.urls import path, re_path, include
from membership import views


urlpatterns = [
    path('', views.MembershipView.as_view(), name='membership_plans'),
    path('membership-plans/', views.AdminMembershipPlans.as_view(),
         name='admin_membership_plans'),
    path('add/', views.AddMembershipPlans.as_view(), name='add_membership_plans'),
    path('update/<int:id>/', views.UpdateMembershipPlans.as_view(), name='update_membership_plans'),
]
