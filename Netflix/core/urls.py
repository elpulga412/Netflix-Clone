from unicodedata import name
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile_list, name='listProfile'),
    path('profile/create/', views.profile_create, name='createProfile'),
    path('watch/<str:profile_id>/', views.watch, name="watch"),
    path('movie/detail/<str:movie_id>/',views.show_movie_detail,name='show_det'),
    path('movie/play/<str:movie_id>/',views.show_movie,name='play'),
    path('api/movies/<str:profile_id>/', views.api_movie, name='api_movies'),
]