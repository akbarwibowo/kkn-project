from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from registration.models import UserExtend
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Information, InformationMessage
from datetime import date
import base64

# Create your views here.


def home(request):
    informations = Information.objects.filter(approved=True).order_by('-info_created_date').values()
    for info in informations:
        info['info_image'] = base64.b64encode(info['info_image']).decode('utf-8')
        info['maker'] = Information.objects.get(id=info['id']).user.user.username

    message = "Belum ada informasi." if not informations else ""
    context = {
        'informations': informations,
        'message': message,
    }

    if request.user.is_authenticated:
        user_id = request.user.id
        user_type = UserExtend.objects.get(user_id=user_id).user_type
        context['user_type'] = user_type

    return render(request, 'home.html', context=context)


def add_info_form(request):
    if request.user.is_authenticated:
        user = request.user.username
        if user == 'AnonymousUser':
            return render(request, 'home.html', context={'message': 'You are not allowed to access this page'})

        return render(request, 'info_desa/add_info_form.html')
    return HttpResponseRedirect(reverse('home'))


def add_info(request, user_id):
    if request.user.is_authenticated:
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

                return redirect(reverse('feedback_info', args=(user_id,)))
            except Exception as e:
                return render(request, 'info_desa/add_info_form.html', context={'message': e})
        return render(request, 'info_desa/add_info_form.html')
    return HttpResponseRedirect(reverse('home'))


def info_acc_form(request, user_id):
    if request.user.is_authenticated:
        user_type = UserExtend.objects.get(user_id=user_id).user_type
        if user_type != 'super_user':
            return redirect(reverse('home'))

        informations = Information.objects.filter(approved=False, revision=False, rejected=False).values()

        if informations:
            for info in informations:
                info['info_image'] = base64.b64encode(info['info_image']).decode('utf-8')
                info_maker = Information.objects.get(id=info['id']).user.user.username
                info['info_maker'] = info_maker

        if informations is None or len(informations) == 0:
            message = "Tidak ada informasi untuk di proses"
            return render(request, 'info_desa/acc_form_page.html', context={'message': message})

        context = {
            'informations': informations,
            'user_id': user_id
        }

        return render(request, 'info_desa/acc_form_page.html', context=context)
    return HttpResponseRedirect(reverse('home'))


def info_acc(request, info_id, user_id):
    if request.user.is_authenticated:
        info = Information.objects.get(id=info_id)
        info.approved = True
        info.save()

        return HttpResponseRedirect(reverse('acc_form', args=(user_id,)))
    return HttpResponseRedirect(reverse('home'))


@require_POST
def info_reject(request, info_id, user_id):
    if request.user.is_authenticated:
        info = Information.objects.get(id=info_id)
        info.info_image = None
        info.rejected = True
        info.save()

        reject_message = InformationMessage(
            type='rejected',
            message=request.POST.get('reject_message'),
            information=info
        )
        reject_message.save()

        return HttpResponseRedirect(reverse('acc_form', args=(user_id,)))
    return HttpResponseRedirect(reverse('home'))


@require_POST
def info_revise(request, info_id, user_id):
    if request.user.is_authenticated:
        info = Information.objects.get(id=info_id)
        info.revision = True
        info.info_image = None
        info.save()

        revision_message = InformationMessage(
            type='revision',
            message=request.POST.get('revision_message'),
            information=info
        )
        revision_message.save()

        return HttpResponseRedirect(reverse('acc_form', args=(user_id,)))
    return HttpResponseRedirect(reverse('home'))


def info_feedback(request, user_id):
    if request.user.is_authenticated:
        informations = Information.objects.filter(user=user_id).values().order_by('-info_created_date')
        if informations:
            for info in informations:
                if info['rejected'] or info['revision']:
                    info_messages = InformationMessage.objects.get(information=info['id'])
                    info['info_message'] = info_messages.message
                    info['status'] = info_messages.type
                elif not info['approved']:
                    info['info_message'] = '-'
                    info['status'] = 'Menunggu disetujui'
                else:
                    info['info_message'] = 'Sudah dipulikasikan'
                    info['status'] = 'Disetujui'

        else:
            return render(request, 'info_desa/feedback_info.html', context={'message': 'Belum ada informasi'})
        context = {
            'informations': informations,
        }

        return render(request, 'info_desa/feedback_info.html', context=context)
    return HttpResponseRedirect(reverse('home'))


def info_revision_form(request, info_id):
    if request.user.is_authenticated:
        informations = Information.objects.get(id=info_id)
        info_messages = InformationMessage.objects.get(information=informations)
        context = {
            'informations': informations,
            'info_message': info_messages.message,
        }

        return render(request, 'info_desa/info_revision_form.html', context=context)
    return HttpResponseRedirect(reverse('home'))


@require_POST
def info_do_revision(request, info_id):
    if request.user.is_authenticated:
        info = Information.objects.get(id=info_id)
        info.info_name = request.POST.get('info_name')
        info.info_description = request.POST.get('info_description')
        info_image_data = request.FILES.get('info_image')
        info.info_image = info_image_data.read()
        info.info_date = date.today()
        info.revision = False

        info.save()

        info_message = InformationMessage.objects.get(information=info_id)
        info_message.delete()

        return HttpResponseRedirect(reverse('home'))
    return HttpResponseRedirect(reverse('home'))


def info_delete(request, info_id):
    if request.user.is_authenticated:
        try:
            info_message = InformationMessage.objects.get(information=info_id)
            info_message.delete()
        except Exception as e:
            pass
        info = Information.objects.get(id=info_id)
        if info:
            info.delete()

        return HttpResponseRedirect(reverse('feedback_info', args=(request.user.id,)))
    return HttpResponseRedirect(reverse('home'))


def info_detail(request, info_id):
    try:
        info = Information.objects.filter(id=info_id).values()[0]
        info['info_image'] = base64.b64encode(info['info_image']).decode('utf-8')
        info['maker'] = Information.objects.get(id=info['id']).user.user.username

        return render(request, 'info_desa/info_detail.html', context={'info': info})
    except Exception as e:
        HttpResponseRedirect(reverse('home'))
