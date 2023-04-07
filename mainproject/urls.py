from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import IndexView, SubscribeView
from .oauth import FacebookLogin, GoogleLogin
from user.api.urls import MyTokenObtainPairView


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="batuwa@email.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('main/', admin.site.urls),

    #  path('', RedirectView.as_view(pattern_name='dashboard'),name='redirect'),
    #  path('', RedirectView.as_view(pattern_name='dashboard'),name='redirect'),
    path('', IndexView.as_view(), name='index'),
    path('dashboard/', RedirectView.as_view(pattern_name='dashboard'), name='redirect'),
    path('user/', include('user.urls')),
    path('project/', include('projects.urls')),
    path('membership/', include('membership.urls')),
    path('site/', include('sitesettings.urls')),
    path('admin/', include('user.admin_urls')),
    path('notice/', include('notification.urls')),
    path('accounts/', include('allauth.urls')),
    path('chat/', include('chat.urls')),
    path('payments/', include('payments.urls')),
    path('blog/', include('blog.urls')),
    path('subscribe', SubscribeView.as_view(), name='subscribe'),

    # path('jwt/create/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),


    path('api/projects/', include('projects.api.urls')),
    path('api/user/', include('user.api.urls')),
    path('api/payments/', include('payments.api.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="user/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    path('oauth/facebook/', FacebookLogin.as_view(), name='facebook_oauth'),
    path('oauth/google/', GoogleLogin.as_view(), name='google_oauth'),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]


urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
                                               cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
                                             cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
