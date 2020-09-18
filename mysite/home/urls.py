from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

from home.views import signup_view
app_name='home'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(),name='home'),
    path('home/', views.ContentView.as_view(),name='content'),
    path('signup/', signup_view,name='signup'),
    path("login/", views.login_request, name="logins"),
    path("logout/", views.logout_request, name="logout"),
    path('addForum/', views.addInForum.as_view(), name='addForum'),
    path('Comment/<int:pk>', views.addInDiscussion.as_view(), name='Comment'),
    path('tags/<int:pk>', views.addInTag.as_view(), name='tags'),

]
