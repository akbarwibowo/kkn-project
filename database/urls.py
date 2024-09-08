from django.urls import path
from . import views

urlpatterns = [
    path('database_home/', views.database_page, name='database_home'),
]
