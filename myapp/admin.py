from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('user','firstname','lastname','mobile','email','address')#

admin.site.register(Contact,ContactAdmin)
