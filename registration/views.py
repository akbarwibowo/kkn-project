from django.shortcuts import render
from .models import UserExtend, User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.


def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            phone = request.POST.get('phone')
            rt = request.POST.get('rt')
            rw = request.POST.get('rw')
            user_type = request.POST.get('usertype')
            user_choices = UserExtend.user_type_choices
            if user_type == 'resident':
                user_type = user_choices['user']
            elif user_type == ('rt' or 'rw'):
                user_type = user_choices['special_user']

            user = User.objects.create_user(username=username, password=password, email=email)
            user_extend = UserExtend(user_id=user, phone=phone, rt=rt, rw=rw, user_type=user_type)
            user_extend.save()
            login(request, user)
            context = {
                'message': 'you are logged in!'
            }

            return HttpResponseRedirect(reverse('home'))
        except Exception as e:
            return render(request, 'registration.html', context={'message': e})
    return render(request, 'registration.html')


def log_in(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'login_page.html', context={'message': 'username or password is incorrect'})
        except Exception as e:
            return render(request, 'login_page.html', context={'message': e})
    return render(request, 'login_page.html')


@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
