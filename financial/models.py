from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Table_invoices(models.Model):

    POSTING_TYPES = (
        ('expense', _('expense')),
        ('revenue', _('revenue')),
    )

    STATUS_TYPES = (
        ('pending', _('pending')), 
        ('paid', _('paid')),
        ('canceled', _('canceled')),
        ('overdue', _('overdue')),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posting_type = models.CharField(max_length=50, choices=POSTING_TYPES, default='expense')
    payment_description = models.CharField(max_length=250)
    payment_amount = models.DecimalField(max_digits=20, decimal_places=2)
    due_date = models.DateField()
    payee = models.CharField(max_length=250, null=True, blank=True)
    document_number = models.CharField(max_length=250, null=True, blank=True)
    category = models.CharField()
    bank_account = models.CharField(max_length=100)
    card = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(max_length=300, null=True, blank=True)
    status = models.CharField(choices=STATUS_TYPES, default='pending')

    def __str__(self):
        return self.payment_description

    def get_absolute_url_delete(self):
        return reverse('financial:delete_invoice', args=[self.pk])

    def get_absolute_url_update(self):
        return reverse('financial:update_invoice', args=[self.pk])

    # Form is ok
    def get_absolute_url(self):
        return reverse('financial:list_invoice')

class Invoice_category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_category = models.CharField(max_length=250)

    def get_absolute_url_update(self):
        return reverse('financial:settings_update_category', args=[self.pk])

class Invoice_bank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_bank = models.CharField(max_length=250)

    def get_absolute_url_update(self):
        return reverse('financial:settings_update_bank', args=[self.pk])

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.CharField(max_length=250)
    
    def get_absolute_url_update(self):
        return reverse('financial:settings_update_card', args=[self.pk])

class Payee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payee = models.CharField(max_length=250)
    
    def get_absolute_url_update(self):
        return reverse('financial:settings_update_payee', args=[self.pk])