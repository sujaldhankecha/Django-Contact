from django.db import models

# Create your models here.
class Contact(models.Model):
    no = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    mobile = models.IntegerField()
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=50)


