from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from .admin_view import *

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'categories', CategoryViewset, basename='categories')
router.register(r'invites', InviteViewSet, basename='invites')



urlpatterns = [
    path('',include(router.urls)),
    path('all_reviews/', GetAllReviews.as_view()),
    path('create_review/', CreateReview.as_view()),
    path('reviews_got_by_me/', ReviewGotApi.as_view()),
    path('project-info/', OverallProjectInfo.as_view()),
    path('reviews_given_by_me/', ReviewGivenApi.as_view()),
    path('answer-invite/', AnswerInviteAPI.as_view(),name="answer_invite_api"),
    path('check-my-availability/', CheckMyAvailability.as_view(),name="check_my_availability_api"),
    path('change-status/<int:id>/',ChangeProjectStatus.as_view(), name='change_status'),
    path('approve-project/<int:project_id>/', ApproveProject.as_view(),name="approve_project"),
    path('review-detail/<int:id>/', ReviewDetailApi.as_view(),name="review_api_detail"),
]


admin_urls = [
    path('answer-identity-request/', AnswerIdentiyRequest.as_view(),name="answer_identity_request"),
]

urlpatterns+=admin_urls