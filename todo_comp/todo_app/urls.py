from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('tasks', views.task_list, name='task_list'),
    path('profile/<str:username>', views.profile_view, name='profile'),
    path('tasks_by_date/<str:username>/<str:date>', views.tasks_by_date, name='tasks_by_date'),
]
