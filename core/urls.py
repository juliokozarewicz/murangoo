from django.urls import path
from .views import about, features, contact, home, privacy_policy, service_terms


app_name = 'core'

urlpatterns = [
    path('', home.as_view(), name='home'),
    path('about-us', about, name='about-us'),
    path('features', features, name='features'),
    path('contact', contact.as_view(), name='contact'),
    path('privacy-policy', privacy_policy.as_view(), name='privacy_policy'),
    path('service-terms', service_terms.as_view(), name='service_terms'),
]
