from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('battle/', views.battle, name='battle'),
    path('attack/', views.attack, name='attack'),
    path('start-battle/', views.start_battle, name='start-battle'),
    path('update-stats/', views.update_stats, name='update-stats'),
    path('get-player', views.get_player, name='get-player'),
]