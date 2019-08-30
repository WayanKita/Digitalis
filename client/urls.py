from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

from django.contrib import admin

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name='client/login.html')),
    url(r'^logout/$', auth_views.LogoutView.as_view()),
    url('', views.offres_view, name='offres'),
]


