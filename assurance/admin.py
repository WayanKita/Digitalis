from django.contrib import admin

# Register your models here.
from assurance.models import *


class CourtierAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return []
        elif request.user.groups.filter(name='Courtier').exists():
            return ['user']


admin.site.register(Assureur)
admin.site.register(Courtier, CourtierAdmin)
admin.site.register(ProduitAssurance)
