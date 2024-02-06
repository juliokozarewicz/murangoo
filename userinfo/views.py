from .models import User_info, Account_plan, plans_available, Subscription_history
from .forms import Form_userinfo, Form_delete_account
from django.views.generic import UpdateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Succes message
from django.contrib import messages
from django.http import HttpResponseRedirect

# Others imports
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import logout
from decouple import config

# email
from django.core.mail import send_mail
import random
import string


# Edit profile (page)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class Edit_profile(UpdateView): 
    model = User_info
    template_name = 'userinfo/profile.html'
    context_object_name = 'edit_profile'
    form_class = Form_userinfo

    def form_valid(self, form):
      messages.success(self.request, _("Your profile has been updated."))
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

    # filter for user
    def get_queryset(self):
        return User_info.objects.filter(user=self.request.user)
# -------------------------------------------------------------------------------------


# Payments (page)
# -------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class Payments_page(TemplateView): 
    template_name = 'userinfo/payments.html'
    context_object_name = 'payments'

    # apply filters
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Account plan
        context['template_account_plan'] = self.get_queryset()['get_account_plan']

        # Plan value
        filter_user = self.get_queryset()['get_account_plan'].plan
        context['template_account_value'] = plans_available[str(filter_user)]['value']

        # Limit date
        context['date_limit_plan'] = self.get_queryset()['get_account_plan'].date_limit_plan
        
        # Plan hostory
        context['template_plan_history'] = self.get_queryset()['get_plan_history']

        return context

    # filters
    def get_queryset(self):

        search = {
          'get_account_plan': Account_plan.objects.filter(user=self.request.user).first(),
          'get_plan_history': Subscription_history.objects.filter(user=self.request.user).order_by('-date'),
        }

        return search
# -------------------------------------------------------------------------------------


# Account release verify
# -------------------------------------------------------------------------------------
def accounts_release_verify(user, request):
    accounts_release = list(plans_available.keys())[ 1: ]
    current_plan = Account_plan.objects.filter(user=request.user).first().plan
    date_created_perfil = Account_plan.objects.filter(user=request.user).first().created

    # Conditions to trial account (INIT)
    date_current = timezone.now()
    date_limit_plan = Account_plan.objects.filter(user=request.user).first().date_limit_plan

    if current_plan == '0' and date_current >= date_limit_plan:
      return False

    if current_plan == '0' and date_current < date_limit_plan:
      return True
    # Conditions to trial account (END)

    # last condition for granting access (INIT)
    if current_plan in accounts_release:
      return True

    else:
      return False
    # last condition for granting access (END)
# -------------------------------------------------------------------------------------


# Delete account
# -------------------------------------------------------------------------------------
@login_required
def deleteacc_sendemail_code(request):

  # temporary code
  temporary_code = ''.join(random.choice(string.digits) for _ in range(6))
  request.session['number_sent_email'] = temporary_code
  temporary_code_send = request.session['number_sent_email']

  subject = _('MURANGOO: Account deletion code')
  message = _('Your code to delete your account is: ') + temporary_code_send + '\n\n\nMURANGOO | Financial'
  from_email = config('EMAIL_HOST_USER')
  recipient_list = [request.user.email]

  send_mail(subject, message, from_email, recipient_list)
  
  return redirect('/')

@login_required
def delete_account(request):
    template_name = 'userinfo/delete_acc.html'
    context = {}

    # session variable to count fairule access
    request.session.setdefault('acess_count_error', 0)

    # messages
    success_message = _('Your account has been successfully deleted.')
    error_message = _('No changes were made, check!')
    error_password = _("The password entered does not match the user's password.")
    many_access = _("You were logged out because you exceeded the attempt limit. Be careful, your account will be blocked.")
    invalid_number = _('The number entered is not the same as the number sent to your email, repeat the process!')

    if request.method == 'POST':

      # Password inserted form (INIT)
      # ------------------------------------------------------------------------------------------------
      form_delete_account = Form_delete_account(request.POST)

      if form_delete_account.is_valid():

          password_inserted = form_delete_account.cleaned_data.get('password_inserted')
          number_entered = form_delete_account.cleaned_data.get('number_entered')

          if request.user.check_password(password_inserted):

            number_sent_email = request.session.get('number_sent_email')

            if number_entered == number_sent_email:

              # DELETE USER
              # -----------------------------------------
              request.user.delete()
              
              # warning acc delete
              subject_del = _('MURANGOO: Account deletion')
              message_del = _("Your account has been successfully deleted from our app. Your data has all been deleted and there is no longer any record of you with us. Thank you for spending this time with us.") + "\n\n\nMURANGOO | Financial"
              from_email_del = config('EMAIL_HOST_USER')
              recipient_list_del = [request.user.email]
              send_mail(subject_del, message_del, from_email_del, recipient_list_del)
              
              logout(request)
              # -----------------------------------------

              messages.add_message(request, messages.INFO, success_message)
              return redirect('/accounts/login')

            else:
              messages.add_message(request, messages.ERROR, invalid_number)
              return redirect(reverse_lazy('account_manager'))

          else:

            if request.session['acess_count_error'] >= 2:

              messages.add_message(request, messages.ERROR, many_access)

              # warning many acess
              subject = _('MURANGOO: Attention! Someone is trying to delete your account')
              message = _("Attention! Someone is trying to delete your account. Since attempts to delete your account using your password have already been exceeded, you have been logged out. If you are not trying to delete your account, please change your password!") + "\n\n\nMURANGOO | Financial"
              from_email = config('EMAIL_HOST_USER')
              recipient_list = [request.user.email]
              send_mail(subject, message, from_email, recipient_list)

              # logout
              logout(request)

              return redirect('/accounts/login')

            request.session['acess_count_error'] += 1
            messages.add_message(request, messages.ERROR, error_password)

            return redirect(reverse_lazy('account_manager'))

      else:
          messages.add_message(request, messages.ERROR, error_message)
          return redirect(reverse_lazy('account_manager'))

      # ------------------------------------------------------------------------------------------------
      # Password inserted form (END)

    else:
        form_delete_account = Form_delete_account()

    context['form_delete_account'] = form_delete_account

    return render(request, template_name, context)