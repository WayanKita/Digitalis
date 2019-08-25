from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import CreateView, ListView, View
from ecole.models import *
from ecole.utils import render_to_pdf


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
                  template_name="ecole/payment.html",
                  context={"eleves": Eleve.objects.all()})


def valider_payment(request, pk):
    requete = DemandeSouscription.objects.filter(pk=pk).get()
    requete.payement_valider = True
    requete.save()
    for eleve in requete.eleves.all():
        eleve.assure = True
        eleve.save()
    return redirect('/admin/ecole/demandesouscription')


def render_pdf(request, pk):
    context = {"declaration": Declaration.objects.filter(pk=pk).get(),
               "ecole": Etablissement.objects.all()[:1].get()}
    pdf = render_to_pdf('ecole/declaration_telecharger.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Declaration_%s.pdf" % Declaration.objects.filter(pk=pk).get().titre
        content = "attachement; filename=%s" % filename
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not Found")


def accepter_demande(request, pk):
    demande = Declaration.objects.filter(pk=pk).get()
    demande.status = '3'
    demande.accepter = True
    demande.save()
    return redirect('/admin/ecole/declaration')


def refuser_demande(request, pk):
    demande = Declaration.objects.filter(pk=pk).get()
    demande.status = '3'
    demande.accepter = False
    demande.save()
    return redirect('/admin/ecole/declaration')


def traite(request, pk):
    demande = Declaration.objects.filter(pk=pk).get()
    demande.status = '2'
    demande.save()
    return redirect('/admin/ecole/declaration')


