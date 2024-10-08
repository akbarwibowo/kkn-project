from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from registration.models import UserExtend
from .models import Event, EventMessage
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.


def event_page(request, user_id):
    if request.user.is_authenticated:
        try:
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('home'))

            events = Event.objects.filter(approved=True).values()
            for event in events:
                event_maker = Event.objects.get(id=event['id']).user.user.username
                event['event_maker'] = event_maker
            message = "Belum ada kegiatan!" if not events else ""
            context = {
                'events': events,
                'message': message,
            }

            user_type = UserExtend.objects.get(user=user_id).user_type
            context['user_type'] = user_type

            return render(request, 'event_desa/event.html', context=context)
        except Exception as e:
            pass
    return HttpResponseRedirect(reverse('home'))


def add_event_form(request):
    if request.user.is_authenticated:
        return render(request, 'event_desa/add_event_form.html')
    return HttpResponseRedirect(reverse('home'))


@require_POST
def add_event(request, user_id):
    if request.user.is_authenticated:
        try:
            if request.method == 'POST':
                event_name = request.POST.get('event_name')
                event_description = request.POST.get('event_description')
                event_date = request.POST.get('event_date')
                event_time = request.POST.get('event_time')
                event_location = request.POST.get('event_location')
                event_target = request.POST.get('event_target')

                event = Event(
                    event_name=event_name,
                    event_description=event_description,
                    event_date=event_date,
                    event_time=event_time,
                    event_location=event_location,
                    event_target=event_target,
                    user=UserExtend.objects.get(user_id=user_id),
                )
                event.save()

                return HttpResponseRedirect(reverse('event_feedback', args=(user_id,)))
        except Exception as e:
            return render(request, 'event_desa/add_event_form.html', context={'message': e})
    return HttpResponseRedirect(reverse('home'))


def event_acc_form(request, user_id):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            user_type = UserExtend.objects.get(user_id=user_id).user_type
            if user_type == 'user':
                return render(request, 'event_desa/event.html',
                              context={'message': 'You are not allowed to access this page'})
            events = Event.objects.filter(approved=False, revision=False, rejected=False).values()
            if events:
                for event in events:
                    event_maker = Event.objects.get(id=event['id']).user.user.username
                    event['event_maker'] = event_maker
            message = "Belum ada kegiatan untuk diproses!" if not events else ""
            context = {
                'events': events,
                'message': message,
            }

            return render(request, 'event_desa/event_acc_form.html', context=context)
        return render(request, 'home.html', context={'message': 'You are not allowed to access this page'})
    return HttpResponseRedirect(reverse('home'))


@require_POST
def event_reject(request, event_id, user_id):
    if request.user.is_authenticated:
        event = Event.objects.get(id=event_id)
        event.rejected = True
        event.save()

        reject_message = EventMessage(
            type='rejected',
            message=request.POST.get('reject_message'),
            event=event
        )

        reject_message.save()

        return HttpResponseRedirect(reverse('event_acc_form', args=(user_id,)))
    return HttpResponseRedirect(reverse('home'))


@require_POST
def event_revision(request, event_id, user_id):
    if request.user.is_authenticated:
        event = Event.objects.get(id=event_id)
        event.revision = True
        event.save()

        revision_message = EventMessage(
            type='revision',
            message=request.POST.get('revision_message'),
            event=event
        )

        revision_message.save()

        return HttpResponseRedirect(reverse('event_acc_form', args=(user_id,)))
    return HttpResponseRedirect(reverse('home'))


def event_acc(request, event_id, user_id):
    if request.user.is_authenticated:
        event = Event.objects.get(id=event_id)
        event.approved = True
        event.save()

        return HttpResponseRedirect(reverse('event_acc_form', args=(user_id,)))
    return HttpResponseRedirect(reverse('home'))


def event_feedback(request, user_id):
    if request.user.is_authenticated:
        events = Event.objects.filter(user=user_id).values().order_by('-event_date')

        if events:
            for event in events:
                if event['rejected'] or event['revision']:
                    event_message = EventMessage.objects.get(event=event['id'])
                    event['event_message'] = event_message.message
                    event['status'] = event_message.type
                elif not event['approved']:
                    event['event_message'] = '-'
                    event['status'] = 'Menunggu disetujui'
                else:
                    event['event_message'] = 'Sudah dipublikasikan'
                    event['status'] = 'Disetujui'

            return render(request, 'event_desa/feedback_event.html', context={'events': events})  # Return after the loop
        else:
            return render(request, 'event_desa/feedback_event.html', context={'message': 'Belum ada kegiatan ditambahkan!'})
    return HttpResponseRedirect(reverse('home'))


def event_revision_form(request, event_id):
    if request.user.is_authenticated:
        event = Event.objects.get(id=event_id)
        event_message = EventMessage.objects.get(event=event)
        context = {
            'event': event,
            'event_message': event_message.message,
        }

        return render(request, 'event_desa/event_revision_form.html', context=context)
    return HttpResponseRedirect(reverse('home'))


@require_POST
def event_do_revision(request, event_id):
    if request.user.is_authenticated:
        event = Event.objects.get(id=event_id)
        event.event_name = request.POST.get('event_name')
        event.event_description = request.POST.get('event_description')
        event.event_date = request.POST.get('event_date')
        event.event_time = request.POST.get('event_time')
        event.event_location = request.POST.get('event_location')
        event.event_target = request.POST.get('event_target')
        event.revision = False

        event.save()

        event_message = EventMessage.objects.get(event=event_id)
        event_message.delete()

        return HttpResponseRedirect(reverse('event_feedback', args=(event.user.user_id,)))
    return HttpResponseRedirect(reverse('home'))


def event_delete(request, event_id):
    if request.user.is_authenticated:
        try:
            event_message = EventMessage.objects.get(event=event_id)
            event_message.delete()
        except Exception as e:
            pass

        try:
            event = Event.objects.get(id=event_id)
            event.delete()

        except Exception as e:
            pass

        return HttpResponseRedirect(reverse('event_feedback', args=(request.user.id,)))
    return HttpResponseRedirect(reverse('home'))
