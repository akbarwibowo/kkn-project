from django.urls import path
from . import views

urlpatterns = [
    path('event_page/<int:user_id>', views.event_page, name='event_page'),
    path('event_form/', views.add_event_form, name='add_event_form'),
    path('event_add/<int:user_id>', views.add_event, name='add_event'),
    path('event_acc_form/<int:user_id>', views.event_acc_form, name='event_acc_form'),
    path('event_accept/<int:event_id>/<int:user_id>', views.event_acc, name='event_accept'),
    path('event_reject/<int:event_id>/<int:user_id>', views.event_reject, name='event_reject'),
    path('event_revision/<int:event_id>/<int:user_id>', views.event_revision, name='event_revision'),
    path('event_feedback/<int:user_id>/', views.event_feedback, name='event_feedback'),
    path('event_revision_form/<int:event_id>', views.event_revision_form, name='event_revision_form'),
    path('event_do_revision/<int:event_id>', views.event_do_revision, name='event_do_revision'),
    path('event_delete/<int:event_id>', views.event_delete, name='event_delete'),
]
