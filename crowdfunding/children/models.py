# Create your models here.
from django.db import models
from fundraisers.models import Fundraiser


# Create your models here.
class Children(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    DOB= models.DateField()
    description = models.TextField()
    SpecialHelp = models.BooleanField()
    Specify = models.TextField(null=True)
    #create list
    image = models.URLField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    fundraisers= models.ForeignKey(
        Fundraiser,
        on_delete=models.CASCADE,
        related_name='owned_fundraisers' 
    )
    
    def __str__(self):
        return self.firstname