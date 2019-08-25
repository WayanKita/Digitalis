from django.contrib.auth.models import User
from django.db import models

from assurance.models import Assureur, Courtier, ProduitAssurance


class ChefEtablissement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    addresse = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.prenom + " " + self.nom


class Eleve(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    addresse = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    classe = models.CharField(max_length=100)
    date_de_naissance = models.DateField()
    date_ajout = models.DateField(blank=True, null=True)
    assure = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.prenom + " " + self.nom


class Assistant(models.Model):
    nom_utilisateur = models.CharField(max_length=150)
    mot_de_passe = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    numero_telephone = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_utilisateur


class Declaration(models.Model):
    BLESSURES = (
        ('0', 'Leger'),
        ('1', 'Grave'),
        ('2', 'Deces'),
    )
    STATUS = (
        ('0', 'Envoyer'),
        ('1', 'Reçu'),
        ('2', 'En cours de traitement'),
        ('3', 'Résolue'),
    )
    titre = models.CharField(max_length=100)
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    date_incident = models.DateField()
    lieu_incident = models.TextField()
    circonstence_incident = models.TextField()
    nature_blessure = models.CharField(max_length=5, choices=BLESSURES)
    information_supplementaire = models.TextField(max_length=500, blank=True, null=True)
    accepter = models.BooleanField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS)
    courtier = models.ForeignKey(Courtier, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

    def nature_blessure_verbose(self):
        return dict(Declaration.BLESSURES)[self.nature_blessure]


class Etablissement(models.Model):
    nom = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=200)
    numero_telephone = models.CharField(max_length=100)
    nombre_eleve = models.IntegerField()
    courtier = models.ForeignKey(Courtier, blank=True, null=True, on_delete=models.CASCADE)
    chef_etablissement = models.OneToOneField(ChefEtablissement, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "etablissement"
        verbose_name_plural = "etablissement"

    def __str__(self):
        return self.nom


class Souscription(models.Model):
    STATUS_SOUSCRIPTION = (
        ('0', 'Expression de Besoin'),
        ('1', 'Offre'),
        ('2', 'Paiement'),
        ('3', 'Souscrit'),
    )
    produit_assurance = models.ForeignKey(ProduitAssurance, related_name='souscription_produitassurance_eleve', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_SOUSCRIPTION)
    courtier = models.ForeignKey(Courtier, related_name='souscription_courtier_eleve', on_delete=models.CASCADE)
    eleve = models.OneToOneField(Eleve, on_delete=models.CASCADE)
    chef_etablissement = models.ForeignKey(ChefEtablissement, on_delete=models.CASCADE)
    date_expiration = models.DateField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.produit_assurance.titre


class DemandeSouscription(models.Model):
    chef_etablissement = models.ForeignKey(ChefEtablissement, on_delete=models.CASCADE)
    eleves = models.ManyToManyField(Eleve, blank=True)
    courtier = models.ForeignKey(Courtier, blank=True, null=True, on_delete=models.CASCADE)
    eleves_count = models.IntegerField(blank=True, null=True)
    payement_valider = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.chef_etablissement.prenom + " " + self.chef_etablissement.prenom + " pour " + str(self.eleves.count()) + " eleve(s)"
