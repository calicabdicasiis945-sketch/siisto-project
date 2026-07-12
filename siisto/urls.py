from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('history/', views.history_view, name='history'),
    path('progress/', views.progress_view, name='progress'),
    
    # KAN WAA LINK-GA PROFILE-KA CUSUB
    path('profile/', views.profile_view, name='profile_page'),
    
    # QAYBAHA DELETE-KA (Tirtirista)
    path('tirtir-cunto/<int:cunto_id>/', views.tirtir_cunto, name='tirtir_cunto'),
    path('tirtir-jimicsi/<int:jimicsi_id>/', views.tirtir_jimicsi, name='tirtir_jimicsi'),
]