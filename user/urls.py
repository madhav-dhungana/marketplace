
from django.urls import path

from user.view.admin_view import RoleSettingsView, PermissionSettingsView, ReportsView, InvoiceView, PermissionStatusUpdateAPIView
from .view.views import *
from projects.freelancer_views import WeekdayAvailabilty

urlpatterns = [
   path('choose-type/',ChooseUserType.as_view(), name='ChooseUserType'), #don't change url path (used in middleware to prevent infinite looping)
   path('register/',RegisterView.as_view(), name='register'),
   path('login/',LoginView.as_view(), name='login'),
   path('logout/',logout, name='logout'),
   path('forgot-password/',ForgotPasswordPage.as_view(), name='forgot_password_page'),
   path('email-activated/',EmailActivatedView.as_view(), name='email_activated_page'),
   path('activate-email/<uidb64>/<token>/',activate_email, name='activate_email'),
   path('dashboard/',Dashboard.as_view(), name='dashboard'),
   path('role-settings/',RoleSettingsView.as_view(), name='role_settings'),
   path('reports/',ReportsView.as_view(), name='reports'),
   path('view-invoice/',InvoiceView.as_view(), name='view_invoice'),
   path('permission-settings/<int:role_id>/',PermissionSettingsView.as_view(), name='permission_settings'),
   path('permission-status-update', PermissionStatusUpdateAPIView.as_view(), name='permission-status-update'),
   path('change-password/',ChangePasswordView.as_view(), name='change_password'),
   path('delete-account/',DeleteAccountView.as_view(), name='delete_account'),
   path('profile-settings/',ProfileSettings.as_view(), name='profile_settings'),
   path('favourites/',FavouriteView.as_view(), name='favourite'),
   path('reviews/',ReviewView.as_view(), name='reviews'),
   path('verify-identity/',VerifyIdentityView.as_view(), name='verify_identity'),
   path('invite-list/',InviteList.as_view(), name='invite_list'),
   path('user-invite/',InviteUserView.as_view(), name='invite_user_page'),
   path('freelancer-list/',FreelancerList.as_view(), name='freelancer_list'),
   # path('search-freelancer/',SearchFreelancer.as_view(), name='search_freelancer'),
   path('set-availability/',WeekdayAvailabilty.as_view(), name='set_availability'),
   path('user-detail/<int:id>/',FreelancerDetail.as_view(), name='user_detail'),
   path('fav-freelancer/<int:id>/',FavouriteFreelancer.as_view(), name='fav_freelancer'),

   path('privacy-policy/', privacyPolicy, name = 'privacy-policy'),
   path('user-aggrement/', userAggrement, name = 'user-agreement'),
   path('cookie-policy/', cookiePolicy, name = 'cookie-policy'),


   path('follow/now/<int:id>/', follow, name='follow_user'),
   path('freelancer-portfolio/', PortfolioView.as_view(), name='freelancer_portfolio')


   
]
