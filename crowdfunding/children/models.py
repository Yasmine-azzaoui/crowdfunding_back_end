# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Children(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    DOB= models.DateField()
    description = models.TextField()
    SpecialHelp = models.BooleanField()
    Specify = models.TextField()
    #create list
    image = models.URLField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
        # create or find owned_child  
    fundraiser = models.ForeignKey(
    'Fundraiser',
    related_name='owned_child' 
    )
    

