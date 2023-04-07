from wsgiref.util import request_uri

import pytz
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.views import APIView
from user.mixins import AccessMixinView, BaseViewMixin
from user.models import SocialLink, User

from .forms import (CookieAgreement, EmailForm, FacebookMessengerForm,
                    FacebookPixelForm, FacebookSocialSettingForm,
                    GoogleAdsenseForm, GoogleAnalyticsForm,
                    GoogleRecaptchaForm, GoogleSocialSettingForm,
                    LinkdinSocialSettingForm, LocalizationSettingForm,
                    PaymentForm, SEOForm, SiteAddressForm, SiteBasicForm,
                    SocialLinkSettingForm, SocialSettingForm,
                    TwitterSocialSettingForm)
from .models import (EmailSetting, LocalizationSetting, OtherSetting,
                     PaymentSetting, SEOSetting, SiteSetting,
                     ExtendedSocialSetting)


class SiteSettingsView(AccessMixinView, BaseViewMixin):
    only_role = "Admin"

    def get(self, request):
        site = SiteSetting.load()
        form2 = SiteAddressForm(instance=site)
        context = {'form2': form2, "site": site}
        return render(request, "sitesettings/sitesettings.html", context)

    def post(self, request):
        site = SiteSetting.load()
        form2 = SiteAddressForm(request.POST, instance=site)

        if "basic_form" in request.POST:
            logo = request.FILES.get("logo")
            favicon = request.FILES.get("favicon")
            if logo:
                site.logo_image = logo
            if favicon:
                site.favicon = favicon
            site.site_name = request.POST.get("site_name")
            site.save()
            site = SiteSetting.load()
            form2 = SiteAddressForm(instance=site)
            context = {'form2': form2, "site": site}
            messages.success(
                request, f"SiteSetting was successfully updated !")
            return render(request, "sitesettings/sitesettings.html", context)

        site = SiteSetting.load()
        if "address_form" in request.POST:
            if form2.is_valid():
                form2.save()
                messages.success(
                    request, f"SiteSetting was successfully updated !")
                site = SiteSetting.load()
            else:
                messages.error(request, f"{form2.errors}")
        context = {'form2': form2, "site": site}
        return render(request, "sitesettings/sitesettings.html", context)


class LocalizationsView(AccessMixinView, BaseViewMixin):
    only_role = "Admin"

    def get(self, request):
        timezones = pytz.all_timezones
        localization = LocalizationSetting.load()
        context = {'localization': localization, 'timezones': timezones}
        return render(request, "sitesettings/localization_details.html", context)

    def post(self, request):
        timezones = pytz.all_timezones
        localization = LocalizationSetting.load()
        form = LocalizationSettingForm(request.POST, instance=localization)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Localization was successfully updated !")
        else:
            messages.error(request, f"{form.errors}")
        context = {'from': form, 'localization': localization,
                   'timezones': timezones}
        return render(request, "sitesettings/localization_details.html", context)


class PaymentSettingsView(AccessMixinView, BaseViewMixin):
    only_role = "Admin"

    def get(self, request):
        pay = PaymentSetting.load()
        form2 = PaymentForm(instance=pay)
        context = {'form2': form2, "pay": pay}
        return render(request, "sitesettings/payment_settings.html", context)

    def post(self, request):
        pay = PaymentSetting.load()
        form2 = PaymentForm(request.POST, instance=pay)

        if "payment_form" in request.POST:
            if form2.is_valid():
                form2.save()
                messages.success(
                    request, f"Payment Setting was successfully updated !")
            else:
                messages.error(request, f"{form2.errors}")
        pay = PaymentSetting.load()
        context = {'form2': form2, "pay": pay}
        return render(request, "sitesettings/payment_settings.html", context)


class EmailSettingsView(AccessMixinView, BaseViewMixin):
    only_role = "Admin"

    def get(self, request):
        email = EmailSetting.load()
        form2 = EmailForm(instance=email)
        context = {'form2': form2, "email": email}
        return render(request, "sitesettings/email_settings.html", context)

    def post(self, request):
        email = EmailSetting.load()
        form2 = EmailForm(request.POST, instance=email)

        if "email_form" in request.POST:
            if form2.is_valid():
                form2.save()
                messages.success(
                    request, f"Email Setting was successfully updated !")
            else:
                messages.error(request, f"{form2.errors}")
        email = EmailSetting.load()
        context = {'form2': form2, "email": email}
        return render(request, "sitesettings/email_settings.html", context)


class SocialSettingsView(AccessMixinView, BaseViewMixin):
    only_role = "Admin"

    def get(self, request):
        try:
            facebookData = ExtendedSocialSetting.facebook_fetch()
        except:
            facebookData = None
        try:
            googleData = ExtendedSocialSetting.google_fetch()
        except:
            googleData = None
        try:
            twitterData = ExtendedSocialSetting.twitter_fetch()
        except:
            twitterData = None
        try:
            linkdinData = ExtendedSocialSetting.linkdin_fetch()
        except:
            linkdinData = None
        context = {
            'facebookData': facebookData,
            'googleData': googleData,
            'twitterData': twitterData,
            'linkdinData': linkdinData
        }

        # socialSetting = SocialSetting.google_load()
        return render(request, "sitesettings/social_settings.html", context)

    def post(self, request):

        if 'google_form' in request.POST:
            print(request.POST,' post data')
            google_data = ExtendedSocialSetting.google_load()
            form = GoogleSocialSettingForm(request.POST, instance=google_data)
            print(form,'form data')
            if form.is_valid():
                mode_value = False
                if 'mode' in request.POST:
                    mode_value = True
                google_data.provider = 'google'
                google_data.is_active = mode_value
                google_data.client_id = request.POST['client_id']
                google_data.secret = request.POST['secret']
                google_data.name = request.POST['name']
                google_data.sites.add(1)
                google_data.save()
                messages.success(
                    request, f"Google Credentials was successfully updated !")
            else:
                messages.error(request, f"{form.errors}")

            try:
                facebookData = ExtendedSocialSetting.facebook_fetch()
            except:
                facebookData = None
            try:
                googleData = ExtendedSocialSetting.google_fetch()
            except:
                googleData = None
            try:
                twitterData = ExtendedSocialSetting.twitter_fetch()
            except:
                twitterData = None
            try:
                linkdinData = ExtendedSocialSetting.linkdin_fetch()
            except:
                linkdinData = None
            context = {
                'facebookData': facebookData,
                'googleData': googleData,
                'twitterData': twitterData,
                'linkdinData': linkdinData
            }
            return render(request, "sitesettings/social_settings.html", context)
        elif 'facebook_form' in request.POST:
            facebook_data = ExtendedSocialSetting.facebook_load()
            form = FacebookSocialSettingForm(
                request.POST, instance=facebook_data)
            if form.is_valid():
                mode_value = False
                if 'mode' in request.POST:
                    mode_value = True
                facebook_data.is_active = mode_value
                facebook_data.provider = 'facebook'
                facebook_data.client_id = request.POST['client_id']
                facebook_data.secret = request.POST['secret']
                facebook_data.sites.add(1)
                facebook_data.save()
                messages.success(
                    request, f"Facebook Credentials was successfully updated !")
            else:
                messages.error(request, f"{form.errors}")

            try:
                facebookData = ExtendedSocialSetting.facebook_fetch()
            except:
                facebookData = None
            try:
                googleData = ExtendedSocialSetting.google_fetch()
            except:
                googleData = None
            try:
                twitterData = ExtendedSocialSetting.twitter_fetch()
            except:
                twitterData = None
            try:
                linkdinData = ExtendedSocialSetting.linkdin_fetch()
            except:
                linkdinData = None
            context = {
                'facebookData': facebookData,
                'googleData': googleData,
                'twitterData': twitterData,
                'linkdinData': linkdinData
            }
            return render(request, "sitesettings/social_settings.html", context)
        elif 'twitter_form' in request.POST:
            twitter_data = ExtendedSocialSetting.twitter_load()
            form = FacebookSocialSettingForm(
                request.POST, instance=twitter_data)
            if form.is_valid():
                mode_value = False
                if 'mode' in request.POST:
                    mode_value = True
                twitter_data.is_active= mode_value
                twitter_data.provider = 'twitter'
                twitter_data.client_id = request.POST['client_id']
                twitter_data.secret = request.POST['secret']
                twitter_data.sites.add(1)
                twitter_data.save()
                messages.success(
                    request, f"Twitter Credentials was successfully updated !")
            else:
                messages.error(request, f"{form.errors}")

            try:
                facebookData = ExtendedSocialSetting.facebook_fetch()
            except:
                facebookData = None
            try:
                googleData = ExtendedSocialSetting.google_fetch()
            except:
                googleData = None
            try:
                twitterData = ExtendedSocialSetting.twitter_fetch()
            except:
                twitterData = None
            try:
                linkdinData = ExtendedSocialSetting.linkdin_fetch()
            except:
                linkdinData = None
            context = {
                'facebookData': facebookData,
                'googleData': googleData,
                'twitterData': twitterData,
                'linkdinData': linkdinData
            }
            return render(request, "sitesettings/social_settings.html", context)
        elif 'linkdin_form' in request.POST:
            print('in linkeditn')
            linkedin_data = ExtendedSocialSetting.linkdin_load()
            form = LinkdinSocialSettingForm(
                request.POST, instance=linkedin_data)
            if form.is_valid():
                mode_value = False
                if 'mode' in request.POST:
                    mode_value = True
                linkedin_data.is_active = mode_value
                linkedin_data.provider = 'linkedin'
                linkedin_data.client_id = request.POST['client_id']
                linkedin_data.name = request.POST['name']
                linkedin_data.secret = request.POST['secret']
                linkedin_data.save()
                linkedin_data.sites.add(1)
                messages.success(
                    request, f"Linkdin Credentials was successfully updated !")
            else:
                messages.error(request, f"{form.errors}")

            try:
                facebookData = ExtendedSocialSetting.facebook_fetch()
            except:
                facebookData = None
            try:
                googleData = ExtendedSocialSetting.google_fetch()
            except:
                googleData = None
            try:
                twitterData = ExtendedSocialSetting.twitter_fetch()
            except:
                twitterData = None
            try:
                linkdinData = ExtendedSocialSetting.linkdin_fetch()
            except:
                linkdinData = None
            context = {
                'facebookData': facebookData,
                'googleData': googleData,
                'twitterData': twitterData,
                'linkdinData': linkdinData
            }
            return render(request, "sitesettings/social_settings.html", context)
        try:
            facebookData = ExtendedSocialSetting.facebook_fetch()
        except:
            facebookData = None
        try:
            googleData = ExtendedSocialSetting.google_fetch()
        except:
            googleData = None
        try:
            twitterData = ExtendedSocialSetting.twitter_fetch()
        except:
            twitterData = None
        try:
            linkdinData = ExtendedSocialSetting.linkdin_fetch()
        except:
            linkdinData = None
        context = {
            'facebookData': facebookData,
            'googleData': googleData,
            'twitterData': twitterData,
            'linkdinData': linkdinData
        }
        return render(request, "sitesettings/social_settings.html", context)


class SocialLinksView(AccessMixinView, BaseViewMixin):
    only_role = "Admin"

    def get(self, request):
        try:
            linkObject = SocialLink.objects.get(user=request.user)
        except:
            linkObject = None
        context = {'data': linkObject}
        return render(request, "sitesettings/social_links.html", context)

    def post(self, request):
        linkObject, created = SocialLink.objects.get_or_create(
            user=request.user)
        form = SocialLinkSettingForm(request.POST, instance=linkObject)
        if form.is_valid():
            linkObject.facebook = request.POST['facebook']
            linkObject.linkedin = request.POST['linkedin']
            linkObject.twitter = request.POST['twitter']
            linkObject.save()
            messages.success(
                request, f"Social link setting was successfully updated !")
        else:
            messages.success(request, f"{form.errors}")
        linkObject = SocialLink.objects.get(user=request.user)
        context = {'data': linkObject}
        return render(request, "sitesettings/social_links.html", context)


class SEOSettingsView(AccessMixinView, BaseViewMixin):
    only_role = "Admin"

    def get(self, request):
        seo = SEOSetting.load()
        form3 = SEOForm(instance=seo)
        context = {'form3': form3, "seo": seo}
        return render(request, "sitesettings/seo_settings.html", context)

    def post(self, request):
        seo = SEOSetting.load()
        form3 = SEOForm(request.POST, instance=seo)

        if "seo_form" in request.POST:
            if form3.is_valid():
                form3.save()
                messages.success(request, f"seo was successfully updated !")
            else:
                messages.error(request, f"{form3.errors}")
        seo = SEOSetting.load()
        context = {'form3': form3, "seo": seo}
        return render(request, "sitesettings/seo_settings.html", context)


class OtherSettingsView(AccessMixinView, BaseViewMixin):
    only_role = "Admin"

    def get(self, request):
        try:
            googleAnalytics = OtherSetting.google_analytics_fetch()
        except:
            googleAnalytics = None
        try:
            googleAdsense = OtherSetting.google_adsense_fetch()
        except:
            googleAdsense = None
        try:
            facebookMessenger = OtherSetting.facebook_messenger_fetch()
        except:
            facebookMessenger = None
        try:
            facebookPixel = OtherSetting.facebook_pixel_fetch()
        except:
            facebookPixel = None
        try:
            googleRecaptcha = OtherSetting.google_rechaptcha_fetch()
        except:
            googleRecaptcha = None
        try:
            cookieAgreement = OtherSetting.cookie_agreement_fetch()
        except:
            cookieAgreement = None
        context = {
            'googleAnalytics': googleAnalytics, 'googleAdsense': googleAdsense,
            'facebookMessenger': facebookMessenger, 'facebookPixel': facebookPixel,
            'googleRecaptcha': googleRecaptcha, 'cookieAgreement': cookieAgreement
        }
        return render(request, "sitesettings/others_settings.html", context)

    def post(self, request):
        if 'google_analytics' in request.POST:
            googleAnalytics = OtherSetting.google_analytics_load()
            form = GoogleAnalyticsForm(request.POST, instance=googleAnalytics)
            if form.is_valid():
                googleAnalytics.descriptions = request.POST['descriptions']
                googleAnalytics.media = "Google_Analytics"
                mode_value = 'Inactive'
                if 'mode' in request.POST:
                    mode_value = 'Active'
                googleAnalytics.mode = mode_value
                googleAnalytics.save()
                messages.success(
                    request, f"Google analytics setting was successfully updated !")
            else:
                messages.success(request, f"{form.errors}")
            try:
                googleAnalytics = OtherSetting.google_analytics_fetch()
            except:
                googleAnalytics = None
            try:
                googleAdsense = OtherSetting.google_adsense_fetch()
            except:
                googleAdsense = None
            try:
                facebookMessenger = OtherSetting.facebook_messenger_fetch()
            except:
                facebookMessenger = None
            try:
                facebookPixel = OtherSetting.facebook_pixel_fetch()
            except:
                facebookPixel = None
            try:
                googleRecaptcha = OtherSetting.google_rechaptcha_fetch()
            except:
                googleRecaptcha = None
            try:
                cookieAgreement = OtherSetting.cookie_agreement_fetch()
            except:
                cookieAgreement = None
            context = {
                'googleAnalytics': googleAnalytics, 'googleAdsense': googleAdsense,
                'facebookMessenger': facebookMessenger, 'facebookPixel': facebookPixel,
                'googleRecaptcha': googleRecaptcha, 'cookieAgreement': cookieAgreement
            }
            return render(request, "sitesettings/others_settings.html", context)
        elif 'google_adsense' in request.POST:
            googleAdsense = OtherSetting.google_adsense_load()
            form = GoogleAdsenseForm(request.POST, instance=googleAdsense)
            if form.is_valid():
                googleAdsense.descriptions = request.POST['descriptions']
                googleAdsense.media = "Google_Adsense"
                mode_value = 'Inactive'
                if 'mode' in request.POST:
                    mode_value = 'Active'
                googleAdsense.mode = mode_value
                googleAdsense.save()
                messages.success(
                    request, f"Google Adsense setting was successfully updated !")
            else:
                messages.success(request, f"{form.errors}")
            try:
                googleAnalytics = OtherSetting.google_analytics_fetch()
            except:
                googleAnalytics = None
            try:
                googleAdsense = OtherSetting.google_adsense_fetch()
            except:
                googleAdsense = None
            try:
                facebookMessenger = OtherSetting.facebook_messenger_fetch()
            except:
                facebookMessenger = None
            try:
                facebookPixel = OtherSetting.facebook_pixel_fetch()
            except:
                facebookPixel = None
            try:
                googleRecaptcha = OtherSetting.google_rechaptcha_fetch()
            except:
                googleRecaptcha = None
            try:
                cookieAgreement = OtherSetting.cookie_agreement_fetch()
            except:
                cookieAgreement = None
            context = {
                'googleAnalytics': googleAnalytics, 'googleAdsense': googleAdsense,
                'facebookMessenger': facebookMessenger, 'facebookPixel': facebookPixel,
                'googleRecaptcha': googleRecaptcha, 'cookieAgreement': cookieAgreement
            }
            return render(request, "sitesettings/others_settings.html", context)
        elif 'facebook_messenger' in request.POST:
            facebookMessenger = OtherSetting.facebook_messenger_load()
            form = FacebookMessengerForm(
                request.POST, instance=facebookMessenger)
            if form.is_valid():
                facebookMessenger.descriptions = request.POST['descriptions']
                facebookMessenger.media = "Facebook_Messenger"
                mode_value = 'Inactive'
                if 'mode' in request.POST:
                    mode_value = 'Active'
                facebookMessenger.mode = mode_value
                facebookMessenger.save()
                messages.success(
                    request, f"Facebook Messenger setting was successfully updated !")
            else:
                messages.success(request, f"{form.errors}")
            try:
                googleAnalytics = OtherSetting.google_analytics_fetch()
            except:
                googleAnalytics = None
            try:
                googleAdsense = OtherSetting.google_adsense_fetch()
            except:
                googleAdsense = None
            try:
                facebookMessenger = OtherSetting.facebook_messenger_fetch()
            except:
                facebookMessenger = None
            try:
                facebookPixel = OtherSetting.facebook_pixel_fetch()
            except:
                facebookPixel = None
            try:
                googleRecaptcha = OtherSetting.google_rechaptcha_fetch()
            except:
                googleRecaptcha = None
            try:
                cookieAgreement = OtherSetting.cookie_agreement_fetch()
            except:
                cookieAgreement = None
            context = {
                'googleAnalytics': googleAnalytics, 'googleAdsense': googleAdsense,
                'facebookMessenger': facebookMessenger, 'facebookPixel': facebookPixel,
                'googleRecaptcha': googleRecaptcha, 'cookieAgreement': cookieAgreement
            }
            return render(request, "sitesettings/others_settings.html", context)
        elif 'facebook_pixel' in request.POST:
            facebookPixel = OtherSetting.facebook_pixel_load()
            form = FacebookPixelForm(request.POST, instance=facebookPixel)
            if form.is_valid():
                facebookPixel.descriptions = request.POST['descriptions']
                facebookPixel.media = "Facebook_Pixel"
                mode_value = 'Inactive'
                if 'mode' in request.POST:
                    mode_value = 'Active'
                facebookPixel.mode = mode_value
                facebookPixel.save()
                messages.success(
                    request, f"Facebook pixel setting was successfully updated !")
            else:
                messages.success(request, f"{form.errors}")
            try:
                googleAnalytics = OtherSetting.google_analytics_fetch()
            except:
                googleAnalytics = None
            try:
                googleAdsense = OtherSetting.google_adsense_fetch()
            except:
                googleAdsense = None
            try:
                facebookMessenger = OtherSetting.facebook_messenger_fetch()
            except:
                facebookMessenger = None
            try:
                facebookPixel = OtherSetting.facebook_pixel_fetch()
            except:
                facebookPixel = None
            try:
                googleRecaptcha = OtherSetting.google_rechaptcha_fetch()
            except:
                googleRecaptcha = None
            try:
                cookieAgreement = OtherSetting.cookie_agreement_fetch()
            except:
                cookieAgreement = None
            context = {
                'googleAnalytics': googleAnalytics, 'googleAdsense': googleAdsense,
                'facebookMessenger': facebookMessenger, 'facebookPixel': facebookPixel,
                'googleRecaptcha': googleRecaptcha, 'cookieAgreement': cookieAgreement
            }
            return render(request, "sitesettings/others_settings.html", context)

        elif 'google_rechaptcha' in request.POST:
            googleRechaptcha = OtherSetting.google_rechaptcha_load()
            form = GoogleRecaptchaForm(request.POST, instance=googleRechaptcha)
            if form.is_valid():
                googleRechaptcha.site_key = request.POST['site_key']
                googleRechaptcha.media = "Google_Recaptcha"
                googleRechaptcha.secret_key = request.POST['secret_key']
                mode_value = 'Inactive'
                if 'mode' in request.POST:
                    mode_value = 'Active'
                googleRechaptcha.mode = mode_value
                googleRechaptcha.save()
                messages.success(
                    request, f"Google rechaptcha setting was successfully updated !")
            else:
                messages.success(request, f"{form.errors}")
            try:
                googleAnalytics = OtherSetting.google_analytics_fetch()
            except:
                googleAnalytics = None
            try:
                googleAdsense = OtherSetting.google_adsense_fetch()
            except:
                googleAdsense = None
            try:
                facebookMessenger = OtherSetting.facebook_messenger_fetch()
            except:
                facebookMessenger = None
            try:
                facebookPixel = OtherSetting.facebook_pixel_fetch()
            except:
                facebookPixel = None
            try:
                googleRecaptcha = OtherSetting.google_rechaptcha_fetch()
            except:
                googleRecaptcha = None
            try:
                cookieAgreement = OtherSetting.cookie_agreement_fetch()
            except:
                cookieAgreement = None
            context = {
                'googleAnalytics': googleAnalytics, 'googleAdsense': googleAdsense,
                'facebookMessenger': facebookMessenger, 'facebookPixel': facebookPixel,
                'googleRecaptcha': googleRecaptcha, 'cookieAgreement': cookieAgreement
            }
            return render(request, "sitesettings/others_settings.html", context)

        elif 'cookie_aggrement' in request.POST:
            cookieAgreement = OtherSetting.cookie_agreement_load()
            form = CookieAgreement(request.POST, instance=cookieAgreement)
            if form.is_valid():
                cookieAgreement.descriptions = request.POST['descriptions']
                cookieAgreement.media = "Cookies_Agreement"
                mode_value = 'Inactive'
                if 'mode' in request.POST:
                    mode_value = 'Active'
                cookieAgreement.mode = mode_value
                cookieAgreement.save()
                messages.success(
                    request, f"Cookie agreement setting was successfully updated !")
            else:
                messages.success(request, f"{form.errors}")
            try:
                googleAnalytics = OtherSetting.google_analytics_fetch()
            except:
                googleAnalytics = None
            try:
                googleAdsense = OtherSetting.google_adsense_fetch()
            except:
                googleAdsense = None
            try:
                facebookMessenger = OtherSetting.facebook_messenger_fetch()
            except:
                facebookMessenger = None
            try:
                facebookPixel = OtherSetting.facebook_pixel_fetch()
            except:
                facebookPixel = None
            try:
                googleRecaptcha = OtherSetting.google_rechaptcha_fetch()
            except:
                googleRecaptcha = None
            try:
                cookieAgreement = OtherSetting.cookie_agreement_fetch()
            except:
                cookieAgreement = None
            context = {
                'googleAnalytics': googleAnalytics, 'googleAdsense': googleAdsense,
                'facebookMessenger': facebookMessenger, 'facebookPixel': facebookPixel,
                'googleRecaptcha': googleRecaptcha, 'cookieAgreement': cookieAgreement
            }
            return render(request, "sitesettings/others_settings.html", context)


class RemoveImageAPIView(APIView):
    def post(self, request):
        object = SiteSetting.load()
        if 'logo' in request.data.get('type'):
            object.logo_image = None
        elif 'favicon' in request.data.get('type'):
            object.favicon = None
        object.save()
        return JsonResponse({'message': 'success'})
