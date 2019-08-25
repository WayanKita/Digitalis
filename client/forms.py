from django import forms

from assurance.models import ProduitAssurance
from client.models import Offre, Souscription


class ChoixForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ChoixForm, self).__init__(*args, **kwargs)
        offres_disponible = Offre.objects.filter(client=self.request.user.client, status__lte=1).values(
            'souscription').distinct()
        tous_les_produits = ProduitAssurance.objects.all()
        for offre in offres_disponible.values():
            souscription = Souscription.objects.filter(pk=offre['souscription_id']).get()
            tous_les_produits = tous_les_produits.exclude(titre=souscription.produit_assurance.titre)

        self.fields['offres_form'] = forms.ModelMultipleChoiceField(queryset=tous_les_produits, widget=forms.CheckboxSelectMultiple)

    # offres_form = forms.ModelMultipleChoiceField(queryset=ProduitAssurance.objects.all(), widget=forms.CheckboxSelectMultiple)

