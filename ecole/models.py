from django.contrib.auth.models import User
from django.db import models

from assurance.models import Assurance, Courtier


class ChefEtablissement(models.Model):
    user = models.OneToOneField(User)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    addresse = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)


class Eleve(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    addresse = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    classe = models.CharField(max_length=100)
    date_de_naissance = models.DateField()
    date_ajout = models.DateField()
    assure = models.BooleanField()

    def __str__(self):
        return self.prenom + " " + self.nom


class Assistant(models.Model):
    nom_utilisateur = models.CharField(max_length=150)
    mot_de_passe = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    numero_telephone = models.CharField(max_length=150)

    def __str__(self):
        return self.nom_utilisateur


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
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    assurance = models.ForeignKey(Assurance, related_name='assurance_eleve', on_delete=models.CASCADE)
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
    courtier = models.ForeignKey(Courtier, related_name='courtier_eleve', on_delete=models.CASCADE)


class Etablissement(models.Model):
    nom = models.CharField(max_length=100)
    directeur = models.ForeignKey(ChefEtablissement)
    adresse = models.CharField(max_length=200)
    numero_telephone = models.CharField(max_length=100)
    # school_logo = models.ImageField()
    nombre_eleve = models.IntegerField()

    class Meta:
        verbose_name = "ecole"
        verbose_name_plural = "ecoles"

    def __str__(self):
        return self.nom




