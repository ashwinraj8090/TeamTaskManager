from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_task_view, name='create_task'),
    path('<int:task_id>/update/', views.update_task_view, name='update_task'),
    path('<int:task_id>/action/<str:action>/', views.task_action_view, name='task_action'),
    path('api/members/', views.get_members_api, name='get_project_members_api'),
    path('', views.task_list_view, name='task_list'),
]