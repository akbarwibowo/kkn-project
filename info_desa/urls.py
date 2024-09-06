from django.urls import path
from . import views

urlpatterns = [
    path('add_info_page/', views.add_info_form, name='add_info_page'),
    path('add_info/<int:user_id>/', views.add_info, name='add_info'),
    path('acc_form/<int:user_id>/', views.info_acc_form, name='acc_form'),
    path('acc_info/<int:info_id>/<int:user_id>/', views.info_acc, name='acc_info'),
    path('reject_info/<int:info_id>/<int:user_id>/', views.info_reject, name='reject_info'),
    path('revise_info/<int:info_id>/<int:user_id>/', views.info_revise, name='revise_info'),
    path('rejected_info/<int:user_id>/', views.info_feedback, name='rejected_info'),
    path('revision/<int:info_id>/', views.info_revision_form, name='revision'),
    path('revision_info_do/<int:info_id>/', views.info_do_revision, name='revision_info_do'),
]

