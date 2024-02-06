from django.urls import path
from .views import (
    home_financial, list_invoice, delete_invoice, update_invoice, account_settings,
    settings_new_category, settings_update_category, settings_delete_cetegory,
    settings_new_bank, settings_update_bank, settings_delete_bank, settings_new_card,
    settings_update_card, settings_delete_card, settings_new_payee, settings_update_payee,
    settings_delete_payee
)


app_name = 'financial'

urlpatterns = [

    # home
    path('financial/', home_financial.as_view(), name='home_financial'),
    
    # account settings
    path('account-settings/', account_settings.as_view(), name='account_settings'),
    # category
    path('account-settings/new-category', settings_new_category.as_view(), name='settings_new_category'),
    path('account-settings/category/<int:pk>/update', settings_update_category.as_view(), name='settings_update_category'),
    path('account-settings/category/<int:pk>/delete', settings_delete_cetegory.as_view(), name='settings_delete_cetegory'),
    # bank acc
    path('account-settings/new-bank', settings_new_bank.as_view(), name='settings_new_bank'),
    path('account-settings/bank/<int:pk>/update', settings_update_bank.as_view(), name='settings_update_bank'),
    path('account-settings/bank/<int:pk>/delete', settings_delete_bank.as_view(), name='settings_delete_bank'),
    #card
    path('account-settings/new-card', settings_new_card.as_view(), name='settings_new_card'),
    path('account-settings/card/<int:pk>/update', settings_update_card.as_view(), name='settings_update_card'),
    path('account-settings/card/<int:pk>/delete', settings_delete_card.as_view(), name='settings_delete_card'),
    # payee
    path('account-settings/new-payee', settings_new_payee.as_view(), name='settings_new_payee'),
    path('account-settings/payee/<int:pk>/update', settings_update_payee.as_view(), name='settings_update_payee'),
    path('account-settings/payee/<int:pk>/delete', settings_delete_payee.as_view(), name='settings_delete_payee'),
    
    # financial page
    path('financial/invoices/', list_invoice, name='list_invoice'),
    path('financial/invoices/<int:pk>/delete/', delete_invoice.as_view(), name='delete_invoice'),
    path('financial/invoices/<int:pk>/update/', update_invoice.as_view(), name='update_invoice'),

]