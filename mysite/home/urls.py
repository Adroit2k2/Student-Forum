from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name='home'

urlpatterns = [
    path('', views.HomeView.as_view(),name='home'),
    path('home/', views.ContentView.as_view(),name='content'),
    path('signup/', views.SignupView.as_view(),name='signup'),
]
