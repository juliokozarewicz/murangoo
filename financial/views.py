from django.shortcuts import render
from .models import Table_invoices, Invoice_category, Invoice_bank, Card, Payee
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView, CreateView
from django.urls import reverse_lazy
from .forms import Create_form, DateFilterForm, Update_form, form_invoice_category, form_invoice_bank, form_invoice_card, form_invoice_payee
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from userinfo.views import accounts_release_verify
from django.shortcuts import redirect
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from dateutil.relativedelta import relativedelta



# Home financial (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class home_financial(TemplateView):
    template_name = 'financial/dashboards_financial.html'
    context_object_name = 'home_financial'

    # filter for user
    def get_queryset(self):
        return Table_invoices.objects.filter(user=self.request.user)
    
    # Get account plan
    def get(self, request, *args, **kwargs):
        is_release_verified = accounts_release_verify(request.user, request)

        if not is_release_verified:
            return redirect('/accounts/')

        return super().get(request, *args, **kwargs)
# -------------------------------------------------------------------------------------
# Home financial (END)

# Finance list (INIT)
# -------------------------------------------------------------------------------------
@login_required
def list_invoice(request):
    template_name = 'financial/list_invoice.html'

    # Get account plan (INIT)
    # -------------------------------------------------------------------------------------
    is_release_verified = accounts_release_verify(request.user, request)

    if not is_release_verified:
        return redirect('/accounts/')

    # -------------------------------------------------------------------------------------
    # Get account plan (END)
    
    # Data for the top cards
    # -------------------------------------------------------------------------------------
    context = {}
    revenues = Table_invoices.objects.filter(user=request.user, posting_type='revenue').aggregate(total=Sum('payment_amount'))['total']
    expenses = Table_invoices.objects.filter(user=request.user, posting_type='expense').aggregate(total=Sum('payment_amount'))['total']
    context['template_balance'] = (revenues or 0) + (expenses or 0)
    context['template_revenues'] = revenues or 0
    context['template_expenses'] = expenses or 0
    # -------------------------------------------------------------------------------------

    # Date filter for form
    # -------------------------------------------------------------------------------------
    today = datetime.today()
    first_day = today.replace(day=1)

    if first_day.month == 12:
        next_month = first_day.replace(year=first_day.year + 1, month=1, day=1)
    else:
        next_month = first_day.replace(month=first_day.month + 1, day=1)

    last_day = next_month - timedelta(days=1)
    # -------------------------------------------------------------------------------------

    # Overdue invoices
    # -------------------------------------------------------------------------------------
    overdue_status = Table_invoices.objects.filter(
        user=request.user,
        due_date__gte=first_day,
        due_date__lte=last_day
    )

    for line in overdue_status:

        if line.status == 'pending' and line.due_date < datetime.now().date():
            line.status = 'overdue'
            line.save()

        if line.status == 'overdue' and line.due_date >= datetime.now().date():
            line.status = 'pending'
            line.save()
    # -------------------------------------------------------------------------------------

    # New invoice form (INIT)
    # -------------------------------------------------------------------------------------
    if request.method == 'POST':

        form_new_invoice = Create_form(request.POST, request=request)

        if form_new_invoice.is_valid():

            # If repeat is active
            if form_new_invoice.cleaned_data['repeat_check']:

                qtd_repeat_number = form_new_invoice.cleaned_data['qtd_repeat']
                period_repeat = form_new_invoice.cleaned_data['period_repeat']

                init_repeat = 1
                data_for_repeat = form_new_invoice.cleaned_data['due_date']

                while init_repeat <= qtd_repeat_number:

                    if period_repeat == _('weekly'):

                        new_data = data_for_repeat + timedelta(days=7)

                        data_object_repeat = Table_invoices(
                            user=request.user,
                            posting_type=form_new_invoice.cleaned_data['posting_type'],
                            payment_description=form_new_invoice.cleaned_data['payment_description'] + f' ({init_repeat+1}/{qtd_repeat_number+1})',
                            payment_amount=form_new_invoice.cleaned_data['payment_amount'],
                            due_date=new_data,
                            payee=form_new_invoice.cleaned_data['payee'],
                            document_number=form_new_invoice.cleaned_data['document_number'],
                            category=form_new_invoice.cleaned_data['category'],
                            bank_account=form_new_invoice.cleaned_data['bank_account'],
                            card=form_new_invoice.cleaned_data['card'],
                            notes=form_new_invoice.cleaned_data['notes'],
                            status=form_new_invoice.cleaned_data['status']
                        )

                        data_object_repeat.save()

                        init_repeat += 1
                        data_for_repeat = new_data

                    if period_repeat == _('monthly'):

                        new_data = data_for_repeat + relativedelta(months=1)

                        data_object_repeat = Table_invoices(
                            user=request.user,
                            posting_type=form_new_invoice.cleaned_data['posting_type'],
                            payment_description=form_new_invoice.cleaned_data['payment_description'] + f' ({init_repeat+1}/{qtd_repeat_number+1})',
                            payment_amount=form_new_invoice.cleaned_data['payment_amount'],
                            due_date=new_data,
                            payee=form_new_invoice.cleaned_data['payee'],
                            document_number=form_new_invoice.cleaned_data['document_number'],
                            category=form_new_invoice.cleaned_data['category'],
                            bank_account=form_new_invoice.cleaned_data['bank_account'],
                            card=form_new_invoice.cleaned_data['card'],
                            notes=form_new_invoice.cleaned_data['notes'],
                            status=form_new_invoice.cleaned_data['status']
                        )

                        data_object_repeat.save()

                        init_repeat += 1
                        data_for_repeat = new_data

            # insert data form
            if form_new_invoice.cleaned_data['repeat_check']:
                object_commit = Table_invoices(
                            user=request.user,
                            posting_type=form_new_invoice.cleaned_data['posting_type'],
                            payment_description=form_new_invoice.cleaned_data['payment_description'] + f' (1/{qtd_repeat_number+1})',
                            payment_amount=form_new_invoice.cleaned_data['payment_amount'],
                            due_date=form_new_invoice.cleaned_data['due_date'],
                            payee=form_new_invoice.cleaned_data['payee'],
                            document_number=form_new_invoice.cleaned_data['document_number'],
                            category=form_new_invoice.cleaned_data['category'],
                            bank_account=form_new_invoice.cleaned_data['bank_account'],
                            card=form_new_invoice.cleaned_data['card'],
                            notes=form_new_invoice.cleaned_data['notes'],
                            status=form_new_invoice.cleaned_data['status']
                        )
            else:
                object_commit = Table_invoices(
                            user=request.user,
                            posting_type=form_new_invoice.cleaned_data['posting_type'],
                            payment_description=form_new_invoice.cleaned_data['payment_description'],
                            payment_amount=form_new_invoice.cleaned_data['payment_amount'],
                            due_date=form_new_invoice.cleaned_data['due_date'],
                            payee=form_new_invoice.cleaned_data['payee'],
                            document_number=form_new_invoice.cleaned_data['document_number'],
                            category=form_new_invoice.cleaned_data['category'],
                            bank_account=form_new_invoice.cleaned_data['bank_account'],
                            card=form_new_invoice.cleaned_data['card'],
                            notes=form_new_invoice.cleaned_data['notes'],
                            status=form_new_invoice.cleaned_data['status']
                        )

            obj = object_commit.save()

            response = redirect('/financial/invoices/')
            response.set_cookie('statusNewInvoice', 'statusNewInvoiceCLOSED')

            return response

    else:
        form_new_invoice = Create_form(request=request)

    context['form_new_invoice'] = form_new_invoice
    # -------------------------------------------------------------------------------------
    # New invoice form (END)   

    # Form filter requested by user (INIT)
    # -------------------------------------------------------------------------------------
    form = DateFilterForm(request.GET, request=request)

    if form.is_valid():

        if (
            form.cleaned_data['date_min'] or
            form.cleaned_data['date_max'] or
            form.cleaned_data['transaction_type'] or
            form.cleaned_data['selecteditemfinal'] or
            form.cleaned_data['bankaccount'] or
            form.cleaned_data['card'] or
            form.cleaned_data['order_search']
            ):

            if form.cleaned_data['order_search']:
                if form.cleaned_data['order_search'] == 'ascending':
                    order_filter = 'due_date'
                else:
                    order_filter = '-due_date'                    
            else:
                order_filter = 'due_date'
                
            if form.cleaned_data['date_min']:
                date_min = form.cleaned_data['date_min']
            else:
                date_min = first_day

            if form.cleaned_data['date_max']:
                date_max = form.cleaned_data['date_max']
            else:
                date_max = last_day

            if form.cleaned_data['transaction_type']:
                if form.cleaned_data['transaction_type'] == 'all':
                    transaction_type = ['revenue','expense']
                else:
                    transaction_type = [form.cleaned_data['transaction_type']]
            else:
                transaction_type = ['revenue', 'expense']

            if form.cleaned_data['selecteditemfinal']:
                if form.cleaned_data['selecteditemfinal'] == '----------':
                    selecteditemfinal = ''            
                else:
                    selecteditemfinal = form.cleaned_data['selecteditemfinal']
            else:
                selecteditemfinal = ''

            if form.cleaned_data['bankaccount']:
                if form.cleaned_data['bankaccount'] == '----------':
                    bankaccount = ''
                else:
                    bankaccount = form.cleaned_data['bankaccount']
            else:
                bankaccount = ''

            if form.cleaned_data['card']:
                if form.cleaned_data['card'] == '----------':
                    card = ''
                else:
                    card = form.cleaned_data['card']
            else:
                card = ''

            if form.cleaned_data['statusacc']:
                if form.cleaned_data['statusacc'] == '----------':
                    statusacc = ''
                else:
                    statusacc = form.cleaned_data['statusacc']
            else:
                statusacc = ''

            overdue_status = Table_invoices.objects.filter(
                user=request.user,
                due_date__gte=date_min,
                due_date__lte=date_max
            )

            for line in overdue_status:

                if line.status == 'pending' and line.due_date < datetime.now().date():
                    line.status = 'overdue'
                    line.save()

                if line.status == 'overdue' and line.due_date >= datetime.now().date():
                    line.status = 'pending'
                    line.save()

            context['dados'] = Table_invoices.objects.filter(
                user=request.user,
                due_date__gte=date_min,
                due_date__lte=date_max,
                posting_type__in=transaction_type,
                **({'category__iexact': selecteditemfinal} if selecteditemfinal else {}),
                **({'bank_account__iexact': bankaccount} if bankaccount else {}),
                **({'card__iexact': card} if card else {}),
                **({'status__iexact': statusacc} if statusacc else {}),
                ).order_by(order_filter)

        else:
            context['dados'] = Table_invoices.objects.filter(
                user=request.user,
                due_date__gte=first_day,
                due_date__lte=last_day
            ).order_by('due_date')

    context['form'] = form
    # -------------------------------------------------------------------------------------
    # Form filter requested by user (END)

    # clear repeated dates for mobile
    # -------------------------------------------------------------------------------------
    try:
        datelistunique = []
        for daterepeat in context['dados']:
            if daterepeat.due_date not in datelistunique:
                datelistunique.append(daterepeat.due_date)

        context['date_mobile'] = datelistunique
    except:
        error_message = _('No changes were made, check!')
        messages.add_message(request, messages.ERROR, error_message)
        return redirect('/financial/invoices')
    # -------------------------------------------------------------------------------------

    return render(request, template_name, context)
# -------------------------------------------------------------------------------------
# Finance list (END)

# Delete (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class delete_invoice(DeleteView): 
    model = Table_invoices
    template_name = 'financial/delete_invoice.html'
    context_object_name = 'delete_invoice'
    success_url = reverse_lazy('financial:list_invoice')

    # messages
    success_message = _('Successfully deleted.')
    error_message = _('No changes were made, check!')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(reverse_lazy('financial:list_invoice'))

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, self.success_message)
        return super().form_valid(form)

    # filter for user
    def get_queryset(self):
        return Table_invoices.objects.filter(user=self.request.user)
# -------------------------------------------------------------------------------------
# Delete (END)

# Update (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class update_invoice(SuccessMessageMixin, UpdateView):
    template_name = 'financial/update_invoice.html'
    context_object_name = 'update_invoice'
    form_class = Update_form
    model = Table_invoices
    success_message = _('Successfully changed.')
    error_message = _('No changes were made, check!')

    # Seleciona o usuario logado
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(reverse_lazy('financial:list_invoice'))
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # Passa o objeto request para o formulário
        return kwargs

    # filter for user
    def get_queryset(self):
        return Table_invoices.objects.filter(user=self.request.user)
# -------------------------------------------------------------------------------------
# Update (END)

# Account settings (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class account_settings(TemplateView):
    template_name = 'financial/account_settings.html'
    context_object_name = 'account_settings'

    # Context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Invoice_category'] = Invoice_category.objects.filter(user=self.request.user).order_by('invoice_category')
        context['Invoice_bank'] = Invoice_bank.objects.filter(user=self.request.user).order_by('invoice_bank')
        context['Credit_card'] = Card.objects.filter(user=self.request.user).order_by('card')
        context['payees'] = Payee.objects.filter(user=self.request.user).order_by('payee')
        return context

    # filter for user
    def get_queryset(self):
        return Table_invoices.objects.filter(user=self.request.user)

    # Get account plan
    def get(self, request, *args, **kwargs):
        is_release_verified = accounts_release_verify(request.user, request)

        if not is_release_verified:
            return redirect('/accounts/')

        return super().get(request, *args, **kwargs)
# -------------------------------------------------------------------------------------
# Account settings (END)

# Account settings new category (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class settings_new_category(CreateView):
    template_name = 'financial/category_new.html'
    context_object_name = 'settings_new_category'
    model = Invoice_category
    form_class = form_invoice_category
    success_url = reverse_lazy('financial:account_settings')

    success_message = _('Successfully inserted.')
    error_message = _('No changes were made, check!')

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, self.success_message)
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(reverse_lazy('financial:account_settings'))

    # filter for user
    def get_queryset(self):
        return Invoice_category.objects.filter(user=self.request.user)

    # Get account plan
    def get(self, request, *args, **kwargs):
        is_release_verified = accounts_release_verify(request.user, request)

        if not is_release_verified:
            return redirect('/accounts/')

        return super().get(request, *args, **kwargs)
# -------------------------------------------------------------------------------------
# Account settings new category (END)

# Account settings update category (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class settings_update_category(UpdateView):
    template_name = 'financial/category_update.html'
    context_object_name = 'settings_update_category'
    model = Invoice_category
    form_class = form_invoice_category
    success_url = reverse_lazy('financial:account_settings')

    success_message = _('Successfully changed.')
    error_message = _('No changes were made, check!')

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, self.success_message)
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(reverse_lazy('financial:account_settings'))

    # filter for user
    def get_queryset(self):
        return Invoice_category.objects.filter(user=self.request.user)

    # Get account plan
    def get(self, request, *args, **kwargs):
        is_release_verified = accounts_release_verify(request.user, request)

        if not is_release_verified:
            return redirect('/accounts/')

        return super().get(request, *args, **kwargs)
# -------------------------------------------------------------------------------------
# Account settings update category (END)

# Account settings delete category (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class settings_delete_cetegory(DeleteView): 
    model = Invoice_category
    context_object_name = 'settings_delete_cetegory'
    success_url = reverse_lazy('financial:account_settings')

    # messages
    success_message = _('Successfully deleted.')
    error_message = _('No changes were made, check!')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(reverse_lazy('financial:account_settings'))

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, self.success_message)
        return super().form_valid(form)

    # filter for user
    def get_queryset(self):
        return Invoice_category.objects.filter(user=self.request.user)
# -------------------------------------------------------------------------------------
# Account settings delete category

# Account settings new bank (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class settings_new_bank(CreateView):
    template_name = 'financial/bank_new.html'
    context_object_name = 'settings_new_bank'
    model = Invoice_bank
    form_class = form_invoice_bank
    success_url = reverse_lazy('financial:account_settings')

    success_message = _('Successfully inserted.')
    error_message = _('No changes were made, check!')

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, self.success_message)
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(reverse_lazy('financial:account_settings'))

    # filter for user
    def get_queryset(self):
        return Invoice_bank.objects.filter(user=self.request.user)

    # Get account plan
    def get(self, request, *args, **kwargs):
        is_release_verified = accounts_release_verify(request.user, request)

        if not is_release_verified:
            return redirect('/accounts/')

        return super().get(request, *args, **kwargs)
# -------------------------------------------------------------------------------------
# Account settings new bank (END)

# Account settings update bank (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class settings_update_bank(UpdateView):
    template_name = 'financial/bank_update.html'
    context_object_name = 'settings_update_bank'
    model = Invoice_bank
    form_class = form_invoice_bank
    success_url = reverse_lazy('financial:account_settings')

    success_message = _('Successfully changed.')
    error_message = _('No changes were made, check!')

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, self.success_message)
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(reverse_lazy('financial:account_settings'))

    # filter for user
    def get_queryset(self):
        return Invoice_bank.objects.filter(user=self.request.user)

    # Get account plan
    def get(self, request, *args, **kwargs):
        is_release_verified = accounts_release_verify(request.user, request)

        if not is_release_verified:
            return redirect('/accounts/')

        return super().get(request, *args, **kwargs)
# -------------------------------------------------------------------------------------
# Account settings update bank (END)

# Account settings delete bank (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class settings_delete_bank(DeleteView): 
    model = Invoice_bank
    context_object_name = 'settings_delete_bank'
    success_url = reverse_lazy('financial:account_settings')

    # messages
    success_message = _('Successfully deleted.')
    error_message = _('No changes were made, check!')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(reverse_lazy('financial:account_settings'))

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, self.success_message)
        return super().form_valid(form)

    # filter for user
    def get_queryset(self):
        return Invoice_bank.objects.filter(user=self.request.user)
# -------------------------------------------------------------------------------------
# Account settings delete bank

# Account settings new card (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class settings_new_card(CreateView):
    template_name = 'financial/card_new.html'
    context_object_name = 'settings_new_card'
    model = Card
    form_class = form_invoice_card
    success_url = reverse_lazy('financial:account_settings')

    success_message = _('Successfully inserted.')
    error_message = _('No changes were made, check!')

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, self.success_message)
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(reverse_lazy('financial:account_settings'))

    # filter for user
    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    # Get account plan
    def get(self, request, *args, **kwargs):
        is_release_verified = accounts_release_verify(request.user, request)

        if not is_release_verified:
            return redirect('/accounts/')

        return super().get(request, *args, **kwargs)
# -------------------------------------------------------------------------------------
# Account settings new card (END)

# Account settings update card (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class settings_update_card(UpdateView):
    template_name = 'financial/card_update.html'
    context_object_name = 'settings_update_card'
    model = Card
    form_class = form_invoice_card
    success_url = reverse_lazy('financial:account_settings')

    success_message = _('Successfully changed.')
    error_message = _('No changes were made, check!')

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, self.success_message)
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(reverse_lazy('financial:account_settings'))

    # filter for user
    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    # Get account plan
    def get(self, request, *args, **kwargs):
        is_release_verified = accounts_release_verify(request.user, request)

        if not is_release_verified:
            return redirect('/accounts/')

        return super().get(request, *args, **kwargs)
# -------------------------------------------------------------------------------------
# Account settings update card (END)

# Account settings delete card (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class settings_delete_card(DeleteView): 
    model = Card
    context_object_name = 'settings_delete_card'
    success_url = reverse_lazy('financial:account_settings')

    # messages
    success_message = _('Successfully deleted.')
    error_message = _('No changes were made, check!')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(reverse_lazy('financial:account_settings'))

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, self.success_message)
        return super().form_valid(form)

    # filter for user
    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)
# -------------------------------------------------------------------------------------
# Account settings delete card

# Account settings new payee (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class settings_new_payee(CreateView):
    template_name = 'financial/payee_new.html'
    context_object_name = 'settings_new_payee'
    model = Payee
    form_class = form_invoice_payee
    success_url = reverse_lazy('financial:account_settings')

    success_message = _('Successfully inserted.')
    error_message = _('No changes were made, check!')

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, self.success_message)
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(reverse_lazy('financial:account_settings'))

    # filter for user
    def get_queryset(self):
        return Payee.objects.filter(user=self.request.user)

    # Get account plan
    def get(self, request, *args, **kwargs):
        is_release_verified = accounts_release_verify(request.user, request)

        if not is_release_verified:
            return redirect('/accounts/')

        return super().get(request, *args, **kwargs)
# -------------------------------------------------------------------------------------
# Account settings new payee (END)

# Account settings update payee (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class settings_update_payee(UpdateView):
    template_name = 'financial/payee_update.html'
    context_object_name = 'settings_update_payee'
    model = Payee
    form_class = form_invoice_payee
    success_url = reverse_lazy('financial:account_settings')

    success_message = _('Successfully changed.')
    error_message = _('No changes were made, check!')

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, self.success_message)
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(reverse_lazy('financial:account_settings'))

    # filter for user
    def get_queryset(self):
        return Payee.objects.filter(user=self.request.user)

    # Get account plan
    def get(self, request, *args, **kwargs):
        is_release_verified = accounts_release_verify(request.user, request)

        if not is_release_verified:
            return redirect('/accounts/')

        return super().get(request, *args, **kwargs)
# -------------------------------------------------------------------------------------
# Account settings update payee (END)

# Account settings delete payee (INIT)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class settings_delete_payee(DeleteView): 
    model = Payee
    context_object_name = 'settings_delete_payee'
    success_url = reverse_lazy('financial:account_settings')

    # messages
    success_message = _('Successfully deleted.')
    error_message = _('No changes were made, check!')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return redirect(reverse_lazy('financial:account_settings'))

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, self.success_message)
        return super().form_valid(form)

    # filter for user
    def get_queryset(self):
        return Payee.objects.filter(user=self.request.user)
# -------------------------------------------------------------------------------------
# Account settings delete payee