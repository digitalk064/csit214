from django import forms
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, time, timedelta
from django.utils import timezone as timmy #Avoid naming conflict
from pytz import timezone
from django.contrib.admin.widgets import AdminDateWidget

from datetime import datetime

from .models import Booking

class AdminRoomUseForm(forms.Form):
    r_id = forms.IntegerField(widget=forms.HiddenInput())
    start_date = forms.DateField(widget=AdminDateWidget(), label="From ")
    end_date = forms.DateField(widget=AdminDateWidget(), label="To ")

def admin_view_room_usage (request):
    timmy.activate(settings.TIME_ZONE)
    if request.user is None:
        return HttpResponse("invalid user", status=400)
    if not (request.user.is_authenticated and request.user.is_staff):
        return HttpResponse("unauthenticated access", status=400)
    if request.method != "POST":
        return HttpResponse("invalid request", status=400)

    form = AdminRoomUseForm(request.POST)
    if not form.is_valid():
        return HttpResponse("invalid form", status=400)

    r_id = form.cleaned_data.get('r_id')
    start_date = timezone(settings.TIME_ZONE).localize(datetime.combine(form.cleaned_data.get('start_date'), time(0,0)))
    end_date = timezone(settings.TIME_ZONE).localize(datetime.combine(form.cleaned_data.get('end_date'), time(0,0)))

    u_bookings = Booking.objects.filter(room_id = r_id).filter(start__gte=start_date).filter(end__lte=end_date).order_by('start') #Get bookings within time frame
    data = {}
    data["bookings"] = list(u_bookings.values('id','start','end'))
    for i, b in enumerate(data["bookings"]):
        #Localize times
        #print(f'Before localize: {b["start"]} and {b["end"]}')
        b["start"] = timmy.localtime(b["start"], timezone(settings.TIME_ZONE))
        b["end"] = timmy.localtime(b["end"], timezone(settings.TIME_ZONE))
        b["booker_name"] = u_bookings[i].booker_name
        #print(f'After localize: {b["start"]} and {b["end"]}')

    return JsonResponse(data, safe=False)
