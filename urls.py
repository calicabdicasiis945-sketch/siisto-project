from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('history/', views.history, name='history'),
    path('progress/', views.progress_view, name='progress'),
    path('profile/', views.profile_view, name='profile_page'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]