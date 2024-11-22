from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('main/', views.main, name='main'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('logout/', views.logout_view, name='logout_view'),
    path('add_to_watchlist/<int:movie_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/', views.watchlist_page, name='watchlist_page'),
    path('remove_from_watchlist/<int:movie_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('recommendations/', views.recommendation_page, name='recommendation_page'),
]
