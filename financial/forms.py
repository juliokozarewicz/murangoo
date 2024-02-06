from django import forms
from.models import Table_invoices, Invoice_category, Invoice_bank, Card, Payee
from django.utils.translation import gettext_lazy as _


class Create_form(forms.ModelForm):
    
    def __init__(self, *args, request, **kwargs):
        super().__init__(*args, **kwargs)

        self.request = request

        self.fields['category'].choices = [('----------', '----------')] + [
            (item.invoice_category, item.invoice_category) for item in Invoice_category.objects.filter(user=request.user)
        ]

        self.fields['bank_account'].choices = [('----------', '----------')] + [
            (item.invoice_bank, item.invoice_bank) for item in Invoice_bank.objects.filter(user=request.user)
        ]

        self.fields['card'].choices = [('----------', '----------')] + [
            (item.card, item.card) for item in Card.objects.filter(user=request.user)
        ]

        self.fields['payee'].choices = [('----------', '----------')] + [
            (item.payee, item.payee) for item in Payee.objects.filter(user=request.user)
        ]

    category = forms.ChoiceField(
        required=False,
        choices=[],
    )

    bank_account = forms.ChoiceField(
        required=False,
        choices=[],
    )

    payee = forms.ChoiceField(
        required=False,
        choices=[],
    )

    card = forms.ChoiceField(
        required=False,
        choices=[],
    )

    repeat_check = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'id': 'checkboxrepeat',
            }
        ),
    )

    qtd_repeat = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'type': 'number',
                'id': 'id_qtd_repeat_st',
                'min': 1,
            }
        )
    )
    
    period_repeat = forms.ChoiceField(
    required=False,
    initial='----------',
    choices=[
        ('----------', '----------'),
        (_('monthly'), _('monthly')),
        (_('weekly'), _('weekly')),
        ],
    )

    def clean(self):
        cleaned_data = super().clean()

        qtd_repeat_clean = cleaned_data.get('qtd_repeat')
        repeat_check_clean = cleaned_data.get('repeat_check')
        period_repeat_clean = cleaned_data.get('period_repeat')

        if repeat_check_clean and qtd_repeat_clean is None:
            self.add_error('qtd_repeat', _('Needs to be an integer and cannot be empty.'))

        if repeat_check_clean and period_repeat_clean == '----------':
            self.add_error('period_repeat', _('Cannot be empty.'))

        return cleaned_data

    def clean_payment_amount(self):
        payment_amount = self.cleaned_data['payment_amount']
        posting_type = self.cleaned_data['posting_type']

        if posting_type == 'expense' and payment_amount > 0:
            payment_amount *= -1

        if posting_type == 'revenue' and payment_amount < 0:
            payment_amount *= -1

        return payment_amount

    class Meta:

        model = Table_invoices

        widgets = {

            'posting_type': forms.RadioSelect(attrs={
                'class': 'posting_type',
                'label': 'transaction type',
            }),

            'payment_description': forms.TextInput(attrs={
                'class': 'posting_type',
                'label': 'transaction type',
                'placeholder': _('Enter payment description'),
            }),

            'due_date': forms.DateInput(
                attrs={
                'type': 'int',
                'class': 'posting_type',
                'label': 'transaction type',
                'pattern': '[0-9/]*',
                'inputmode': 'numeric',
                'placeholder': _("MM/DD/YYYY"),
            }),

            'payment_amount': forms.TextInput(attrs={
                'type': 'int',
                'class': 'payment_amount',
                'label': 'payment amount',
                'placeholder': _('Enter payment amount'),
                'pattern': '[0-9.]*',
                'inputmode': 'numeric',
            }),

            'document_number': forms.TextInput(attrs={
                'class': 'document_number',
                'label': 'document_number',
                'placeholder': _('Enter the document number'),
            }),

            'notes': forms.Textarea(attrs={
                'class': 'notes',
                'label': 'notes',
                'placeholder': _('Enter something about this transaction'),
            }),
        }

        exclude = ('user',)

class Update_form(forms.ModelForm):
    def __init__(self, *args, request, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.request = request
        
        self.fields['category'].choices = [('----------', '----------')] + [
            (item.invoice_category, item.invoice_category) for item in Invoice_category.objects.filter(user=request.user)
        ]

        self.fields['bank_account'].choices = [('----------', '----------')] + [
            (item.invoice_bank, item.invoice_bank) for item in Invoice_bank.objects.filter(user=request.user)
        ]

        self.fields['card'].choices = [('----------', '----------')] + [
            (item.card, item.card) for item in Card.objects.filter(user=request.user)
        ]

        self.fields['payee'].choices = [('----------', '----------')] + [
            (item.payee, item.payee) for item in Payee.objects.filter(user=request.user)
        ]

    category = forms.ChoiceField(
        required=False,
        choices=[],
    )

    bank_account = forms.ChoiceField(
        required=False,
        choices=[],
    )

    payee = forms.ChoiceField(
        required=False,
        choices=[],
    )

    card = forms.ChoiceField(
        required=False,
        choices=[],
    )

    def clean_payment_amount(self):
        payment_amount = self.cleaned_data['payment_amount']
        posting_type = self.cleaned_data['posting_type']

        if posting_type == 'expense' and payment_amount > 0:
            payment_amount *= -1

        if posting_type == 'revenue' and payment_amount < 0:
            payment_amount *= -1

        return payment_amount

    class Meta:

        model = Table_invoices

        widgets = {

            'posting_type': forms.RadioSelect(attrs={
                'class': 'posting_type',
                'label': 'transaction type',
                'id': 'select_update',
            }),

            'payment_description': forms.TextInput(attrs={
                'class': 'posting_type',
                'label': 'transaction type',
                'placeholder': _('Enter payment description'),
            }),

            'due_date': forms.DateInput(
                attrs={
                'type': 'int',
                'class': 'posting_type',
                'label': 'transaction type',
                'pattern': '[0-9/]*',
                'inputmode': 'numeric',
                'placeholder': _("MM/DD/YYYY"),
            }),

            'payment_amount': forms.TextInput(attrs={
                'type': 'int',
                'class': 'payment_amount',
                'label': 'payment amount',
                'placeholder': _('Enter payment amount'),
                'pattern': '[0-9.]*',
                'inputmode': 'numeric',
            }),

            'document_number': forms.TextInput(attrs={
                'class': 'document_number',
                'label': 'document_number',
                'placeholder': _('Enter the document number'),
            }),

            'notes': forms.Textarea(attrs={
                'class': 'notes',
                'label': 'notes',
                'placeholder': _('Enter something about this transaction'),
            }),
        }

        exclude = ('user',)

class DateFilterForm(forms.Form):
    
    def __init__(self, *args, request, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.request = request
        
        self.fields['transaction_type'].choices = [
            ('revenue', _('revenue')),
            ('expense', _('expense')),
            ('all', _('all')),
        ]

        self.fields['selecteditemfinal'].choices = [('----------', '----------')] + [
            (item.invoice_category, item.invoice_category) for item in Invoice_category.objects.filter(user=request.user)
        ]

        self.fields['bankaccount'].choices = [('----------', '----------')] + [
            (item.invoice_bank, item.invoice_bank) for item in Invoice_bank.objects.filter(user=request.user)
        ]

        self.fields['card'].choices = [('----------', '----------')] + [
            (item.card, item.card) for item in Card.objects.filter(user=request.user)
        ]

        self.fields['statusacc'].choices = [('----------', '----------')] + [
            item for item in Table_invoices.STATUS_TYPES
        ]
        
        self.fields['order_search'].choices = [
            ('ascending', _('ascending')),
            ('descending', _('descending')),
        ]


    date_min = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'int',
                'class': 'posting_type',
                'label': 'transaction type',
                'pattern': '[0-9/]*',
                'inputmode': 'numeric',
                'placeholder': _("MM/DD/YYYY"),
            }
        )
    )

    date_max = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'int',
                'class': 'posting_type',
                'label': 'transaction type',
                'pattern': '[0-9/]*',
                'inputmode': 'numeric',
                'placeholder': _("MM/DD/YYYY"),
            }
        )
    )


    transaction_type = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.RadioSelect(attrs={'class': 'radiotypetransaction'})
    )

    selecteditemfinal = forms.ChoiceField(
        required=False,
        choices=[],
    )

    bankaccount = forms.ChoiceField(
        required=False,
        choices=[],
    )
    
    card = forms.ChoiceField(
        required=False,
        choices=[],
    )

    statusacc = forms.ChoiceField(
        required=False,
        choices=[],
    )
    
    order_search = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.RadioSelect(attrs={'class': 'radiotypetransaction'})
    )

class form_invoice_category(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(form_invoice_category, self).__init__(*args, **kwargs)

        self.fields['invoice_category'].widget.attrs.update(
            {
            'placeholder': _('Enter the category')
            }
        )

    class Meta:
        model = Invoice_category
        exclude = ('user',)

class form_invoice_bank(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(form_invoice_bank, self).__init__(*args, **kwargs)

        self.fields['invoice_bank'].widget.attrs.update(
            {
            'placeholder': _('Enter bank account')
            }
        )

    class Meta:
        model = Invoice_bank
        exclude = ('user',)
        
class form_invoice_card(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(form_invoice_card, self).__init__(*args, **kwargs)

        self.fields['card'].widget.attrs.update(
            {
            'placeholder': _('Enter credit card')
            }
        )

    class Meta:
        model = Card
        exclude = ('user',)
        
class form_invoice_payee(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(form_invoice_payee, self).__init__(*args, **kwargs)

        self.fields['payee'].widget.attrs.update(
            {
            'placeholder': _('Enter payee name')
            }
        )

    class Meta:
        model = Payee
        exclude = ('user',)