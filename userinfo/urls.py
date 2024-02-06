from django.urls import path
from .views import Edit_profile, Payments_page, delete_account, deleteacc_sendemail_code

app_name = 'userinfo'

urlpatterns = [
    path('dfg653d4qpzdfvgdbcAAAvbrqepol3425983274xcxzcCXZCAwef869g452152ewr1465re4t654ui654o3g25mj1b2n1fg3h1df56g4df65g1fgh125fg63h1fgh2fghfg/<int:pk>/edit/', Edit_profile.as_view(), name='edit_profile'),
    path('payments', Payments_page.as_view(), name='payments'),
    path('delete-account', delete_account, name='delete_account'),
    path('delete-account_numberemail', deleteacc_sendemail_code, name='deleteacc_sendemail_code'),
]