from django.urls import path, include
from .views import *
from user.api.routers import router

urlpatterns = [
    path('user-register/', RegisterUserAPIView.as_view(),name="register_user_api"),
    path('user-login/', UserLoginApiView.as_view(), name='user_login'),
    path('', include(router.urls)),

    path('all-users/', UsersList.as_view(),name="userlist"),
    path('send-activation-email/', SendActivationEmail.as_view()),
    path('set-weekday-availability/', WeekDayAvailableAPI.as_view(),name="set_weekday_api"),
    path('password-reset/', PasswordResetApiView.as_view(),name="password_reset_api"),
    path('user-detail/<username>/', UserDetailView.as_view(),name="user_detail_api"),
    path('change-password/<int:id>/', PasswordChangeAPIView.as_view(),name="password_change_api"),
    # path('oauth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    # path('oauth/google/', GoogleLogin.as_view(), name='google_login'),
    # path('social-auth/',include('allauth.urls'),name='socialaccount_signup'),
]