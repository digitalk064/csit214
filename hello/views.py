from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages

from .models import Greeting,Room,Booking,Promo
from .forms import RoomSearchForm,RoomBookForm,CancelBookForm
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.db.models import Q

from datetime import datetime, time, timedelta
from django.utils import timezone as timmy #Avoid naming conflict
from pytz import timezone
from django.conf import settings

import requests

# Create your views here.
@login_required
def index(request):
    #If user is staff, take user to admin page right away
    if request.user.is_staff:
        return redirect('admin:index')
    context = {"home_page" : "active"} #change navbar active element
    
    form = RoomSearchForm()
    context['form'] = form
    context['bookform'] = RoomBookForm()
    context['cancelform'] = CancelBookForm()

    return render(request, "index.html", context)

def search_room(request):
    if request.user is None:
        return HttpResponse("invalid user", status=400)
    if not request.user.is_authenticated:
        return HttpResponse("not logged in", status=400)
        
    if request.method == "POST":
        form = RoomSearchForm(request.POST)
        if form.is_valid():
            data = {}
            rooms = Room.objects.filter(status='APPROVED').filter(name__icontains=form.cleaned_data["room_name"])

            #Convert from string to date and time then combine to compare
            date = form.cleaned_data.get('date') #REMEMBER TO USE CLEANED DATA HOLY SH*T
            time = form.cleaned_data.get('start_time')
            datetime_to_check = datetime.combine(date, time) #Check against the desired date
            #Make sure to localize this to our settings' timezone
            datetime_to_check = timezone(settings.TIME_ZONE).localize(datetime_to_check)
            rooms = rooms.filter(available_from__lte=datetime_to_check) #Filter available from date
            rooms = rooms.filter(Q(available_to__gte=datetime_to_check)| Q(available_to__isnull=True)) #Filter available to date
            data["rooms"] = list(rooms.values('id', 'name','capacity','location','img','status', 'price'))
            for i, r in enumerate(data["rooms"]):
                r_bookings = Booking.objects.filter(room_id=rooms[i]) #Find all bookings related to this room
                #Optimal: Also filter by start date that is >= book time - 3 hours 
                r["available"] = True #Innocent until proven guilty
                for rb in r_bookings: #Check if booking to see if it overlaps with desired time
                    if rb.occupied(datetime_to_check, form.cleaned_data.get('duration')): #If there's a occupied booking
                        r["available"] = False #Mark the room as not available
                        break    
            return JsonResponse(data, safe=False)
        else:
            return HttpResponse("Your criteria were invalid!", status=401)
    else:
        return HttpResponse("invalid request", status=400)

def get_upcoming(request):
    timmy.activate(settings.TIME_ZONE)
    if request.user is None:
        return HttpResponse("invalid user", status=400)
    if not request.user.is_authenticated:
        return HttpResponse("not logged in", status=400)
    try:
        u_bookings = Booking.objects.filter(booker_id = request.user).filter(start__gte=timmy.now()).select_related('room').order_by('start') #Get bookings with start date >= now
    except: #No booking yet
        u_bookings = None
    data = {}
    data["upcoming_bookings"] = list(u_bookings.values('id','start','end'))
    for i, b in enumerate(data["upcoming_bookings"]):
        b["r_name"] = u_bookings[i].room.name
        b["r_location"] = u_bookings[i].room.location
        #Localize times
        #print(f'Before localize: {b["start"]} and {b["end"]}')
        b["start"] = timmy.localtime(b["start"], timezone(settings.TIME_ZONE))
        b["end"] = timmy.localtime(b["end"], timezone(settings.TIME_ZONE))
        #print(f'After localize: {b["start"]} and {b["end"]}')

    data['promos'] = list(Promo.objects.all().values())

    return JsonResponse(data, safe=False)

def book_room(request):
    quick_auth(request)

    form = RoomBookForm(request.POST)
    if form.is_valid():
        start_time = datetime.combine(form.cleaned_data.get('b_date'), form.cleaned_data.get('b_start_time'))
        end_time = start_time + timedelta(hours=form.cleaned_data.get('b_duration'))

        start_time = timezone(settings.TIME_ZONE).localize(start_time)
        end_time = timezone(settings.TIME_ZONE).localize(end_time)
        
        if start_time <= timezone(settings.TIME_ZONE).localize(datetime.now()):
            msg = JsonResponse({"msg":"Your desired time is invalid (it's in the past)!"})
            msg.status_code = 400
            return msg

        #print(f'start {start_time} end {end_time}')
        book, created = Booking.objects.update_or_create (
            room_id = form.cleaned_data.get('b_room_id'),
            start = start_time,
            end = end_time,
            booker = request.user
        )
        #print(f'Result: {book.start} and {book.end}')
        return HttpResponse("done: " + str(created) + ' ' + str(datetime.now()))
    else:
        return HttpResponse("invalid request", status=400)

def cancel_book(request):
    quick_auth(request)
    form = CancelBookForm(request.POST)
    if form.is_valid():
        #print(f'REQUEST TO DELETE BOOKING#{form.cleaned_data.get("c_room_id")}')
        num, detail = Booking.objects.filter(id = form.cleaned_data.get("c_room_id")).delete()
        if(num == 0):
            msg = JsonResponse({"msg":"Cannot find record to delete"})
            msg.status_code = 400
            return msg
        else:
            return HttpResponse("Your booking has been canceled")
    else:
        return HttpResponse("invalid request", status=400)

def modify_first(request): #Temporarily remove the modify target
    quick_auth(request)
    form = CancelBookForm(request.POST)
    if form.is_valid():
        cache.set('book_temp', Booking.objects.get(id = form.cleaned_data.get("c_room_id"))) #Cache the target
        num, detail = Booking.objects.filter(id = form.cleaned_data.get("c_room_id")).delete()
        #print(f'TEMP IS {book_temp.id} {book_temp.room}')
        if(num == 0):
            msg = JsonResponse({"msg":"Cannot find record to delete"})
            msg.status_code = 400
            return msg
        else:
            return HttpResponse("temporarily deleted")
    else:
        return HttpResponse("invalid request", status=400)

@csrf_exempt #HUGE SECURITY FLAW BUT I'VE SPENT ENOUGH TIME ON THIS ALREADY
def modify_cancel(request):
    if request.user is None:
        return HttpResponse("invalid user", status=400)
    if not request.user.is_authenticated:
        return HttpResponse("not logged in", status=400)
    #print(f'ATTEMPT TO INSERT {book_temp.id} {book_temp.room} BACK')
    cache.get('book_temp').save() #Restore the target
    return HttpResponse("restored temp booking")

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

def register(request):
    return HttpResponse("not supported")

def quick_auth(request):
    if request.user is None:
        return HttpResponse("invalid user", status=400)
    if not request.user.is_authenticated:
        return HttpResponse("not logged in", status=400)
    if request.method != "POST":
        return HttpResponse("invalid request", status=400)