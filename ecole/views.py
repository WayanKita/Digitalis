import os
from datetime import timedelta, datetime

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import CreateView, ListView, View
from ecole.models import *
# from ecole.utils import render_to_pdf


def index(request):
    return HttpResponse("Page de reception, ecole")


def modele(request):
    return render(request=request,
                  template_name="ecole/declaration_modele.html",
                  context={"etablissement": Etablissement.objects.all()[:1].get()})


def formulaire(request, pk):
    return render(request=request,
                  template_name="ecole/declaration_eleve.html",
                  context={"declaration": Declaration.objects.filter(pk=pk).get(),
                           "etablissement": Etablissement.objects.all()[:1].get()})


def eleve_liste_confirmation(request):
    return render(request=request,
                  template_name="ecole/paiement.html",
                  context={"eleves": Eleve.objects.all()})


def valider_paiement(request, pk):
    requete = DemandeSouscription.objects.filter(pk=pk).get()
    requete.paiement_valider = True
    requete.save()
    for eleve in requete.eleves.all():
        eleve.assure = True
        eleve.save()
        souscription = Souscription.objects.filter(eleve=eleve).get()
        souscription.date_expiration = datetime.now() + timedelta(days=365)
        souscription.save()
    return redirect('/admin/ecole/demandesouscription')


def annuler_demande(request, pk):
    demande_souscription = DemandeSouscription.objects.filter(pk=pk).get()
    for eleve in demande_souscription.eleves.all():
        Souscription.objects.filter(eleve=eleve).delete()
    DemandeSouscription.objects.filter(pk=pk).delete()
    messages.success(request, "Votre demande a ete annuler")
    return redirect('/admin/ecole/eleve')


def accepter_demande_client(request, pk):
    demande = Declaration.objects.filter(pk=pk).get()
    demande.status = '3'
    demande.accepter = True
    demande.date_de_resolution = datetime.now()
    demande.save()
    return redirect('/admin/ecole/declaration')


def envoyer(request, pk):
    demande = Declaration.objects.filter(pk=pk).get()
    demande.status = '0'
    demande.save()
    return redirect('/admin/ecole/declaration')


def refuser_demande_client(request, pk):
    demande = Declaration.objects.filter(pk=pk).get()
    demande.status = '3'
    demande.accepter = False
    demande.save()
    return redirect('/admin/ecole/declaration')


def traiter_demande(request, pk):
    demande = Declaration.objects.filter(pk=pk).get()
    demande.status = '2'
    demande.save()
    return redirect('/admin/ecole/declaration')


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


