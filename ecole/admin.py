from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from django.urls import reverse

from ecole import views
from .resources import EleveResource



# Register your models here.
from ecole.models import *


def assurer(modeladmin, request, queryset):
    pass


class EcoleAdmin(admin.ModelAdmin):
    pass


class EleveAdmin(ImportExportModelAdmin):
    actions = [assurer, ]
    list_display = (
        'prenom',
        'nom',
        'classe',
        'date_de_naissance',
        'assure')

    readonly_fields = ["assure"]
    list_filter = ['assure']

    def get_readonly_fields(self, request, obj=None):
        if obj.assure:
            return ["prenom", "nom", "date_de_naissance", "date_ajout"]
        else:
            return []

    def my_admin_action(modeladmin, request, queryset):
        pass

        # do something with the queryset

    my_admin_action.short_description = 'Assure les eleves selectiones'


class DeclarationAdmin(admin.ModelAdmin):
    def get_urls(self):

        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<pk>.+)$', views.formulaire,
                name='voire')
            ,
            url(
                r'^(?P<pk>.+)$', views.formulaire,
                name='telecharger'),
        ]
        return custom_urls + urls

    def actions_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Voire</a>&nbsp;'
            '<a class="button" href="{}">Telecharger</a>',
            reverse('admin:voire', args=[obj.pk]),
            reverse('admin:telecharger', args=[obj.pk]),
        )

    list_display = (
        'titre',
        'eleve',
        'actions_button',
    )

    actions_button.short_description = 'Actions'
    actions_button.allow_tags = True


assurer.short_description = 'Assurer ces eleves'
admin.site.site_header = "RC Scolaire"
admin.site.register(Eleve, EleveAdmin)
admin.site.register(Assistant)
admin.site.register(Declaration, DeclarationAdmin)
admin.site.register(Etablissement, EcoleAdmin)


