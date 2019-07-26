from django.db import models


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


# class StudentInsured(Student):
#
#     readonly_fields = ["first_name", "last_name", "birth_date", "date_added"]
#



class Administrateur(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=100)
    nom_ecole = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)

    def __str__(self):
        return self.prenom + " " + self.nom


class Declaration(models.Model):
    titre = models.CharField(max_length=100)
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    # claim_picture = models.ImageField()
    raison = models.TextField(max_length=1000)
    information_supplementaire = models.TextField(max_length=500)

    def __str__(self):
        return self.titre


class Ecole(models.Model):
    nom = models.CharField(max_length=100)
    nom_directeur = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    numero_telephone = models.CharField(max_length=100)
    # school_logo = models.ImageField()
    nombre_eleve = models.IntegerField()

    def __str__(self):
        return self.nom
