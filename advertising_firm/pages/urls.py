from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', main, name='main_page'),
    path('sav_form/', sav_form, name='sav_form'),
    path('auth/', auth, name='auth'),
    path('sign_in/', sign_in, name='sign_in'),
    path('logout/', logout_func, name='logout'),
    path('create_appl/', create_appl, name='create_appl'),
    path('worker_view/', worker_view, name='worker_view'),
]
