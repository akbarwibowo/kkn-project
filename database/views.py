import datetime
import json

from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse

from registration.models import UserExtend, User
from .models import Batch, Resident, BatchMessage


# Create your views here.


def database_page(request):
    if request.user.is_authenticated:
        database = list(Resident.objects.filter(batch__approved=True).order_by('rw', 'rt').values())
        user_id = request.user.id
        user_type = UserExtend.objects.get(user=user_id).user_type

        if database:
            child_count = 0
            elderly_count = 0
            pregnant_count = 0
            rw_rt_child_count = {}
            rw_rt_elderly_count = {}
            rw_rt_pregnant_count = {}

            unique_rt = sorted(set(resident['rt'] for resident in database))
            unique_rw = sorted(set(resident['rw'] for resident in database))

            today = datetime.date.today()

            for data in database:
                data['pregnant'] = 'Hamil' if data['pregnant'] is True else 'Tidak Hamil'

                birth_date = data['birth_date']
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                data['age'] = age

                if age < 5:
                    rw_rt_child_count.setdefault(data['rw'], {}).setdefault(data['rt'], 0)
                    rw_rt_child_count[data['rw']][data['rt']] += 1
                    child_count += 1
                elif age > 60:
                    rw_rt_elderly_count.setdefault(data['rw'], {}).setdefault(data['rt'], 0)
                    rw_rt_elderly_count[data['rw']][data['rt']] += 1
                    elderly_count += 1

                if data['pregnant'] == 'Hamil':
                    rw_rt_pregnant_count.setdefault(data['rw'], {}).setdefault(data['rt'], 0)
                    rw_rt_pregnant_count[data['rw']][data['rt']] += 1
                    pregnant_count += 1

            context = {
                'database': database,
                'user_type': user_type,
                'child_count': child_count,
                'elderly_count': elderly_count,
                'pregnant_count': pregnant_count,
                'rw_rt_child_count': rw_rt_child_count,
                'rw_rt_elderly_count': rw_rt_elderly_count,
                'rw_rt_pregnant_count': rw_rt_pregnant_count,
                'unique_rt': unique_rt,
                'unique_rw': unique_rw
            }

            return render(request, 'database/database_home.html', context=context)
        else:
            context = {
                'message': 'Belum ada data!',
                'user_type': user_type
            }
            return render(request, 'database/database_home.html', context=context)
    else:
        return HttpResponseRedirect(reverse('home'))


def database_form(request):
    if request.user.is_authenticated:
        user_type = request.user.userextend.user_type
        if user_type != 'special_user':
            return HttpResponseRedirect(reverse('database_home'))

        user = UserExtend.objects.get(user=request.user.id)
        user_rt = user.rt
        user_rw = user.rw

        context = {
            'rt': user_rt,
            'rw': user_rw
        }

        return render(request, 'database/database_add_form.html', context=context)
    return HttpResponseRedirect(reverse('home'))


def database_add_data(request):
    if request.user.id:
        try:
            with transaction.atomic():
                batch = Batch(input_person=request.user)
                batch.save()

                form_data = json.loads(request.body.decode('utf-8'))

                for form in form_data:
                    # Validate required fields
                    required_fields = ['name', 'gender', 'birthdate', 'rt', 'rw']
                    if not all(field in form for field in required_fields):
                        return JsonResponse({
                            'success': False,
                            'error': 'Terdapat input yang kosong!'
                        }, status=400)

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

            return JsonResponse({
                'success': True,
                'message': 'Data berhasil dikirimkan',
                'redirect': reverse('database_feedback')
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    return HttpResponseRedirect(reverse('home'))


def database_approval_page(request):
    if request.user.is_authenticated:
        user_type = request.user.userextend.user_type
        if user_type in ['super_user', 'special_user_rw']:
            filter_kwargs = {'approved': False, 'revision': False}
            if user_type == 'special_user_rw':
                filter_kwargs['input_person__userextend__rw'] = request.user.userextend.rw

            non_approved_batch = Batch.objects.filter(**filter_kwargs).values()
            if not non_approved_batch:
                return render(request, 'database/database_approval.html', context={'message': 'Belum ada data untuk diproses!'})

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
        else:
            return HttpResponseRedirect(reverse('database_home'))
    return HttpResponseRedirect(reverse('home'))


def database_approve(request, batch_id):
    if request.user.id:
        if request.user.userextend.user_type not in ('super_user', 'special_user_rw'):
            return HttpResponseRedirect(reverse('database_home'))

        batch = Batch.objects.get(id=batch_id)
        batch.approved = True
        batch.save()

        return HttpResponseRedirect(reverse('database_approval_page'))
    return HttpResponseRedirect(reverse('home'))


def database_revision(request, batch_id):
    if request.user.is_authenticated:
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
    return HttpResponseRedirect(reverse('home'))


def database_feedback(request):
    if request.user.is_authenticated:
        if request.user.userextend.user_type != 'special_user':
            return HttpResponseRedirect(reverse('database_home'))

        database = Batch.objects.filter(input_person_id=request.user.id).values()
        if not database:
            return render(request, 'database/database_feedback.html', context={'message': 'Belum ada data yang dikirimkan!'})
        for batch in database:
            if batch['revision']:
                batch['revision_message'] = BatchMessage.objects.get(batch_id=batch['id']).message
            batch['batch_data'] = Resident.objects.filter(batch_id=batch['id']).values()
            if not batch['batch_data']:
                batch = Batch.objects.get(id=batch['id'])
                batch.delete()
                continue
            if batch['approved']:
                batch['status'] = 'Disetujui'
            elif batch['revision']:
                batch['status'] = 'Revisi'
            else:
                batch['status'] = 'Menunggu disetujui'

        context = {
            'batches': database
        }

        return render(request, 'database/database_feedback.html', context=context)
    return HttpResponseRedirect(reverse('home'))


def database_revision_form(request, batch_id):
    if request.user.is_authenticated:
        if request.user.userextend.user_type != 'special_user':
            return HttpResponseRedirect(reverse('database_home'))

        batch_list = []
        batch_data = Resident.objects.filter(batch_id=batch_id).values()
        for data in batch_data:
            date_obj = data['birth_date']
            formated_date = date_obj.strftime('%Y-%m-%d')
            batch_dict = {
                'name': data['name'],
                'gender': data['gender'],
                'birthdate': formated_date,
                'rt': data['rt'],
                'rw': data['rw'],
                'pregnant': data['pregnant'],
                'work': data['work']
            }
            batch_list.append(batch_dict)

        initial_data = {
            'batches': batch_list,
        }

        context = {
            'initial_data': json.dumps(initial_data),
            'batch_id': batch_id
        }

        return render(request, 'database/database_revision_form.html', context=context)
    return HttpResponseRedirect(reverse('home'))


def database_revision_do(request, batch_id):
    if request.user.is_authenticated:
        try:
            batch = Batch.objects.get(id=batch_id)
            if batch.revision is True:
                batch.revision = False
                batch.save()

                batch_message = BatchMessage.objects.get(batch=batch_id)
                batch_message.delete()

            form_data = json.loads(request.body.decode('utf-8'))
            batch_data = Resident.objects.filter(batch_id=batch_id).values()

            for data in range(len(batch_data)):
                edited_data = Resident.objects.get(id=batch_data[data]['id'])
                edited_data.name = form_data['batches'][data]['name']
                edited_data.gender = form_data['batches'][data]['gender']
                edited_data.birth_date = form_data['batches'][data]['birthdate']
                edited_data.rt = int(form_data['batches'][data]['rt'])
                edited_data.rw = int(form_data['batches'][data]['rw'])
                edited_data.work = form_data['batches'][data]['work']
                edited_data.pregnant = form_data['batches'][data]['pregnant']

                edited_data.save()
            return HttpResponseRedirect(reverse('database_feedback'))
        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse('database_feedback'))
    return HttpResponseRedirect(reverse('home'))


def delete_data(request, resident_id):
    if request.user.is_authenticated:
        resident = Resident.objects.get(id=resident_id)
        resident.delete()

        return HttpResponseRedirect(reverse('database_feedback'))
    else:
        return HttpResponseRedirect(reverse('home'))
