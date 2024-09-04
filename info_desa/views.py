from django.shortcuts import render, redirect
from registration.models import UserExtend
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Information
from datetime import date

# Create your views here.


def home(request):
    return render(request, 'home.html')


def add_info_form(request, user_id):
    user_type = UserExtend.objects.filter(user_id=user_id).values('user_type').first()['user_type']

    if user_type == 'user':
        return render(request, 'home.html', context={'message': 'You are not allowed to access this page'})

    return render(request, 'add_info_form.html', context={'user_id': user_id})


def add_info(request, user_id):
    if request.method == 'POST':
        try:
            info_name = request.POST.get('info_name')
            info_description = request.POST.get('info_description')
            info_image = request.FILES.get('info_image')
            info_date = date.today()
            info = Information(
                info_name=info_name,
                info_description=info_description,
                info_created_date=info_date,
                info_image=info_image,
                user=UserExtend.objects.get(user_id=user_id),
            )
            info.save()

            return redirect('home')
        except Exception as e:
            return render(request, 'add_info_form.html', context={'message': e})
    return render(request, 'add_info_form.html')
