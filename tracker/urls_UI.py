# tracker/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/edit/<int:id>/', views.task_edit, name='task_edit'),
    path('tasks/delete/<int:id>/', views.task_delete, name='task_delete'),
    path('tasks/<int:id>/approve/', views.task_approve, name='task_approve'),
    path('tasks/<int:id>/reject/', views.task_reject, name='task_reject'),
    
    ]
