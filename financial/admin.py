from django.contrib import admin
from .models import Table_invoices, Invoice_category, Invoice_bank, Card, Payee


@admin.register(Table_invoices)
class Table_invoices(admin.ModelAdmin):
    
    raw_id_fields = ('user',)

    list_display = (
        'due_date',
        'user',
        'payment_description',
        'posting_type',

    )
    
    list_filter = (
        'posting_type',
        'category',
    )

    search_fields = (
        'posting_type',
        'payment_description',
        'payment_amount',
        'due_date',
        'payee',
        'document_number',
        'category',
        'bank_account',
    )
    
    
@admin.register(Invoice_category)
class Table_invoices(admin.ModelAdmin):
    
    raw_id_fields = ('user',)

    list_display = (
        'user',
        'invoice_category',
    )

@admin.register(Invoice_bank)
class Table_invoices(admin.ModelAdmin):
    
    raw_id_fields = ('user',)

    list_display = (
        'user',
        'invoice_bank',
    )

@admin.register(Card)
class Table_invoices(admin.ModelAdmin):
    
    raw_id_fields = ('user',)

    list_display = (
        'user',
        'card',
    )

@admin.register(Payee)
class Table_invoices(admin.ModelAdmin):
    
    raw_id_fields = ('user',)

    list_display = (
        'user',
        'payee',
    )