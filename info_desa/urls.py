from django.urls import path
from . import views

urlpatterns = [
    path('add_info_page/<int:user_id>/', views.add_info_form, name='add_info_page'),
    path('add_info/<int:user_id>/', views.add_info, name='add_info'),
]

