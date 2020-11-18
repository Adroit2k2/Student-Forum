"""books URL Configuration

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
from . import views
app_name='books'

urlpatterns = [
    path('books', views.search, name='search'),
    path('admin/', admin.site.urls),
    path("search_result", views.api, name="api"),
    path(r'book/<str:val>/',views.result,name='result'),
    path('cart',views.AddinCart_view,name='cart'),
    path('removed',views.remove_cart,name='remove'),

]
