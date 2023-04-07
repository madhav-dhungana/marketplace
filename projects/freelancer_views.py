from itertools import chain
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from projects.filters import ProjectFilter, TravellerFilter
from user.models import WeekDayAvailable
from user.mixins import PaginateView
from .models import InviteModel, Project, ProjectCategory, DesiredExpertise
from user.mixins import AccessMixinView
from datetime import datetime, timedelta
from .forms import ProposalForm
from django.contrib import messages
from user.view.views import FreelancerList
from user.models import User
from django.db.models import Q

weekday = ["Sunday", "Monday", "Tuesday",
           "Wednesday", "Thursday", "Friday", "Saturday"]


class ProjectProposal(AccessMixinView):
    only_role = "Freelancer"

    def get(self, request):
        my_proposals = request.user.proposals.all()
        res = PaginateView()
        page = self.request.GET.get("page")
        response = res.give_paginated_response(page, my_proposals, 5)
        context = {"page_obj": response}
        return render(request, "projects/freelancer/project_proposal.html", context)


class FreeProjectDetail(AccessMixinView):
    only_role = "Freelancer"

    def get(self, request, id):
        project = get_object_or_404(
            Project.objects.select_related("posted_by"), id=id)
        proposals = request.user.proposals.filter(project=project)
        proposal = proposals.first()
        has_applied = proposals.exists()
        project_proposals = project.proposals.all()
        form = ProposalForm()
        context = {
            "project": project,
            "project_proposals": project_proposals,
            "form": form,
            "has_applied": has_applied,
            "proposal": proposal,
        }
        return render(request, "projects/freelancer/project_detail.html", context)

    def post(self, request, id):
        project = get_object_or_404(
            Project.objects.select_related("posted_by"), id=id)
        project_proposals = project.proposals.all()
        form = ProposalForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.project = project
            f.user = request.user
            f.save()
            messages.success(request, f"Proposal sent Successfully !")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        context = {
            "project": project,
            "project_proposals": project_proposals,
            "form": form,
        }
        return render(request, "projects/freelancer/project_detail.html", context)


def delete_proposal(request, id):
    proposal = get_object_or_404(Project, id=id)
    proposal.delete()
    my_proposals = request.user.proposals.all()
    return render(
        request, "projects/htmx/proposals.html", {"my_proposals": my_proposals}
    )


def remove_favourite(request, id):
    project = get_object_or_404(Project, id=id)
    request.user.bookmarked_projects.remove(project)
    projects = request.user.bookmarked_projects.all()
    return render(request, "projects/htmx/Fav.html", {"projects": projects})


class FreeOngoingProject(AccessMixinView):
    only_role = "Freelancer"

    def get(self, request):
        on_projects = request.user.hired_projects.filter(status="ON")
        res = PaginateView()
        page = self.request.GET.get("page")
        response = res.give_paginated_response(page, on_projects, 5)
        context = {"page_obj": response}
        return render(request, "projects/freelancer/ongoing_projects.html", context)


class FreeCompletedProject(AccessMixinView):
    only_role = "Freelancer"

    def get(self, request):
        com_projects = request.user.hired_projects.filter(status="COM")
        res = PaginateView()
        page = self.request.GET.get("page")
        response = res.give_paginated_response(page, com_projects, 10)
        context = {"page_obj": response}
        return render(request, "projects/freelancer/completed_projects.html", context)


class FreeCancelledProject(AccessMixinView):
    only_role = "Freelancer"

    def get(self, request):
        can_projects = request.user.hired_projects.filter(status="CAN")
        res = PaginateView()
        page = self.request.GET.get("page")
        response = res.give_paginated_response(page, can_projects, 10)
        context = {"page_obj": response}
        return render(request, "projects/freelancer/cancelled_projects.html", context)


class FindProject(View):
    # only_role = None

    def get(self, request):
        print(self.request.GET)
        projects = Project.objects.available()
        f = ProjectFilter(self.request.GET, queryset=projects)
        res = PaginateView()
        page = self.request.GET.get("page")
        response = res.give_paginated_response(page, f.qs, 5)
        context = {"page_obj": response}
        context["searchForm"] = f
        return render(request, "projects/freelancer/find_projects.html", context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        projects = Project.objects.available()
        if request.POST.get('query') == 'Batuwa':
            print('in batwa')
            projects = projects.filter(
                title__icontains=request.POST.get('title'))
        else:
            title = request.POST.get('title', None)
            return FreelancerList.get(self, request, title)
        f = ProjectFilter(self.request.POST, queryset=projects)
        res = PaginateView()
        page = self.request.POST.get("page")
        response = res.give_paginated_response(page, f.qs, 5)
        context = {"page_obj": response}
        context["searchForm"] = f
        return render(request, "projects/freelancer/find_projects.html", context)


class FindProjectAndFreelancerView(View):
    freelancer_template = "user/employer/search-freelancers.html"
    batuwa_template = "projects/freelancer/search-projects.html"

    def get(self, request):
        # print(request.session['test'],' session')
        query = request.GET.get('query', None)
        if query:
            if query == 'Traveller':
                queryset = User.objects.filter(role="Freelancer")
                if request.GET.get('keywords', None):
                    if ' ' not in request.GET.get('keywords'):
                        keywords = request.GET.get('keywords')
                        queryset = queryset.filter(Q(title__icontains=keywords) | Q(address__icontains=keywords) | Q(
                            email__icontains=keywords) | Q(display_name__icontains=keywords) | Q(country__icontains=keywords))
                if request.GET.get('location', None):
                    if ' ' not in request.GET.get('location'):
                        location = request.GET.get('location')
                        queryset = queryset.filter(Q(address__icontains=location) | Q(
                            state__icontains=location) | Q(country__icontains=location))

                searched_users = []
                projectCategory = ProjectCategory.objects.all()
                skills = DesiredExpertise.objects.all()

                if request.GET.get("rating"):
                    ratings = request.GET.getlist("rating")
                    queryset = queryset.filter(
                        user_ratings_floor__in=ratings)
                if request.GET.get("desired_skills"):
                    skills = request.GET.get("desired_skills").split(',')
                    queryset = queryset.filter(skills__skill_name__in=skills)
                if request.GET.getlist('experience', None):
                    for item in request.GET.getlist('experience'):
                        all_value = item.split('-')
                        min_value = all_value[0]
                        max_value = all_value[1]
                        queryset = queryset.filter()

                res = PaginateView()
                page = self.request.GET.get("page")
                if request.GET:
                    try:
                        response = res.give_paginated_response(
                            page, queryset, 10)
                    except:
                        response = None
                else:
                    try:
                        response = res.give_paginated_response(
                            page, queryset, 10)
                    except:
                        response = None
                context = {
                    "page_obj": response,
                    "projectCategory": projectCategory,
                    "skills": skills,
                }
                if request.GET:
                    context.update(
                        {"search_q": request.GET,
                         'experiences': ','.join(request.GET.getlist("experience")),
                         'ratings': ''.join(request.GET.getlist("rating"))}
                    )
                return render(request, self.freelancer_template, context)
            elif query == 'Batuwa':

                data = request.GET
                print(data, ' data here')
                # title =
                category = data.get('category', None)
                location = data.get('location', None)
                # tag =
                experience = data.getlist('experience', None)
                projectCategory = ProjectCategory.objects.all()
                skills = DesiredExpertise.objects.all()
                projects = Project.objects.filter(can_apply=True)
                if data.get('title', None):
                    if ' ' not in data.get('title', None):
                        title = data.get('title', None)
                        projects = projects.filter(
                            Q(title__icontains=title) | Q(location__icontains=title))
                if category:
                    projects = projects.filter(
                        category__name__icontains=category)

                if data.get('skills', None):
                    if ' ' not in data.get('skills', None):
                        skills = request.GET.get("skills").split(',')
                        projects = projects.filter(
                            desired_skills__skill_name__in=skills)

                if data.get('location', None):
                    if ' ' not in data.get('location'):
                        projects = projects.filter(
                            Q(location__name=location) | Q(address__icontains=location))

                if data.get('keyword', None):
                    if ' ' not in data.get('keyword', None):
                        keyword = data.get('keyword')
                        projects = projects.filter(
                            Q(title__icontains=keyword) |
                            Q(location__icontains=keyword) |
                            Q(address__icontains=keyword)
                        )

                if data.getlist('experience', None):
                    for item in data.getlist('experience'):
                        all_value = item.split('-')
                        min_value = all_value[0]
                        max_value = all_value[1]
                        projects = projects.filter(
                            experience_needed__lte=min_value, experience_needed__gte=max_value)
                res = PaginateView()
                page = self.request.POST.get("page")
                response = res.give_paginated_response(page, projects, 5)
                context = {"projectCategory": projectCategory, "skills": skills,
                           "page_obj": response}
                data.dict().pop('query')
                if data:
                    context.update(
                        {
                            "search_q": data,
                            'experiences': ','.join(request.GET.getlist("experience")),
                        }
                    )
                    print(context,' context')
                return render(request, self.batuwa_template, context)
            elif query == 'clear_all':
                return  
        return redirect('index')


class FavouriteProjectView(AccessMixinView):
    only_role = "Freelancer"

    def get(self, request):
        projects = request.user.bookmarked_projects.all()
        context = {"projects": projects}
        return render(request, "projects/freelancer/favourite_project.html", context)


class FavoriteProject(View):
    def post(self, request, id):
        user = request.user
        project = get_object_or_404(Project, id=id)
        if project in user.bookmarked_projects.all():
            bookmarked = False
            user.bookmarked_projects.remove(project)
        else:
            bookmarked = True
            user.bookmarked_projects.add(project)
        context = {"project": project}
        return render(request, "projects/htmx/Fav.html", context)


class FreeInviteList(AccessMixinView):
    only_role = "Freelancer"

    def get(self, request):
        me = request.user
        invites = request.user.invites_got.all()
        context = {"invites": invites}
        return render(request, "user/freelancer/invite_list.html", context)

    def post(self, request):
        invite_model = get_object_or_404(
            InviteModel, id=request.POST.get("u_id"))
        accepted = None
        print(request.POST)
        if request.POST.get("accept_invite") == "true":
            accepted = True
        else:
            accepted = False
        invite_model.answer_invite(accepted, request.user)
        accept_status = "accepted" if accepted else "declined"
        return JsonResponse(
            {
                "id": invite_model.id,
                "status": accept_status,
                "accepted": accepted,
                "msg": f"Successfully {accept_status} the invite by {invite_model.sent_by}",
            }
        )


class WeekdayAvailabilty(AccessMixinView):
    only_role = "Freelancer"

    def get(self, request):
        user = request.user
        weekdays = user.weekdayavailable_set.all().order_by("id")
        if weekdays.count() < 1:
            WeekDayAvailable.objects.bulk_create(
                WeekDayAvailable(name=i, user=user) for i in weekday)
        context = {"weekdays": weekdays}
        return render(request, "projects/freelancer/availability.html", context)
