from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.utils import timezone


# config for plans ( trial account: Aways string zero = '0' )
#------------------------------------------------------------------------------
plans_available = {
    '0': {
        'plan': _('trial'),
        'value': 0.00,
        'days_test': 90,
    },

    '1': {
        'plan': _('signature'),
        'value': 14.90,
        'days_test': 0,
    },

    '2': {
        'plan': _('free'),
        'value': 0.00,
        'days_test': 0,
    },
}
#------------------------------------------------------------------------------


class User_info(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    name = models.CharField(max_length=250, null=True, blank=True)
    occupation = models.CharField(max_length=250, null=True, blank=True)
    date_of_birth = models.DateField(max_length=8, null=True, blank=True)
    country = CountryField(blank=True, null=True)
    biography = models.CharField(max_length=700, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('userinfo:edit_profile', args=[self.pk])

    def __str__(self):
        return str(self.user)


class Account_plan(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    CHOICES_PLAN = ()
    
    count = 0

    for plan in plans_available:
        CHOICES_PLAN += ( list(plans_available.keys())[count]  ,  plans_available[str(count)]['plan'] ),
        count += 1

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    plan = models.CharField(max_length=50, choices=CHOICES_PLAN, default='0')
    date_limit_plan = models.DateTimeField(default=timezone.now() + timedelta(days=plans_available['0']['days_test']))

    def plan_verbose(self):
        return dict(Account_plan.CHOICES_PLAN)[self.plan]

    def __str__(self):
        return str(self.user)


class Subscription_history(models.Model):
    CHOICES_PLAN = ()
    
    CHOICES_STATUS = (
        ( 'renewed' , _('renewed') ),
        ( 'refused' , _('refused') ),
    )

    count = 0

    for plan in plans_available:
        CHOICES_PLAN += ( list(plans_available.keys())[count]  ,  plans_available[str(count)]['plan'] ),
        count += 1
    
    date = models.DateTimeField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50, choices=CHOICES_PLAN)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    status = models.CharField(max_length=50, choices=CHOICES_STATUS)
    
    def plan_status(self):
        return dict(Subscription_history.CHOICES_PLAN)[self.status]
    
    def plan_verbose(self):
        return dict(Subscription_history.CHOICES_PLAN)[self.plan]
    
    def __str__(self):
        return str(self.user)


class Privacy_policy(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    version = models.CharField(null=True, blank=True, max_length=1000)
    privacy_policy_en = models.TextField(null=True, blank=True, max_length=50000)
    service_terms_en = models.TextField(null=True, blank=True, max_length=50000)
    
    privacy_policy_pt_br = models.TextField(null=True, blank=True, max_length=50000)
    service_terms_pt_br = models.TextField(null=True, blank=True, max_length=50000)
