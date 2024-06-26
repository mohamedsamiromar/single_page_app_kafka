"""single_page_app_kafka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.authtoken import views
# from django_kafka.views import RegisterView, get_data_with_user_name
from django_kafka.commands import get_commands_from_last_offset, commands_home

urlpatterns = [
    url('home', TemplateView.as_view(template_name='../templates/home/home.html'), name="home"),

    url(r'^admin', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    # url(r'^login', views.obtain_auth_token, name='api_token_auth'),
    # url(r'^register', RegisterView.as_view(), name='register'),
    url(r'^auth/', include('authentication.urls')),
    url(r'^django-kafka/', include('django_kafka.urls')),
    url(r'^commands-home', commands_home, name='commands-home'),

]