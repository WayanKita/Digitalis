from django.conf.urls import url
from django.urls import path

# from ecole.views import EleveListView
from django.contrib import admin
from . import views

admin.site_header = "OnDigitalise"
admin.index_title = ''
admin.site_title = 'OnDigitalise'

urlpatterns = [
    path('index/', views.index, name='index'),
    url(r'^declaration/modele_de_declaration/$', views.modele, name='modele'),
    url(r'^declaration/formulaire/$', views.formulaire, name='formulaire'),
    url(r'^eleve/paiement_confirmation/$', views.eleve_liste_confirmation, name='eleve-list'),
    url(r'^eleve/annuler_demande/(?P<pk>.+)$', views.annuler_demande, name='annuler_demande'),
]