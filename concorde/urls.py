from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePage, name="Home-Page"),
    path('about/', AboutPage, name="About-Page"),
    path('contact/', ContactPage, name="Contact-Page"),
    path('thanks/', ThanksPage, name="Thanks-Page"),
    path('coming-soon/', ComingsoonPage, name="Comingsoon-Page"),
]