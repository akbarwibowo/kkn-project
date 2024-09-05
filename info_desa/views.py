from django.shortcuts import render, redirect
from registration.models import UserExtend
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Information
from datetime import date
import base64
from PIL import Image
import io

# Create your views here.


def home(request):
    informations = Information.objects.filter(approved=True).order_by('-info_created_date').values()
    for info in informations:
        info['info_image'] = base64.b64encode(info['info_image']).decode('utf-8')
    if informations is None or len(informations) == 0:
        message = "There is no information available"
        return render(request, 'home.html', context={'message': message})
    context = {
        'informations': informations,
    }
    return render(request, 'home.html', context=context)


def add_info_form(request):
    user = request.user.username
    if user == 'AnonymousUser':
        return render(request, 'home.html', context={'message': 'You are not allowed to access this page'})

    return render(request, 'add_info_form.html')


def add_info(request, user_id):
    if request.method == 'POST':
        try:
            info_name = request.POST.get('info_name')
            info_description = request.POST.get('info_description')
            info_image = request.FILES.get('info_image')
            info_image_data = info_image.read()
            info_date = date.today()
            info = Information(
                info_name=info_name,
                info_description=info_description,
                info_created_date=info_date,
                info_image=info_image_data,
                user=UserExtend.objects.get(user_id=user_id),
            )
            info.save()

            return redirect('home')
        except Exception as e:
            return render(request, 'add_info_form.html', context={'message': e})
    return render(request, 'add_info_form.html')


def info_acc_form(request, user_id):
    user_type = UserExtend.objects.get(user_id=user_id).user_type
    if user_type != 'super_user':
        return render(request, 'home.html', context={'message': 'You are not allowed to access this page'})
