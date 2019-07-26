from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView

from ecole.models import Eleve, Ecole


def index(request):
    return HttpResponse("Page de reception, ecole")


# class StudentCreate(CreateView):
#     model = Student
#     fields = ['name']

def modele(request):
    return render(request=request,
                  template_name="ecole/declaration_modele.html",
                  context={"ecole": Ecole.objects.all()[:1].get()})


def formulaire(request):
    return render(request=request,
                  template_name="ecole/declaration_eleve.html",
                  context={"eleve" : Eleve.objects.filter(prenom="wayan").get(),
                           "ecole": Ecole.objects.all()[:1].get()})
