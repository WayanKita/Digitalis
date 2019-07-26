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


class EcoleAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # def __unicode__(self):  # __str__ on Python 3
    #     return "Ecole"
    #
    # class Meta:
    #     verbose_name_plural = "Ecole"


class EleveAdmin(ImportExportModelAdmin):
    # def export(request):
    #     person_resource = EleveResource()
    #     dataset = person_resource.export()
    #     response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    #     response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    #     return response

    list_display = (
        'prenom',
        'nom',
        'classe',
        'date_de_naissance')
    # exclude = ('assure',)


class DeclarationAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<pk>.+)/declaration/$', views.formulaire,
                name='voire')
            ,
            url(
                r'^(?P<pk>.+)/declaration/$', views.formulaire,
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



admin.site.site_header = "RC Scolaire"
admin.site.register(Eleve, EleveAdmin)
admin.site.register(Administrateur)
admin.site.register(Declaration, DeclarationAdmin)
admin.site.register(Ecole, EcoleAdmin)


