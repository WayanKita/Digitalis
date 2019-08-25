from django.contrib import admin
from django.contrib.admin import AdminSite


class MyAdminSite(admin.AdminSite):
    view_on_site = False


admin.site.register(MyAdminSite)
admin.site.site_header = "OnDigitalise"



