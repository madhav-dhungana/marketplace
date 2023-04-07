from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages, auth
from user.mixins import AccessMixinView, BaseViewMixin, PaginateView
from django.views.generic import ListView
from membership.models import Membership, Plan, Subscription, UserMembership
from datetime import timedelta, datetime
from projects.models import ProjectCategory
from .forms import MembershipForm


class MembershipView(View):
    template_name = "membership-plans.html"

    def get(self, request):
        # TODO: Create user subscription
        # if 'membership' in request.GET:
        #     membership = Membership.objects.get(slug=request.GET.get('membership'))
        #     userMembership, created = UserMembership.objects.get_or_create(
        #         user=request.user, membership=userMembership)
        #     if created:
        #         if userMembership.duration_period =
        #         subscription = Subscription.objects.create(user_membership=membership, expires_in=datetime.today() + timedelta())
        membership = Membership.objects.all()
        if request.user.is_authenticated:
            try:
                userMembership = UserMembership.objects.get(user=request.user)
            except:
                userMembership = None
        else:
            userMembership = None
        context = {'membership': membership, 'userMembership': userMembership}
        return render(request, self.template_name, context)


class AdminMembershipPlans(AccessMixinView):
    only_role = 'Admin'
    template_name = "admin-membership.html"

    def get(self, request):
        membership = Membership.objects.all()
        name = request.GET.get('membership')

        if name:
            membership = membership.filter(name__icontains=name)
        res = PaginateView()
        page = self.request.GET.get("page")
        response = res.give_paginated_response(page, membership, 10)
        context = {"page_obj": response, 'membership': membership}
        return render(request, self.template_name, context)

    def post(self, request):
        if 'delete_membership' in request.POST:
            Membership.objects.get(id=request.POST.get('membership')).delete()
            messages.add_message(request, 1, 'Successfully Deleted')
        else:
            ...
        membership = Membership.objects.all()
        res = PaginateView()
        page = self.request.GET.get("page")
        response = res.give_paginated_response(page, membership, 10)
        context = {"page_obj": response, 'membership': membership}
        return render(request, self.template_name, context)


class AddMembershipPlans(View):
    template_name = "add-membership.html"

    def get(self, request):
        form = MembershipForm
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = MembershipForm(data=request.POST)
        context = {'form': form}
        if form.is_valid():
            form = form.save()
            return redirect('update_membership_plans', form.id)
        else:
            form = MembershipForm()
            context = {'form': form}
            return render(request, self.template_name, context)


class UpdateMembershipPlans(AccessMixinView):
    only_role = 'Admin'
    template_name = 'edit-membership.html'
    def get(self, request, id=None):
        form = MembershipForm(instance=Membership.objects.get(id=id))
        context = {'form': form}
        return render(request, self.template_name, context)


    def post(self, request, id=None):
        qs = Membership.objects.get(id=id)
        form = MembershipForm(instance=qs, data=request.POST)
        if form.is_valid():
            form = form.save()
            context = {'form': form}
            messages.add_message(request, 1, 'Edited Successfully')
            return redirect('update_membership_plans', form.id)
        context = {'form': form}
        return render(request, self.template_name, context)