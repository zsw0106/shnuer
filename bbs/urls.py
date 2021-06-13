from django.urls import path
from . import views

# start with bbs
urlpatterns = [
    # http://localhost:8000/bbs/
    path('', views.bbs_list, name='bbs_list'),
    path('<int:bbs_pk>', views.bbs_detail, name="bbs_detail"),
    path('add', views.add_bbs, name="add_bbs"),
    path('type/<int:bbs_type_pk>', views.bbss_with_type, name="bbss_with_type"),
    path('date/<int:year>/<int:month>', views.bbss_with_date, name="bbss_with_date"),
    path('personal_bbs', views.personal_bbs, name="personal_bbs"),
    path('bbs_delete/<int:id>/', views.bbs_delete, name='bbs_delete'),
    path('bbs_update/<int:id>/', views.bbs_update, name='bbs_update'),
]