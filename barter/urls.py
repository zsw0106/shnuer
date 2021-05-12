from django.urls import path
from . import views

# start with barter
urlpatterns = [
    # http://localhost:8000/barter/
    path('', views.barter_list, name='barter_list'),
    path('<int:barter_pk>', views.barter_detail, name="barter_detail"),
    path('add', views.add_barter, name="add_barter"),
    path('type/<int:barter_type_pk>', views.barter_with_type, name="barter_with_type"),
    path('apply_barter', views.apply_barter, name='apply_barter')
]