
from django.urls import path
from .views import EmailSettingsView, SiteSettingsView, SocialLinksView, SEOSettingsView, LocalizationsView, PaymentSettingsView, OtherSettingsView, SocialSettingsView, RemoveImageAPIView


urlpatterns = [
   path('site-settings/',SiteSettingsView.as_view(), name='site_settings'),
   path('localizations/',LocalizationsView.as_view(), name='localizations'),
   path('payment-settings/',PaymentSettingsView.as_view(), name='payment_settings'),
   path('email-settings/',EmailSettingsView.as_view(), name='email_settings'),
   path('social-settings/',SocialSettingsView.as_view(), name='social_settings'),
   path('social-links/',SocialLinksView.as_view(), name='social_links'),
   path('seo-settings/',SEOSettingsView.as_view(), name='seo_settings'),
   path('other-settings/',OtherSettingsView.as_view(), name='other_settings'),
   path('site-settings/remove-image/', RemoveImageAPIView.as_view(), name='remove-image')

]