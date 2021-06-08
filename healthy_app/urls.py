from django.urls import path     
from . import views
urlpatterns = [
    # GETS
    path('', views.index),
    path('dashboard', views.dashboard),
    path('logout', views.logout), 
    path('food/new/', views.newfoods), 
    path('workout/new', views.newworkout),
    path('weigh-in/new', views.weighin),
    path('viewall', views.viewall),
    path('food/<int:foodid>/edit', views.editfood),



    # POSTS
    path('regi', views.regi), 
    path('login', views.login),
    path('create', views.create),
    path('create_workout', views.create_workout),
    path('create_weighin', views.create_weighin),
    path("food/<int:foodid>/destroy", views.food_destroy),
    path("workout/<int:workoutid>/destroy", views.workout_destroy),
    path("weight/<int:weightid>/destroy", views.weight_destroy),
]