
from django.urls import path
from .view.admin_view import *


urlpatterns = [
   path('dashboard/',Dashboard.as_view(), name='admin_dashboard'),
   path('categories/',CategoryView.as_view(), name='category_view'),
   path('user-list/',UserListView.as_view(), name='user_list'),
   path('reviews-list/',ReviewAdminList.as_view(), name='review_admin_list'),
   path('identity-formlist/',IdentyFormList.as_view(), name='identity_form_list'),
   path('project-list/<str:project_type>/',ProjectListView.as_view(), name='project_list'),
   path('user-detail/<int:id>/',UserDetailView.as_view(), name='admin_user_detail'),
   path('user-edit/<int:id>/',UserEditView.as_view(), name='admin_user_edit'),
   path('delete-project/<int:project_id>/',DeleteProject.as_view(), name='admin_delete_project'),   
   path('edit-project/<int:id>/',ProjectEditView.as_view(), name='admin_edit_project'),   
   path('delete-user/<int:id>/',UserDeleteAdmin.as_view(), name='admin_delete_user'),   
]



