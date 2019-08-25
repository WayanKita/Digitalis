from django.conf.urls import url
from django.contrib import admin
from django.db.models.functions import datetime
from django.shortcuts import render
from import_export.admin import ImportExportModelAdmin, ExportMixin
from django.utils.html import format_html
from django.urls import reverse
from import_export.formats import base_formats
from django.db.models import Count

from ecole import views
from ecole.models import *

MAX_OBJECTS = 1


class EleveAdmin(ImportExportModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.assure:
                return ["prenom", "nom", "date_de_naissance", "date_ajout"]
            else:
                return []
        except:
            return []

    def assurer(self, request, queryset):
        count = queryset.count()
        count = count*1000
        produit_rc_scolaire = ProduitAssurance.objects.filter(titre='RC Scolaire').get()
        courtier = Etablissement.objects.filter(chef_etablissement=request.user.chefetablissement).get().courtier
        demande_souscription = DemandeSouscription.objects.create(chef_etablissement=request.user.chefetablissement,
                                                                  courtier=courtier)
        demande_souscription.save()
        for eleve in queryset:
            print(eleve.nom)
            Souscription.objects.create(produit_assurance=produit_rc_scolaire,
                                        status='2',
                                        courtier=courtier,
                                        eleve=eleve,
                                        chef_etablissement=request.user.chefetablissement,
                                        date_creation=datetime.datetime.now())
            demande_souscription.eleves.add(eleve)
            demande_souscription.save()
        demande_souscription.eleves_count = demande_souscription.eleves.all().count()
        demande_souscription.save()
        return render(request=request,
                      template_name="ecole/payment.html",
                      context={"object_list": queryset,
                               "count": count})

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name='Chef Etablissement').exists():
            if obj.pk is None:
                obj.user = request.user
                obj.assure = False
                obj.date_ajout = datetime.datetime.now()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_export_formats(self):
        """
        Returns available export formats.
        """
        formats = (
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

    def get_exclude(self, request, obj=None):
        if request.user.groups.filter(name='Chef Etablissement').exists():
            return ['assure', 'user', 'date_ajout']
        else:
            return []

    actions = ['assurer']
    list_display = (
        'prenom',
        'nom',
        'classe',
        'date_de_naissance',
        'assure')

    readonly_fields = ["assure"]
    list_filter = ['assure']
    assurer.short_description = 'Assure les eleves selectiones'


class AssistantAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    exclude = ['user']


class ChefEtablissementAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


class DeclarationAdmin(admin.ModelAdmin):
    def actions_button_chef_etablissement(self, obj):
        return format_html(
            '<a class="button" href="{}">Voire</a>&nbsp;'
            '<a class="button" href="{}">Telecharger</a>',
            reverse('admin:voire', args=[obj.pk]),
            reverse('admin:telecharger', args=[obj.pk]),
        )

    def actions_button_courtier(self, obj):
        if obj.status is '1':
            return format_html(
                '<a class="button" href="{}">Traite la demande</a>&nbsp;',
                reverse('admin:traite', args=[obj.pk]),
            )
        if obj.status is '2':
            return format_html(
                '<a class="button" href="{}">Accepter</a>&nbsp;'
                '<a class="button" href="{}">Refuser</a>',
                reverse('admin:accepter_demande', args=[obj.pk]),
                reverse('admin:refuser_demande', args=[obj.pk]),
            )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(r'^formulaire/(?P<pk>.+)$', views.formulaire, name='voire'),
            url(r'^formulaire_telecharger/(?P<pk>.+)$', views.render_pdf, name='telecharger'),
            url(r'^traite/(?P<pk>.+)$', views.traite, name='traite'),
            url(r'^accepter/(?P<pk>.+)$', views.accepter_demande, name='accepter_demande'),
            url(r'^refuser/(?P<pk>.+)$', views.refuser_demande, name='refuser_demande'),
        ]
        return custom_urls + urls

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name='Chef Etablissement').exists():
            if obj.pk is None:
                obj.user = request.user
                obj.date = datetime.datetime.now()
                obj.courtier = Etablissement.objects.filter(chef_etablissement=request.user.chefetablissement).get().courtier
                obj.status = '0'
            super().save_model(request, obj, form, change)
        else:
            super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.groups.filter(name='Courtier').exists():
            if qs.filter(courtier=request.user.courtier):
                for declaration in qs:
                    if declaration.status == '0':
                        declaration.status = '1'
                        declaration.save()
            return qs.filter(courtier=request.user.courtier)
        elif request.user.groups.filter(name='Chef Etablissement').exists():
            return qs.filter(user=request.user)
        else:
            return qs

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Courtier').exists():
            return ["titre",
                    "eleve",
                    'date_incident',
                    'lieu_incident',
                    'circonstence_incident',
                    'nature_blessure',
                    'information_supplementaire',
                    'courtier']
        if obj:
            if not obj.status == "0":
                if request.user.groups.filter(name='Chef Etablissement').exists():
                    return ["titre",
                            "eleve",
                            'date_incident',
                            'lieu_incident',
                            'circonstence_incident',
                            'nature_blessure',
                            'information_supplementaire',
                            'courtier']
        else:
            return []

    def get_list_display(self, request):
        if request.user.groups.filter(name='Courtier').exists():
            return ['titre', 'eleve', 'status', 'accepter', 'actions_button_courtier']
        elif request.user.groups.filter(name='Chef Etablissement').exists():
            return ['titre', 'eleve', 'status', 'accepter', 'actions_button_chef_etablissement']
        else:
            return ['titre', 'eleve', 'status', 'accepter']

    def get_exclude(self, request, obj=None):
        if request.user.groups.filter(name='Chef Etablissement').exists():
            return ['user', 'date', 'courtier', 'accepter', 'status']
        if request.user.groups.filter(name='Courtier').exists():
            return ['user', 'date', 'courtier']
        else:
            return []

    actions_button_chef_etablissement.short_description = 'Actions'
    actions_button_chef_etablissement.allow_tags = True
    actions_button_courtier.short_description = 'Actions'
    actions_button_courtier.allow_tags = True
    exclude = ['assure', 'user']
    list_filter = ['status']


class EtablissementAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.filter(user=request.user).count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name='Chef Etablissement').exists():
            obj.user = request.user
            obj.chef_etablissement = request.user.chefetablissement
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_exclude(self, request, obj=None):
        if request.user.groups.filter(name='Chef Etablissement').exists():
            return ['chef_etablissement', 'user']

    exclude = ['user']


class DemandeSouscriptionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Courtier').exists():
            return qs.filter(courtier=request.user.courtier)
        if request.user.groups.filter(name='Chef Etablissement').exists():
            return qs.filter(chef_etablissement=request.user.chefetablissement)
        if request.user.is_superuser:
            return qs

    def actions_button(self, obj):
        if not obj.payement_valider:
            return format_html(
                '<a class="button" href="{}">Valider payement</a>&nbsp;',
                reverse('admin:valider_payment', args=[obj.pk]),
            )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(r'^valider_payment/(?P<pk>.+)$', views.valider_payment, name='valider_payment'),
        ]
        return custom_urls + urls

    def get_list_display(self, request):
        if request.user.groups.filter(name='Chef Etablissement').exists():
            return ['courtier', 'eleves_count', 'payement_valider', 'actions_button']
        if request.user.groups.filter(name='Courtier').exists():
            return ['chef_etablissement', 'eleves_count', 'payement_valider', 'actions_button']
        if request.user.is_superuser:
            return ['chef_etablissement', 'courtier', 'eleves_count', 'payement_valider', 'actions_button']

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Courtier').exists():
            return ['chef_etablissement', 'eleves', 'eleves_count', 'payement_valider', 'actions_button']
        if request.user.groups.filter(name='Chef Etablissement').exists():
            return ['courtier', 'eleves', 'eleves_count', 'payement_valider', 'actions_button']
        if request.user.is_superuser:
            return ['chef_etablissement', 'courtier', 'eleves_count', 'payement_valider', 'actions_button']

    def get_exclude(self, request, obj=None):
        if request.user.groups.filter(name='Courtier').exists():
            return ['courtier']
        if request.user.groups.filter(name='Chef Etablissement').exists():
            return ['chef_etablissement']
        if request.user.is_superuser:
            return []


    actions_button.short_description = 'Actions'
    actions_button.allow_tags = True


class SouscriptionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.groups.filter(name='Courtier').exists():
            return qs.filter(courtier=request.user.courtier)
        elif request.user.groups.filter(name='Chef Etablissement').exists():
            return qs.filter(chef_etablissement=request.user.chefetablissement)
        else:
            return qs

    def get_list_display(self, request):
        if request.user.groups.filter(name='Courtier').exists():
            return ['produit_assurance', 'eleve', 'chef_etablissement', 'date_expiration']
        elif request.user.groups.filter(name='Chef Etablissement').exists():
            return ['produit_assurance', 'eleve', 'courtier', 'date_expiration']
        else:
            return ['produit_assurance', 'eleve', 'chef_etablissement', 'courtier', 'date_expiration']

    def get_list_filter(self, request):
        if request.user.groups.filter(name='Courtier').exists():
            return ['produit_assurance', 'chef_etablissement', 'date_expiration']
        elif request.user.groups.filter(name='Chef Etablissement').exists():
            return ['produit_assurance', 'courtier', 'date_expiration']
        else:
            return ['produit_assurance', 'chef_etablissement', 'courtier', 'date_expiration']

admin.site.site_header = "OnDigitalise"
admin.site.register(Eleve, EleveAdmin)
admin.site.register(Assistant, AssistantAdmin)
admin.site.register(ChefEtablissement, ChefEtablissementAdmin)
admin.site.register(Declaration, DeclarationAdmin)
admin.site.register(Etablissement, EtablissementAdmin)
admin.site.register(DemandeSouscription, DemandeSouscriptionAdmin)
admin.site.register(Souscription, SouscriptionAdmin)



