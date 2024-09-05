from django.urls import path
from . import views

urlpatterns = [
    path('add_info_page/', views.add_info_form, name='add_info_page'),
    path('add_info/<int:user_id>/', views.add_info, name='add_info'),
    path('acc_form/<int:user_id>/', views.info_acc_form, name='acc_form'),
    path('acc_info/<int:info_id>/<int:user_id>/', views.info_acc, name='acc_info'),
]

