from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('declaration/modele_de_declaration', views.modele, name='modele'),
    path('declaration/formulaire', views.formulaire, name='formulaire'),
]