
from django.urls import path, include
from .views import *
from .freelancer_views import *
# app_name = 'projects'

employer_urls = [
      path('create-project/', CreateProject.as_view(), name='create_project'),
      path('edit-project/<int:id>/',EditProject.as_view(), name='edit_project'),
      path('add-review/<int:id>/',AddReviewForProject.as_view(), name='add_review'),
      path('projects/<str:project_type>/',AllProjects.as_view(), name='all_projects'),
      path('invite-user/',CreateInvite.as_view(), name='invite_user'),
      path('project/<int:id>/',ProjectDetail.as_view(), name='project_detail'),
      path('pending-projects/',PendingProjects.as_view(), name='pending_projects'),
      path('ongoing-projects/',OngoingProjects.as_view(), name='ongoing_projects'),
      path('completed-projects/',CompletedProjects.as_view(), name='completed_projects'),
      path('cancelled-projects/',CancelledProjects.as_view(), name='cancelled_projects'),
      #path('project-chat/<str:user1>/<str:user2>/',ProjectChatView.as_view(), name='project_chat'),
]

freelancer_urls =[
      path('find-projects/',FindProject.as_view(), name='find_projects'),
      path('project-proposal/',ProjectProposal.as_view(), name='proposals'),
      path('my-ongoing-projects/',FreeOngoingProject.as_view(), name='free_ongoing_projects'),
      path('my-completed-projects/',FreeCompletedProject.as_view(), name='free_completed_projects'),
      path('my-canceleed-projects/',FreeCancelledProject.as_view(), name='free_cancelled_projects'),
      path('invite-list/',FreeInviteList.as_view(), name='free_invite_list'),
      path('projects-detail/v/<int:id>/',FreeProjectDetail.as_view(), name='free_project_detail'),
      path('favourite-project/',FavouriteProjectView.as_view(), name='fav_project_view'),
      path('favourite-project/<int:id>/',FavoriteProject.as_view(), name='fav_project'),
      path('remove-fav/<int:id>/',remove_favourite, name='remove_fav_project'),
      path('delete-proposal/<int:id>/',delete_proposal, name='delete_proposal'),
      path('search-all/',FindProjectAndFreelancerView.as_view(), name='find_all'),
]

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'skills', FeeViewset, basename='skills')

urlpatterns_admin = [
      path('skills-list/',SkillPage.as_view() , name="skills_list"),
      path('',include(router.urls)),

      path('review-approve/<int:id>/',ReviewApprove.as_view() , name="review_approve"),
      path('review-trash/<int:id>/',ReviewTrash.as_view() , name="review_trash"),
]
urlpatterns=employer_urls+freelancer_urls+urlpatterns_admin