from django.db import models
from django.utils import timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved="leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )


def get_duration(visit):
    if visit.leaved_at is None:
        now = timezone.localtime()
        timedelta = now - visit.entered_at
        duration = timedelta.total_seconds()
        return duration
    else:
        timedelta = visit.leaved_at - visit.entered_at
        duration = timedelta.total_seconds()
        return duration


def format_duration(duration):
    duration_hours = int(duration // 3600)
    duration_minutes = int((duration % 3600) // 60)
    return f'{duration_hours} ч {duration_minutes} м'


def is_visit_long(duration, minutes=60):
    return duration > minutes*60
