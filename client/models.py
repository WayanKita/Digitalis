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
        ('Leger', 'Leger'),
        ('Grave', 'Grave'),
        ('Deces', 'Deces'),
    )
    STATUS = (
        ('Reçu', 'Reçu'),
        ('En cours de traitement', 'En cours de traitement'),
        ('Résolue', 'Résolue'),
    )

    titre = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    assurance = models.ForeignKey(Assureur, related_name='assurance_client', on_delete=models.CASCADE)
    addresse = models.CharField(max_length=200)
    numero_telephone = models.CharField(max_length=100)
    numero_mobile = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    raison = models.TextField(max_length=1000)
    information_supplementaire = models.TextField(max_length=500)
    date = models.DateField()
    date_incident = models.DateField()
    lieu_incident = models.TextField()
    circonstence_incident = models.TextField()
    nature_blessure = models.CharField(max_length=5, choices=BLESSURES)
    status = models.CharField(max_length=5, choices=STATUS)
    courtier = models.ForeignKey(Courtier, related_name='courtier_client', on_delete=models.CASCADE)

    def __str__(self):
        return self.titre


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


