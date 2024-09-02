from django.shortcuts import render
from .models import UserExtend, User

# Create your views here.


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        rt = request.POST.get('rt')
        rw = request.POST.get('rw')
        user_type = request.POST.get('user_type')
        user = User.objects.create_user(username=username, password=password, email=email)
        user_extend = UserExtend(user_id=user, phone=phone, rt=rt, rw=rw, user_type=user_type)
        user_extend.save()
        return render(request, 'registration/register.html', {'message': 'User created successfully'})
    return render(request, 'registration/register.html')
