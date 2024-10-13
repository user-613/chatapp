from datetime import timedelta

from django import template
from django.utils import timezone
from django.utils.translation import gettext, ngettext

register = template.Library()


@register.filter
@register.simple_tag
def elapsed_time(dt):
     if not dt:
          return None
     
     delta = timezone.now() - dt

     zero = timedelta()
     one_hour = timedelta(hours=1)
     one_day = timedelta(days=1)
     one_week = timedelta


     if delta < zero:
        raise ValueError("未来の時刻")
     
     if delta < one_hour:
          minutes = delta.seconds // 60
          return ngettext("%d minutes ago", "%d minutes ago", minutes) % minutes
     elif delta < one_day:
          hours = delta.seconds //3600
          return ngettext("%d hour ago", "%d hours ago", hours) % hours
     elif delta < one_week:
          return ngettext("%d day ago", "%d days ago", delta.days) % delta.days
     else:
          return gettext("more than 1 week")

     
def ngettext(singular, plural, number):
    if number == 1:
        msg = gettext(singular)
    else:
        msg = gettext(plural)
    return msg