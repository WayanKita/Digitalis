from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # url(r'^myapp/$', HomeView.as_view(template_name='home.html'), name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='client/login.html')),
    url(r'^logout/$', auth_views.LogoutView.as_view()),
    url(r'^preferences/$', views.offres_view, name='offres'),
    # path(r'^logout/$', auth_views.LoginView.as_view(template_name='client/login.html')),
    # url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
]


