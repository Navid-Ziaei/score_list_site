"""scorelist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from score_list_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    #AUTH
    path('signup/', views.signup_user, name='signup_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('login/', views.login_user, name='login_user'),


    #score_list
    path('profile/', views.profile, name='profile'),
    path('completed/', views.completed, name='completed'),
    path('create/', views.create_todo, name='create_todo'),
    path('upload/', views.upload_file, name='upload_file'),
    path('score_list/', views.score_list, name='score_list'),
    path('todo_view/<int:todo_pk>', views.todo_view, name='todo_view'),
    path('todo_view/complete/<int:todo_pk>', views.complete_task, name='complete_task'),
    path('todo_view/delete/<int:todo_pk>', views.delete_task, name='delete_task'),



]
