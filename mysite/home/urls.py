from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
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
    path('Comment/<int:pk>/', views.addInDiscussion.as_view(), name='comment'),
    path('tags/<int:pk>', views.addInTag.as_view(), name='tags'),
    path('option/<int:pk>', views.addInOption.as_view(), name='option'),
    path('EditProfile/<int:pk>', views.EditProfile.as_view(), name='editprofile'),
    path('add_profile_picture/<int:pk>', views.stream_file, name='dp'),
    path("password/", views.Change_password.as_view(), name='change_password'),
    path('addInUpVote/<int:pk>', views.addInUpVote.as_view(), name='upvote'),
    path('addInDownVote/<int:pk>', views.addInDownVote.as_view(), name='downvote'),
    path('profile/<str:pk>', views.ProfileSearchView.as_view(), name='searchprofile'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('forum/<int:pk>/delete', views.DeleteForum.as_view(), name='delete_forum'),
    path('forum/<int:pk>/update',views.ForumUpdate.as_view(success_url=reverse_lazy('home:content')), name='forum_update'),
    path('tags/', views.TagsView.as_view(), name='searchtags'),
    path('tags/<str:pk>', views.ForumTagsView.as_view(), name='tags_forum'),
    path('forum/<int:pk>/favorite',views.AddFavoriteView.as_view(), name='forum_favorite'),
    path('forum/<int:pk>/unfavorite',views.DeleteFavoriteView.as_view(), name='forum_unfavorite'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('construct/', views.Construct.as_view(), name='construct'),
]
