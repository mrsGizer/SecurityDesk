from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration, format_duration, is_visit_long
import locale

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    for visit in visits:
        duration = get_duration(visit)
        visit_info = {
                "entered_at": visit.entered_at.strftime('%d %B %Y г. %H:%m'),
                "duration": format_duration(duration),
                "is_strange": is_visit_long(duration)
            }
        this_passcard_visits.append(visit_info)

    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
