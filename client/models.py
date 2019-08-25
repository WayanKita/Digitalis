from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from assurance.models import Courtier, Assureur, ProduitAssurance


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    addresse = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    preferences = models.TextField(blank=True)

    def __str__(self):
        return self.prenom + " " + self.nom


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
    produit_assurance = models.ForeignKey(ProduitAssurance, on_delete=models.CASCADE )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    date_incident = models.DateField()
    lieu_incident = models.TextField()
    circonstence_incident = models.TextField()
    nature_blessure = models.CharField(max_length=5, choices=BLESSURES)
    information_supplementaire = models.TextField(max_length=500, blank=True, null=True)
    accepter = models.BooleanField(blank=True, null=True)
    status = models.CharField(max_length=5, choices=STATUS)
    courtier = models.ForeignKey(Courtier, blank=True, null=True, related_name='courtier_client', on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

    def nature_blessure_verbose(self):
        return dict(Declaration.BLESSURES)[self.nature_blessure]


class Souscription(models.Model):
    STATUS_SOUSCRIPTION = (
        ('0', 'Ininteresser'),
        ('1', 'Expression de Besoin'),
        ('2', 'Offre'),
        ('3', 'Paiement'),
        ('4', 'Souscrit'),
    )
    produit_assurance = models.ForeignKey(ProduitAssurance, related_name='souscription_produitassurance_client', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    courtier = models.ForeignKey(Courtier, related_name='souscription_courtier_client', blank=True, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_SOUSCRIPTION)
    date_expiration = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.produit_assurance.titre


class Offre(models.Model):
    STATUS_OFFRE = (
        ('0', "Demande en Cours"),
        ('1', 'Proposition'),
        ('2', 'Accepter'),
        ('3', 'Refuser'),
        ('4', 'Paiement en Cours'),
        ('5', 'Paiement Accepter'),
    )
    souscription = models.ForeignKey(Souscription, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    courtier = models.ForeignKey(Courtier, blank=True, null=True, related_name='offre_courtier_client', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_OFFRE)
    prix = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.souscription.produit_assurance.titre


