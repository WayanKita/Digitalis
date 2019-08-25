from django.contrib.auth.models import User
from django.db import models

# Create your models here.



class Assureur(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    numero_telephone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Courtier(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    addresse = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.prenom + " " + self.nom


class ProduitAssurance(models.Model):
    assureur = models.ForeignKey(Assureur, on_delete=models.CASCADE)
    titre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    prix = models.IntegerField()

    def __str__(self):
        return self.titre




