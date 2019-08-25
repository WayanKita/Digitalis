# Generated by Django 2.2.3 on 2019-08-25 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assurance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prenom', models.CharField(max_length=100)),
                ('nom', models.CharField(max_length=100)),
                ('addresse', models.CharField(max_length=100)),
                ('numero_telephone', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('preferences', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Souscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('0', 'Ininteresser'), ('1', 'Expression de Besoin'), ('2', 'Offre'), ('3', 'Paiement'), ('4', 'Souscrit')], max_length=1)),
                ('date_expiration', models.DateField(blank=True, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Client')),
                ('courtier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='souscription_courtier_client', to='assurance.Courtier')),
                ('produit_assurance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='souscription_produitassurance_client', to='assurance.ProduitAssurance')),
            ],
        ),
        migrations.CreateModel(
            name='Offre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('0', 'Demande en Cours'), ('1', 'Proposition'), ('2', 'Accepter'), ('3', 'Refuser'), ('4', 'Paiement en Cours'), ('5', 'Paiement Accepter')], max_length=1)),
                ('prix', models.IntegerField(blank=True, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Client')),
                ('courtier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offre_courtier_client', to='assurance.Courtier')),
                ('souscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Souscription')),
            ],
        ),
        migrations.CreateModel(
            name='Declaration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('addresse', models.CharField(max_length=200)),
                ('numero_telephone', models.CharField(max_length=100)),
                ('numero_mobile', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('raison', models.TextField(max_length=1000)),
                ('information_supplementaire', models.TextField(max_length=500)),
                ('date', models.DateField()),
                ('date_incident', models.DateField()),
                ('lieu_incident', models.TextField()),
                ('circonstence_incident', models.TextField()),
                ('nature_blessure', models.CharField(choices=[('Leger', 'Leger'), ('Grave', 'Grave'), ('Deces', 'Deces')], max_length=5)),
                ('status', models.CharField(choices=[('Reçu', 'Reçu'), ('En cours de traitement', 'En cours de traitement'), ('Résolue', 'Résolue')], max_length=5)),
                ('assurance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assurance_client', to='assurance.Assureur')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Client')),
                ('courtier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courtier_client', to='assurance.Courtier')),
            ],
        ),
    ]
