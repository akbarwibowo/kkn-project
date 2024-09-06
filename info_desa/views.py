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

    message = "There is no information available" if not informations else ""
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
    user = request.user.username
    # TODO: try to use http redirect instead
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
        return redirect(reverse('home'))

    informations = Information.objects.filter(approved=False, revision=False, rejected=False).values()

    for info in informations:
        info['info_image'] = base64.b64encode(info['info_image']).decode('utf-8')
        info_maker = Information.objects.get(id=info['id']).user.user.username
        info['info_maker'] = info_maker

    if informations is None or len(informations) == 0:
        message = "There is no information need to accept"
        return render(request, 'acc_form_page.html', context={'message': message})

    context = {
        'informations': informations,
        'user_id': user_id
    }

    return render(request, 'acc_form_page.html', context=context)


def info_acc(request, info_id, user_id):
    info = Information.objects.get(id=info_id)
    info.approved = True
    info.save()

    return HttpResponseRedirect(reverse('acc_form', args=(user_id,)))


@require_POST
def info_reject(request, info_id, user_id):
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


@require_POST
def info_revise(request, info_id, user_id):
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


def info_feedback(request, user_id):
    informations = (Information.objects.filter(user=user_id, rejected=True).values() |
                    Information.objects.filter(user=user_id, revision=True).values()).order_by('-info_created_date')
    if informations:
        for info in informations:
            info_messages = InformationMessage.objects.get(information=info['id'])
            info['info_message'] = info_messages
            info['status'] = info_messages.type
    else:
        return render(request, 'feedback_info.html', context={'message': 'There is no information available'})
    context = {
        'informations': informations,
    }

    return render(request, 'feedback_info.html', context=context)


def info_revision_form(request, info_id):
    informations = Information.objects.get(id=info_id)
    context = {
        'informations': informations,
    }

    return render(request, 'info_revision_form.html', context=context)


@require_POST
def info_do_revision(request, info_id):
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
