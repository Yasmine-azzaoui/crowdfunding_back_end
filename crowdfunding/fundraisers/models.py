from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


# Create your models here.
class Fundraiser(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField(null=True)
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_fundraisers'  
    )

class Pledge(models.Model):
    MONEY = 'money'
    TIME = 'time'
    PLEDGE_TYPE_CHOICES = [
        (MONEY, 'Money'),
        (TIME, 'Time'),
    ]

    pledge_type = models.CharField(max_length=10, choices=PLEDGE_TYPE_CHOICES, default=MONEY)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # for money pledges
    hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)    # for time pledges
    comment = models.CharField(max_length=200, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    anonymous = models.BooleanField(default=False)
    fundraiser = models.ForeignKey(
        'Fundraiser',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name='pledges',
        null=True,
        blank=True
    )

    def clean(self):
        from django.core.exceptions import ValidationError
        #TO PLEADGE MONEY
        if self.pledge_type == self.MONEY and (self.amount is None):
            raise ValidationError('Amount is required for money pledges.')
        #TO PLEDGE HOURS
        if self.pledge_type == self.TIME and (self.hours is None):
            raise ValidationError('Hours is required for time pledges.')
        # CAN PLEDGE WITHOUT BEING A USER
        if self.anonymous and self.supporter is not None:
            raise ValidationError('Anonymous users can not commit time.')
        super().clean()

    def save(self, *args, **kwargs):
        # ensure validation runs on save
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Pledge {self.pk} ({self.pledge_type})'