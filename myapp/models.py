from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    mobile = models.IntegerField()
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=50)


class Request(models.Model):
    request_sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='request_sender')
    request_receiver = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='request_receiver')
    accept_request = models.BooleanField(default=False)
