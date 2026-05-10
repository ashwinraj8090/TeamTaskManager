from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list_view, name='project_list'),
    path('create/', views.create_project_view, name='create_project'),
    path('<int:project_id>/', views.project_detail_view, name='project_detail'),
    path('<int:project_id>/members/add/', views.add_member_view, name='add_member'),
    path('<int:project_id>/members/<int:membership_id>/remove/', views.remove_member_view, name='remove_member'),
    path('<int:project_id>/members/<int:membership_id>/role/', views.change_role_view, name='change_role'),
    path('<int:project_id>/toggle-completion/', views.toggle_project_completion_view, name='toggle_project_completion'),
    path('api/', views.project_api_view, name='project_api'),
]