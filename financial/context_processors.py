from .models import Table_invoices
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _
import calendar


def get_month_name():
    data_atual = datetime.now()

    month_number = data_atual.month

    month_name = _(calendar.month_name[month_number])

    return month_name

def get_year_name():
    data_atual = datetime.now()

    year_number = data_atual.year

    year_name = str(year_number)

    return year_name


def global_context_financial(request):

    try:
        context = {}

        # Date filter for form
        # -------------------------------------------------------------------------------------
        context['GLOBAL_month_name'] = get_month_name()
        context['GLOBAL_year_name'] = get_year_name()
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

        # model query
        # -------------------------------------------------------------------------------------
        revenues = Table_invoices.objects.filter(
            user=request.user,
            posting_type='revenue',
            due_date__gte=first_day,
            due_date__lte=last_day,
        ).aggregate(total=Sum('payment_amount'))['total']

        expenses = Table_invoices.objects.filter(
            user=request.user,
            posting_type='expense',
            due_date__gte=first_day,
            due_date__lte=last_day,
        ).aggregate(total=Sum('payment_amount'))['total']

        expenses_top_five = Table_invoices.objects.filter(
            user=request.user,
            posting_type='expense',
            due_date__gte=first_day,
            due_date__lte=last_day,
        ).order_by('payment_amount')[:5]
        
        
        expenses_category = Table_invoices.objects.filter(
            user=request.user,
            posting_type='expense',
            due_date__gte=first_day,
            due_date__lte=last_day,
        ).values("category").annotate(payment_amount=Sum("payment_amount"))

        expenses_cards = Table_invoices.objects.filter(
            user=request.user,
            posting_type='expense',
            due_date__gte=first_day,
            due_date__lte=last_day,
        ).values("card").annotate(payment_amount=Sum("payment_amount"))

        # -------------------------------------------------------------------------------------

        # context final
        # -------------------------------------------------------------------------------------
        context['GLOBAL_template_balance'] = (revenues or 0) + (expenses or 0)
        context['GLOBAL_template_revenues'] = revenues or 0
        context['GLOBAL_template_expenses'] = expenses or 0

        # top five expenses
        context['GLOBAL_top_five_expenses'] = []

        position = 1

        for expense in expenses_top_five:

            percentage = "{:.2f}".format(float(expense.payment_amount / expenses) * 100)

            context['GLOBAL_top_five_expenses'].append(
                [
                    f'{position}°',
                    expense.payment_description,
                    percentage,
                    expense.payment_amount,
                ]
            )

            position += 1

        # group by category
        context['GLOBAL_expenses_categories'] = { 'label':[], 'dados':[] }

        for line in expenses_category:

            if line['category'] == '----------':
                line['category'] = _('others')

            context['GLOBAL_expenses_categories']['label'].append(
                str(line['category'])
            )

            context['GLOBAL_expenses_categories']['dados'].append(
                float(line['payment_amount'])
            )

        # credit card spending
        context['GLOBAL_credit_card'] = { 'label':[], 'dados':[] }

        for line in expenses_cards:

            if line['card'] == '----------':
                continue

            if line['payment_amount'] < 0:
                line['payment_amount'] = line['payment_amount'] * -1

            context['GLOBAL_credit_card']['label'].append(
                str(line['card'])
            )

            context['GLOBAL_credit_card']['dados'].append(
                float(line['payment_amount'])
            )

        # -------------------------------------------------------------------------------------

        return context

    except:
        context['GLOBAL_template_balance'] = '0'
        context['GLOBAL_template_revenues'] = '0'
        context['GLOBAL_template_expenses'] = '0'
        context['GLOBAL_top_five_expenses'] = '0'

        return context