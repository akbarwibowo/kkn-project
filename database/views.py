from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .models import Batch, Resident
from registration.models import UserExtend
import datetime

# Create your views here.


def database_page(request):
    if request.user.is_authenticated:
        database = Resident.objects.all().values()
        user_id = request.user.id
        user_type = UserExtend.objects.get(user=user_id).user_type
        for data in database:
            today = datetime.date.today()
            birth_date = data['birth_date']
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            data['age'] = age
        if database:
            context = {
                'database': database,
                'user_type': user_type
            }
            return render(request, 'database/database_home.html', context=context)
        else:
            return render(request, 'database/database_home.html', {'message': "There is no data available"})
    else:
        return HttpResponseRedirect(reverse('home'))
