import datetime
import json

from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from registration.models import UserExtend, User
from .models import Batch, Resident, BatchMessage


# Create your views here.


def database_page(request):
    if request.user.is_authenticated:
        database = Resident.objects.filter(batch__approved=True).values()
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
            context = {
                'message': 'there is no data available',
                'user_type': user_type
            }
            return render(request, 'database/database_home.html', context=context)
    else:
        return HttpResponseRedirect(reverse('home'))


def database_form(request):
    user_type = request.user.userextend.user_type
    if user_type != 'special_user':
        return HttpResponseRedirect(reverse('database_home'))

    return render(request, 'database/database_add_form.html')


def database_add_data(request):
    try:
        batch = Batch(input_person=request.user)
        batch.save()

        form_data = json.loads(request.body.decode('utf-8'))

        for form in form_data:
            # Validate required fields
            required_fields = ['name', 'gender', 'birthdate', 'rt', 'rw']
            if not all(field in form for field in required_fields):
                return render(
                    request,
                    'database/database_add_form.html',
                    context={'error': 'Missing required fields'},
                    status=400)

            data = Resident(
                name=form['name'],
                gender=form['gender'],
                birth_date=form['birthdate'],
                rt=form['rt'],
                rw=form['rw'],
                pregnant=False if form['pregnant'] == 'false' else True,
                work=form['work'],
                batch=batch
            )
            data.save()
        return HttpResponseRedirect(reverse('database_home'))

    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse('database_form'))


def database_approval_page(request):
    if request.user.userextend.user_type != 'super_user':
        return HttpResponseRedirect(reverse('database_home'))

    non_approved_batch = Batch.objects.filter(approved=False).values()
    for batch in non_approved_batch:
        batch['batch_data'] = Resident.objects.filter(batch_id=batch['id']).values()
        input_person = User.objects.get(id=batch['input_person_id'])
        batch['input_person'] = input_person.username
        batch['rt'] = input_person.userextend.rt
        batch['rw'] = input_person.userextend.rw

        for data in batch['batch_data']:
            today = datetime.date.today()
            birth_date = data['birth_date']
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            data['age'] = age

    context = {
        'batches': non_approved_batch
    }

    return render(request, 'database/database_approval.html', context=context)


def database_approve(request, batch_id):
    if request.user.userextend.user_type != 'super_user':
        return HttpResponseRedirect(reverse('database_home'))

    batch = Batch.objects.get(id=batch_id)
    batch.approved = True
    batch.save()

    return HttpResponseRedirect(reverse('database_approval_page'))


def database_revision(request, batch_id):
    if request.user.userextend.user_type != 'super_user':
        return HttpResponseRedirect(reverse('database_home'))

    batch = Batch.objects.get(id=batch_id)
    batch.revision = True
    batch.save()

    message = BatchMessage(
        batch=batch,
        message=request.POST['revision_message']
    )

    message.save()

    return HttpResponseRedirect(reverse('database_approval_page'))
