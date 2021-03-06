from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from django.template import RequestContext

from assurance.models import ProduitAssurance, Courtier
from client.forms import ChoixForm
from client.models import Offre, Souscription, Declaration
from client.utils import render_to_pdf


def offres_view(request):
    if request.method == 'POST':
        form = ChoixForm(request.POST, request=request)
        if form.is_valid():
            produits_choisis = form.cleaned_data.get('offres_form')
            client = request.user.client
            produit_list = []
            if not Souscription.objects.filter(client=client).exists():
                for produit in ProduitAssurance.objects.all():
                    Souscription.objects.create(produit_assurance=produit,
                                                client=client,
                                                status=0)
            for produit in produits_choisis:
                produit_list.append(produit.id)
                souscription = Souscription.objects.filter(client=client, produit_assurance=produit)[:1].get()
                souscription.status = 1
                souscription.save()
                if not Offre.objects.filter(client=client, souscription=souscription).exists():
                    for courtier in Courtier.objects.all():
                        Offre.objects.create(souscription=souscription,
                                             client=client,
                                             courtier=courtier,
                                             status=0)
            client.preferences = produit_list
            client.save()
            return HttpResponseRedirect('/admin/')
    else:
        form = ChoixForm(request=request)

    return render(request=request,
                  template_name='client/preferences.html',
                  context={'form': form})


def accepter(request, pk):
    offre = Offre.objects.filter(pk=pk).get()
    offre.status = '2'
    offre.save()
    Offre.objects.filter(client=request.user.client, souscription=offre.souscription, status='0').delete()
    Offre.objects.filter(client=request.user.client, souscription=offre.souscription, status='1').delete()
    souscription = Souscription.objects.filter(client=offre.client, produit_assurance=offre.souscription.produit_assurance).get()
    souscription.status = 3
    souscription.save()
    return redirect('/admin/client/offre/')


def refuser(request, pk):
    offre = Offre.objects.filter(pk=pk).get()
    offre.status = '3'
    offre.save()
    return redirect('/admin/client/offre/')


def payer(request, pk):
    offre = Offre.objects.filter(pk=pk).get()
    offre.status = '4'
    offre.save()
    return render(request=request,
                  template_name='client/paiement.html',
                  context={'offre': offre})


def accepter_paiement(request, pk):
    offre = Offre.objects.filter(pk=pk).get()
    offre.status = '5'
    offre.save()
    souscription = Souscription.objects.filter(client=offre.client,
                                               produit_assurance=offre.souscription.produit_assurance).get()
    souscription.status = 4
    souscription.courtier = request.user.courtier
    souscription.save()
    return redirect('/admin/client/offre/')


def render_pdf(request, pk):
    context = {"declaration": Declaration.objects.filter(pk=pk).get()}
    pdf = render_to_pdf('ecole/declaration_telecharger.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Declaration_%s.pdf" % Declaration.objects.filter(pk=pk).get().titre
        content = "attachement; filename=%s" % filename
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not Found")


def formulaire(request, pk):
    return render(request=request,
                  template_name="client/declaration_client.html",
                  context={"declaration": Declaration.objects.filter(pk=pk).get()})


def traite(request, pk):
    demande = Declaration.objects.filter(pk=pk).get()
    demande.status = '2'
    demande.save()
    return redirect('/admin/client/declaration')


def accepter_demande(request, pk):
    demande = Declaration.objects.filter(pk=pk).get()
    demande.status = '3'
    demande.accepter = True
    demande.save()
    return redirect('/admin/client/declaration')


def refuser_demande(request, pk):
    demande = Declaration.objects.filter(pk=pk).get()
    demande.status = '3'
    demande.accepter = False
    demande.save()
    return redirect('/admin/client/declaration')

