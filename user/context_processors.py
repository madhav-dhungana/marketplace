from django.contrib.auth.models import *

from sitesettings.models import SiteSetting

def get_siteinfo(request):
    site = SiteSetting.load()
    context = {"site":site,"check_arrs":["Project","InviteModel"]}
    if request.user.is_authenticated:
        unread_notification = request.user.notification_to.filter(user_has_seen=False).count()
        context["unread_notification"]=unread_notification
        if unread_notification >0:
            context["latest_unread_notification"]=request.user.notification_to.filter(user_has_seen=False)[:4]
    return context

def get_full_domain(request):
    return {"get_full_domain":request.scheme +"://"+ request.get_host()}