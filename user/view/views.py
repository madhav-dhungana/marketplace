from itertools import chain

from allauth.socialaccount.models import SocialAccount
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import (Http404, HttpResponse, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import RedirectView
from projects.forms import InviteForm
from projects.models import DesiredExpertise, Project, ProjectCategory
from projects.utils import firstError
from user.api.mixins import SendEmailMixin
from user.api.tokens import account_activation_token

from ..filters import FreelancerFilter
from ..forms import (CustomUserChangeForm, CustomUserCreationForm,
                     IdentiyuserForm, SocialLinkForm)
from ..mixins import (AccessMixinView, BaseViewMixin, NonAdminView,
                      PaginateView, UnAuthorizedView)
from ..models import (Awards, Education, Experience, Followers, IdentityForm,
                      Languages, Portfolio, PortfolioDocument, SocialLink,
                      User, UserDeleteRecords)
from sitesettings.models import ExtendedSocialSetting


class ChooseUserType(View):
    def get(self, request):
        if not request.user.is_authenticated or request.user.role:
            return redirect("/")
        return render(request, "user/choose_type.html")

    def post(self, request):
        if "freelancer" in request.POST:
            request.user.role = "Freelancer"
            request.user.save()

        if "employer" in request.POST:
            request.user.role = "Employer"
            request.user.save()
        return redirect("/")


class Dashboard(BaseViewMixin):
    def get(self, request):
        user = request.user
        if user.role == "Employer":
            my_projects = request.user.my_projects.all()
            posted_projects = my_projects.count()
            ongoing_projects = my_projects.filter(status="ON").count()
            completed_projects = my_projects.filter(status="COM").count()
            active_projects = my_projects.filter(status="Active").count()
            pending_projects = my_projects.filter(status="PEN").count()
            cancelled_projects = my_projects.filter(status="CAN").count()
            activities = user.activities.all()[:5]
            project_chart_data = [
                active_projects,
                pending_projects,
                ongoing_projects,
                completed_projects,
                cancelled_projects,
            ]
            context = {
                "posted_projects": posted_projects,
                "ongoing_projects": ongoing_projects,
                "completed_projects": completed_projects,
                "recent_projects": my_projects[:3],
                "project_chart_data": project_chart_data,
                "activities": activities,
            }
            return render(request, "user/employer/dashboard.html", context)

        elif user.role == "Freelancer":
            my_projects = request.user.hired_projects.all()
            reviews_count = request.user.reviews_got.count()
            on_projects = my_projects.filter(status="ON")
            ongoing_projects = on_projects.count()
            comp_projects = my_projects.filter(status="COM")
            cancelled_projects = my_projects.filter(status="CAN").count()
            completed_projects = comp_projects.count()
            project_chart_data = [
                ongoing_projects,
                completed_projects,
                cancelled_projects,
            ]
            reviews = request.user.reviews_got.all()[:3]
            context = {
                "on_projects": on_projects,
                "reviews_count": reviews_count,
                "comp_projects": comp_projects,
                "ongoing_projects": ongoing_projects,
                "completed_projects": completed_projects,
                "project_chart_data": project_chart_data,
                "reviews": reviews,
            }
            return render(request, "user/freelancer/dashboard.html", context)
        else:
            return redirect("admin_dashboard")


class RegisterView(UnAuthorizedView, SendEmailMixin):
    form_class = CustomUserCreationForm()
    email_template_name = "email/activation_email.html"
    mail_subject = "Activate Your Account "

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('admin_dashboard')
        form = self.form_class
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
            'linkdinData': linkdinData,
            'form': form,
        }
        return render(request, "user/register.html", context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if "freelancer" in request.POST:
                user.role = "Freelancer"
            else:
                user.role = "Employer"
            user.is_active = False
            user.save()

            email_data = {
                "domain": request.META["HTTP_HOST"],
                "uid": urlsafe_base64_encode(force_bytes(user.id)),
                "token": account_activation_token.make_token(user),
                "site_name": "Batuwa",
            }
            self.send_email_temp(email_data, request.POST.get("email"))
            messages.success(
                request, f"{str(user)} was successfully registerd !")
            return redirect("login")
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
            'linkdinData': linkdinData,
            'form': form,
        }
        return render(request, "user/register.html", context)


def activate_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("email_activated_page")
    else:
        return HttpResponse("Activation link is invalid!")


class EmailActivatedView(View):
    template_name = "user/activation_done.html"

    def get(self, request):
        return render(request, self.template_name)


class LoginView(UnAuthorizedView):
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
            'linkdinData': linkdinData,
        }
        return render(request, "user/login.html", context)

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        remember_me = request.POST.get("remember_me")
        check_user = User.objects.filter(email=email).first()
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
            'linkdinData': linkdinData,
        }
        if check_user and not check_user.is_active:
            messages.error(request, "Please verify your email !")
            return render(request, "user/login.html", context)

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email or password")
            return render(request, "user/login.html", context)


def logout(request):
    auth.logout(request)
    return redirect("login")


class ChangePasswordView(BaseViewMixin):
    def get(self, request):
        is_social_account = SocialAccount.objects.filter(
            user=request.user).exists()

        return render(
            request,
            "user/changepassword.html",
            {"is_social_account": is_social_account},
        )

    def post(self, request):
        old_pass = request.POST["old_pass"]
        new_pass = request.POST["new_pass"]
        confirm_pass = request.POST["confirm_pass"]
        is_social_account = SocialAccount.objects.filter(
            user=request.user).exists()

        check_pass = request.user.check_password(old_pass)
        if not check_pass:
            messages.error(request, "Old Password is incorrect !")
            return render(request, "user/changepassword.html")
        if new_pass != confirm_pass:
            messages.error(request, "Password do not match each other !")
            return render(request, "user/changepassword.html")
        request.user.set_password(new_pass)

        request.user.save()
        messages.success(
            request, "Successfully changed your password . You have to login again!"
        )
        return render(request, "user/changepassword.html")


class DeleteAccountView(BaseViewMixin):

    def get(self, request):
        from ..forms import UserDeleteForm
        is_social_account = SocialAccount.objects.filter(
            user=request.user).exists()
        context = {"is_social_account": is_social_account,
                   'form': UserDeleteForm}
        return render(request, "user/delete_account.html", context)

    def post(self, request):
        from ..forms import UserDeleteForm
        form = UserDeleteForm(request.POST)
        old_pass = request.POST.get("password")
        reason = request.POST.get("reason")
        check_pass = request.user.check_password(old_pass)
        if not check_pass:
            messages.error(request, "Your password is incorrect !")
            return render(request, "user/delete_account.html", {'form': form})
        UserDeleteRecords.objects.create(
            email=request.user.email, reason=reason)
        request.user.delete()
        return redirect("register")


class ProfileSettings(BaseViewMixin):
    def get(self, request):
        # admin has their own user settings /edit page
        if request.user.role == "Admin":
            raise Http404
        form = CustomUserChangeForm(instance=request.user)
        try:
            social_links = SocialLink.objects.filter(user=request.user).last()
        except:
            social_links = None
        link_form = SocialLinkForm(instance=social_links)
        is_social_account = SocialAccount.objects.filter(
            user=request.user).exists()
        context = {
            "form": form, "is_social_account": is_social_account, 'link_form': link_form}
        return render(request, "user/profile_settings.html", context)

    def post(self, request):
        form = CustomUserChangeForm(request.POST, instance=request.user)
        try:
            social_links = SocialLink.objects.filter(user=request.user).last()
        except:
            social_links = None
        link_form = SocialLinkForm(request.POST, instance=social_links)
        print(link_form.errors)
        if form.is_valid() and link_form.is_valid():
            print('----')
            f = form.save(commit=False)
            profile_img = request.FILES.get("profile_img")
            banner_img = request.FILES.get("banner_img")
            if profile_img:
                f.avatar = profile_img
            if banner_img:
                f.banner_image = banner_img
            skills = request.POST.getlist("user_skills[]")
            if skills:
                request.user.skills.set(
                    [
                        DesiredExpertise.objects.get_or_create(skill_name=i)[0]
                        for i in skills
                    ]
                )
            awards_name = request.POST.getlist("awards_name[]")
            awards_date = request.POST.getlist("awards_date[]")

            Awards.objects.filter(user=request.user).delete()
            if awards_name and awards_date:
                awards_dict = dict(zip(awards_name, awards_date))
                for title, date in awards_dict.items():
                    Awards.objects.create(
                        user=request.user, title=title, date=date)

            lang = request.POST.getlist("lang[]")
            fluency = request.POST.getlist("fluency[]")
            Languages.objects.filter(user=request.user).delete()
            if lang and fluency:
                lang_dict = dict(zip(lang, fluency))
                for name, fluency in lang_dict.items():
                    Languages.objects.create(
                        user=request.user, name=name, fluency=fluency
                    )
            f.save()
            data = link_form.cleaned_data
            facebook = data.get('facebook')
            linkedin = data.get('linkedin')
            twitter = data.get('twitter')
            if social_links:
                social_links.facebook = facebook
                social_links.linkedin = linkedin
                social_links.twitter = twitter
                social_links.save()
            else:
                SocialLink.objects.create(
                    user=request.user, facebook=facebook, linkedin=linkedin, twitter=twitter)
            messages.success(request, "Your profile is successfully updated !")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        context = {"form": form, "link_form": link_form}
        return render(request, "user/profile_settings.html", context)


class FavouriteView(AccessMixinView):
    only_role = "Employer"

    def get(self, request):
        form = InviteForm(user=request.user)
        context = {"form": form}
        return render(request, "user/fav_batuwa.html", context)


class InviteList(AccessMixinView):
    only_role = "Employer"

    def get(self, request):
        me = request.user
        invites = request.user.invites_sent.all()
        context = {"invites": invites}
        return render(request, "user/employer/invite_list.html", context)


class InviteUserView(AccessMixinView):
    only_role = "Employer"

    def get(self, request):
        form = InviteForm(user=request.user)
        u_id = request.GET.get("invite_user")

        if u_id:
            sent_to = get_object_or_404(User, id=u_id)
            context = {"form": form, "sent_to": sent_to, "u_id": u_id}
        else:
            context = {"form": form}
        return render(request, "user/employer/invite_user.html", context)


class ReviewView(NonAdminView):
    def get(self, request):
        user = request.user
        if user.role == "Employer":
            reviews = user.reviews_given.all()
            return render(request, "user/employer/review.html", {"reviews": reviews})
        if user.role == "Freelancer":
            reviews = user.reviews_got.all()
            return render(request, "user/freelancer/review.html", {"reviews": reviews})


class VerifyIdentityView(BaseViewMixin):
    def get(self, request):
        myform = IdentityForm.objects.filter(user=request.user).first()
        form = IdentiyuserForm(
            instance=myform) if myform else IdentiyuserForm()
        context = {"form": form, "myform": myform}
        return render(request, "user/verify_identity.html", context)

    def post(self, request):
        myform = IdentityForm.objects.filter(user=request.user).first()
        form = (
            IdentiyuserForm(request.POST, instance=myform)
            if myform
            else IdentiyuserForm(request.POST)
        )
        if form.is_valid():
            f = form.save(commit=False)
            document = request.FILES.get("input_file")
            if document:
                f.document = document
            f.user = request.user
            f.save()
            messages.success(
                request,
                "Document Successfully submitted. Please wait until it's reviewed by our team !",
            )
        else:
            messages.error(request, firstError(form))

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class FreelancerList(BaseViewMixin):
    def get(self, request, title=None, *args, **kwargs):
        freelancers = User.objects.filter(role="Freelancer")
        if title:
            freelancers = freelancers.filter(Q(email__icontains=title) | Q(username__icontains=title) | Q(
                display_name__icontains=title) | Q(address__icontains=title) | Q(country__icontains=title))
        searched_users = []
        categories = ProjectCategory.objects.all()
        skills = DesiredExpertise.objects.all()
        location_search, title_search, hourly_max, hourly_min, user_ratings, user_skills = '', '', '', '', '', ''
        if request.GET:
            if request.GET.get("location"):
                location_search = freelancers.filter(
                    address__icontains=request.GET.get("location"))
            if request.GET.get("username"):
                title_search = freelancers.filter(
                    username__icontains=request.GET.get("username"))
            min_hour, max_hour = request.GET.get(
                "hourly_min"), request.GET.get("hourly_max")
            if min_hour and max_hour:
                hourly_min = freelancers.filter(
                    hourly_rate__range=[min_hour, max_hour])
            if request.GET.get("rating"):
                ratings = request.GET.getlist("rating")
                user_ratings = freelancers.filter(
                    user_ratings_floor__in=ratings)
            if request.GET.get("desired_skills"):
                skills = request.GET.get("desired_skills").split(',')
                user_skills = freelancers.filter(skills__skill_name__in=skills)

        qschain = list(chain(location_search, title_search,
                       hourly_max, hourly_min, user_ratings, user_skills))
        res = PaginateView()
        page = self.request.GET.get("page")
        if request.GET:
            response = res.give_paginated_response(page, qschain, 10)
        else:
            response = res.give_paginated_response(page, freelancers, 10)
        context = {
            "page_obj": response,
            "categories": categories,
            "skills": skills,
        }
        if request.GET:
            context.update(
                {"search_q": request.GET,
                 'ratings': ''.join(request.GET.getlist("rating"))}
            )
        return render(request, "user/employer/freelancers.html", context)

    def post(self, request):
        return redirect('freelancer_list')


class SearchFreelancer(BaseViewMixin):
    def get(self, request, *args, **kwargs):
        freelancers = User.objects.filter(role="Freelancer")
        searched_users = []
        categories = ProjectCategory.objects.all()
        skills = DesiredExpertise.objects.all()
        location_search, title_search, hourly_max, hourly_min, user_ratings, user_skills = '', '', '', '', '', ''
        if request.GET:
            print(request.GET)

            if request.GET.get("location"):
                location_search = freelancers.filter(
                    address__icontains=request.GET.get("location"))
            if request.GET.get("username"):
                print('--------------')
                title_search = freelancers.filter(
                    username__icontains=request.GET.get("username"))
                print(title_search)
            min_hour, max_hour = request.GET.get(
                "hourly_min"), request.GET.get("hourly_max")
            if min_hour and max_hour:
                hourly_min = freelancers.filter(
                    hourly_rate__range=[min_hour, max_hour])
            if request.GET.get("rating"):
                ratings = request.GET.getlist("rating")
                user_ratings = freelancers.filter(
                    user_ratings_floor__in=ratings)
            if request.GET.get("desired_skills"):
                skills = request.GET.get("desired_skills").split(',')
                print('skills are ', skills)
                user_skills = freelancers.filter(skills__skill_name__in=skills)

        qschain = list(chain(location_search, title_search,
                       hourly_max, hourly_min, user_ratings, user_skills))
        res = PaginateView()
        page = self.request.GET.get("page")
        if request.GET:
            print(searched_users)
            response = res.give_paginated_response(page, qschain, 10)
        else:
            response = res.give_paginated_response(page, freelancers, 10)
        context = {
            "page_obj": response,
            "categories": categories,
            "skills": skills,
        }
        if request.GET:
            context.update(
                {"search_q": request.GET,
                 'ratings': ''.join(request.GET.getlist("rating"))}
            )
        return render(request, "user/employer/freelancers.html", context)

    def post(self, request):
        return redirect('search_freelancer')


class FreelancerDetail(BaseViewMixin):
    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        portfolios = user.portfolios.all()
        clients = set([i.posted_by for i in user.hired_projects.all()])
        com_projects = user.hired_projects.filter(status="COM").count()
        on_projects = user.hired_projects.filter(status="ON").count()
        reviews = user.reviews_got.all()
        reviews_count = reviews.count()
        follow_status = Followers.get_follow_status(request.user.id, id)
        context = {
            "user": user,
            "portfolios": portfolios,
            "com_projects": com_projects,
            "on_projects": on_projects,
            "no_of_clients": len(clients),
            "reviews": reviews,
            "reviews_count": reviews_count,
            "social_links": SocialLink.objects.filter(user=user).last(),
            "follow_status": follow_status
        }

        return render(request, "user/freelancer/profile_detail.html", context)


class FavouriteFreelancer(BaseViewMixin):
    def post(self, request, id):
        user = request.user
        user_to_add_or_remove = get_object_or_404(User, id=id)
        if user_to_add_or_remove in user.bookmarked_people.all():
            user.bookmarked_people.remove(user_to_add_or_remove)
        else:
            user.bookmarked_people.add(user_to_add_or_remove)
        context = {"user_to_add_or_remove": user_to_add_or_remove}
        return render(request, "projects/htmx/Fav.html", context)


class ForgotPasswordPage(UnAuthorizedView):
    def get(self, request):
        return render(request, "user/forgot_password.html")


def privacyPolicy(request):
    if request.method == 'GET':
        return render(request, 'user/privacy_policy.html')


def userAggrement(request):
    if request.method == 'GET':
        return render(request, 'user/user_aggrement.html')


def cookiePolicy(request):
    if request.method == 'GET':
        return render(request, 'user/cookie_policy.html')


@login_required(login_url='/')
def follow(request, id):
    if request.method == 'GET':
        if not Followers.objects.filter(follow_by=request.user, follow_to_id=id).exists():
            Followers.objects.create(follow_by=request.user, follow_to_id=id)
            return JsonResponse({"status": 201})
        return JsonResponse({"status": 404})


class PortfolioView(AccessMixinView):
    only_role = 'Freelancer'
    template_name = "user/freelancer/freelancer-portfolio.html"

    def get(self, request):
        portfolioData = Portfolio.objects.filter(user=request.user)
        context = {'portfolio': portfolioData}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        if 'update' in request.POST:
            portfolio_id = request.POST.get('portfolio_id', None)
            title = request.POST.get('title', None)
            url = request.POST.get('url', None)
            files = request.FILES.getlist('files')
            portfolioData = Portfolio.objects.get(id=portfolio_id)
            portfolioData.title = title
            portfolioData.url = url
            if files:
                for file in files:
                    document = PortfolioDocument.objects.create(file=file)
                    portfolioData.file.add(document)
                    portfolioData.save()
        elif 'create' in request.POST:
            title = request.POST.get('title', None)
            url = request.POST.get('url', None)
            files = request.FILES.getlist('files')
            portfolioData = Portfolio(
                user = request.user,
                title = title,
                url = url
            )
            portfolioData.save()
            if files:
                first_file = files[0]
                for file in files:
                    document = PortfolioDocument.objects.create(file=file)
                    if file.name == first_file.name:
                        document.is_banner = True
                        document.save()
                    portfolioData.file.add(document)
                    portfolioData.save()
        return redirect('freelancer_portfolio')
