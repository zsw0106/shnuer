from django.urls import path
from . import views

# start with barter
urlpatterns = [
    # http://localhost:8000/barter/
    path('', views.barter_list, name='barter_list'),
    path('<int:barter_pk>', views.barter_detail, name="barter_detail"),
    path('add', views.add_barter, name="add_barter"),
    path('type/<int:barter_type_pk>', views.barter_with_type, name="barter_with_type"),
    path('personal_barters', views.personal_barters, name="personal_barters"),
    path('apply_barter', views.apply_barter, name='apply_barter'),
    path('my_application', views.my_application, name='my_application'),
    path('recive_apply', views.recive_apply, name='recive_apply'),
    path('reject_apply', views.reject_apply, name='reject_apply'),
    path('barter_delete/<int:id>/', views.barter_delete, name='barter_delete'),
    path('barter_update/<int:id>/', views.barter_update, name='barter_update')
]