from django.contrib import admin
from .models import Contact, Request


class ContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'lastname', 'mobile', 'email', 'address')  #


admin.site.register(Contact, ContactAdmin)


class RequestAdmin(admin.ModelAdmin):
    list_display = ('request_sender', 'request_receiver','accept_request')


admin.site.register(Request, RequestAdmin)
