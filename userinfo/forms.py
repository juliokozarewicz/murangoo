from django import forms
from django.utils.translation import gettext_lazy as _
from allauth.account.forms import SignupForm
from .models import User_info, Account_plan, Subscription_history, plans_available
from django.db import transaction
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from datetime import timedelta


# Standard registration form
class MyCustomSignupForm(SignupForm):
    field_order = ['name', 'email', 'password1', 'password2']

    name = forms.CharField(
        label=_('Name'),
        max_length=250,
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter your full name'),
            'class': 'name',
            'style':
                """
                """,
        }))

    email = forms.EmailField(
        label=_('Email'),
        max_length=250,
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter your best email'),
            'class': 'email',
            'style':
                """
                """,
        }))

    @transaction.atomic
    def save(self, request):
        email = self.cleaned_data.get('email')
        name = self.cleaned_data.get('name')

        # Check if user exists
        if User.objects.filter(email=email).exists():
            user = super(MyCustomSignupForm, self).save(request)
            return user

        user = super(MyCustomSignupForm, self).save(request)

        # First register in Subscription_history
        date = timezone.now()
        plan = str('0')
        amount = plans_available['0']['value']
        status = 'renewed'
        number_month_trial = plans_available['0']['days_test'] // 30
        total_registers_trialacc = len([Subscription_history.objects.filter(user=user)])

        # Create or update user_info, Account_plan, plans_available
        user_info, created = User_info.objects.get_or_create(user=user, name=name)
        user_info, created = Account_plan.objects.get_or_create(user=user)

        while total_registers_trialacc <= number_month_trial:
            user_info, created = Subscription_history.objects.get_or_create(
                date=date,
                user=user,
                plan=plan,
                amount=amount,
                status=status
            )

            date += timedelta(days=30)
            total_registers_trialacc += 1
            
            user_info.save()

        return user

    def signup(self, request, user):
        # Call the standard method for 'signup' from SignupForm for finish.
        return super().signup(request, user)

# Data complement registration form
class Form_userinfo(forms.ModelForm):
    field_order = ['name', 'phone', 'country', 'date_of_birth', 'occupation', 'Biography',]

    name = forms.CharField(
        required=True,
        label=_('Name'),
        max_length=250,
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter your full name'),
            'class': 'name',
            'style':
                """
                """,
        }))

    occupation = forms.CharField(
        required=False,
        label=_('occupation'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': _("What's your profession?"),
            'class': 'occupation',
            'style':
                """
                """,
        }))

    date_of_birth = forms.DateField(
        required=False,
        label=_('date_of_birth'),
        widget=forms.DateInput(
            attrs={
                'type': 'int',
                'class': 'datefields',
                'label': 'transaction type',
                'pattern': '[0-9/]*',
                'inputmode': 'numeric',
                'placeholder': _("MM/DD/YYYY"),
            }
        )
    )
    
    biography = forms.CharField(
        required=False,
        label=_('biography'),
        max_length=700,
        widget=forms.Textarea(attrs={
            'placeholder': _("So, tell us a bit more about you. What's your story?"),
            'class': 'biography',
            'style':
                """
                """,
        }))

    phone = forms.CharField(
        required=False,
        label=_('Phone'),
        max_length=250,
        widget=forms.TextInput(attrs={
            'pattern': '[0-9/]*',
            'inputmode': 'numeric',
            'placeholder': _('Enter your phone number'),
            'class': 'phone',
        }))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Realizar a validação do número de telefone
        if not phone.isdigit():
            raise forms.ValidationError(_("Enter a valid phone number (numbers only)."))
        return phone
    
    class Meta:
        model = User_info
        exclude = ('user',)

class Form_delete_account(forms.Form):

    password_inserted = forms.CharField(
        label=_("current password"),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Current password"),
            }
        )
    )

    number_entered = forms.CharField(
        label=_("number sent"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Number sent to email"),
            }
        )
    )