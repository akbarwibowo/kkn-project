from django.urls import path
from . import views

urlpatterns = [
    path('database_home/', views.database_page, name='database_home'),
    path('database_form/', views.database_form, name='database_form'),
    path('database_add_data/', views.database_add_data, name='database_add_data'),
    path('database_approval/', views.database_approval_page, name='database_approval_page'),
    path('database_approve/<int:batch_id>/', views.database_approve, name='database_approve'),
    path('database_revision/<int:batch_id>/', views.database_revision, name='database_revision'),
    path('database_feedback/', views.database_feedback, name='database_feedback'),
    path('database_revision_form/<int:batch_id>/', views.database_revision_form, name='database_revision_form'),
    path('database_revision_do/<int:batch_id>/', views.database_revision_do, name='database_revise_data'),
    path('database_delete/<int:resident_id>/', views.delete_data, name='database_delete'),
]
