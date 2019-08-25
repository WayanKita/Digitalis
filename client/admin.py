from django.conf.urls import url
from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

from client import views
from client.models import *


class ClientAdmin(admin.ModelAdmin):
    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            pass
        else:
            self.exclude = ['preferences']
            super(ClientAdmin, self).get_exclude(request)


class DeclarationAdmin(admin.ModelAdmin):
    pass


class OffreAdmin(admin.ModelAdmin):
    def actions_button_client(self, obj):
        if obj.status is "1":
            return format_html(
                '<a class="button" href="{}">Accepter</a>&nbsp;'
                '<a class="button" href="{}">Refuser</a>',
                reverse('admin:accepter', args=[obj.pk]),
                reverse('admin:refuser', args=[obj.pk]),
            )
        elif obj.status is "2" or obj.status is "4":
            return format_html(
                '<a class="button" href="{}">Payer</a>&nbsp;',
                reverse('admin:payer', args=[obj.pk]),
            )

    def actions_button_courtier(self, obj):
        if obj.status is "4":
            return format_html(
                '<a class="button" href="{}">Accepter Paiement</a>&nbsp;',
                reverse('admin:accepter_payment', args=[obj.pk]),
            )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(r'^accepter/(?P<pk>.+)$', views.accepter, name='accepter'),
            url(r'^refuser/(?P<pk>.+)$', views.refuser, name='refuser'),
            url(r'^payer/(?P<pk>.+)$', views.payer, name='payer'),
            url(r'^accepter_payment/(?P<pk>.+)$', views.accepter_payment, name='accepter_payment'),
        ]
        return custom_urls + urls

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name='Courtier').exists():
            if obj.prix >= 0 and obj.status != 0:
                obj.status = 1
        super().save_model(request, obj, form, change)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['souscription', 'client', 'courtier', 'prix', 'status']
        elif request.user.groups.filter(name='Courtier').exists():
            return ['souscription', 'client', 'prix', 'status', 'actions_button_courtier']
        elif request.user.groups.filter(name='Client').exists():
            return ['souscription', 'courtier', 'prix', 'status', 'actions_button_client']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        elif request.user.groups.filter(name='Courtier').exists():
            if obj.status == '0':
                return ['souscription', 'client', 'status']
            else:
                return ['souscription', 'client', 'status', 'prix']
        elif request.user.groups.filter(name='Client').exists():
            return ['souscription', 'courtier', 'prix', 'status']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.groups.filter(name='Courtier').exists():
            return qs.filter(courtier=request.user.courtier)
        elif request.user.groups.filter(name='Client').exists():
            return qs.filter(client=request.user.client, prix__gte=0)
        else:
            return qs.filter(user=request.user)

    def get_exclude(self, request, obj=None):
        """Excludes One-to-One relationship with User from the view"""
        if request.user.is_superuser:
            return []
        elif request.user.groups.filter(name='Client').exists():
            return ['client']
        elif request.user.groups.filter(name='Courtier').exists():
            return ['courtier']

    def changelist_view(self, request, **kwargs):
        """Adds the 'Payer Toutes les Offres' button in Offre list view
            when more than 1 Offre has status 'Payer'('2')"""
        if request.user.groups.filter(name='Client').exists():
            if Offre.objects.filter(client=request.user.client, status='2').count() > 1:
                self.change_list_template = 'client/change_list.html'
        return super(OffreAdmin, self).changelist_view(request)

    actions_button_client.short_description = 'Actions'
    actions_button_client.allow_tags = True
    actions_button_courtier.short_description = 'Actions'
    actions_button_courtier.allow_tags = True
    filter = ['souscription']


class SouscriptionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.groups.filter(name='Courtier').exists():
            return qs.filter(courtier=request.user.courtier)
        elif request.user.groups.filter(name='Client').exists():
            return qs.filter(client=request.user.client, status__gte=3)
        else:
            return qs.filter(user=request.user)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['produit_assurance', 'client', 'courtier', 'status', 'date_expiration']
        elif request.user.groups.filter(name='Courtier').exists():
            return ['produit_assurance', 'client', 'status', 'date_expiration']
        elif request.user.groups.filter(name='Client').exists():
            return ['produit_assurance', 'courtier', 'status', 'date_expiration']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        elif request.user.groups.filter(name='Courtier').exists():
            if not obj.date_expiration:
                return ['produit_assurance', 'client', 'courtier', 'status']
            else:
                return ['produit_assurance', 'client', 'courtier', 'status', 'date_expiration']
        elif request.user.groups.filter(name='Client').exists():
            return ['produit_assurance', 'courtier', 'status']


admin.site.register(Client, ClientAdmin)
admin.site.register(Declaration, DeclarationAdmin)
admin.site.register(Offre, OffreAdmin)
admin.site.register(Souscription, SouscriptionAdmin)

