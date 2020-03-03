from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration, format_duration, is_visit_long
import locale

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    for visit in visits:
        duration = get_duration(visit)
        non_closed_visits_info = {
                "who_entered": visit.passcard.owner_name,
                "entered_at": visit.entered_at.strftime('%d %B %Y г. %H:%m'),
                "duration": format_duration(duration),
                "is_strange": is_visit_long(duration)
            }
        non_closed_visits.append(non_closed_visits_info)
    context = {
        "non_closed_visits": non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
