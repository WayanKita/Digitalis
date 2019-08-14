from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView

from ecole.models import *


def index(request):
    return HttpResponse("Page de reception, ecole")


# class StudentCreate(CreateView):
#     model = Student
#     fields = ['name']

def modele(request):
    return render(request=request,
                  template_name="ecole/declaration_modele.html",
                  context={"ecole": Etablissement.objects.all()[:1].get()})


def formulaire(request, pk):
    if pk.isdigit():
        return render(request=request,
                      template_name="ecole/declaration_eleve.html",
                      context={"declaration" : Declaration.objects.filter(pk=pk).get(),
                           "ecole": Etablissement.objects.all()[:1].get()})
    else:
        return render(request=request,
                      template_name="ecole/declaration_eleve.html",
                      context={"ecole": Etablissement.objects.all()[:1].get()})