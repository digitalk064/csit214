from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from django.utils import timezone as timmy #Avoid naming conflict
from datetime import datetime,timedelta,time
import pytz

from pytz import timezone

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class Room(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending Approval')
        REJECTED = 'REJECTED', _('Rejected')
        APPROVED = 'APPROVED', _('Approved for use')

    name = models.CharField(max_length = 60)
    capacity = models.IntegerField(help_text="Maximum number of persons")
    location = models.CharField(max_length = 100,unique=True) 
    price = models.DecimalField(max_digits = 6, decimal_places=2, help_text = "$ / hour")
    img = models.ImageField(null=True, blank=True, upload_to ='rooms/')
    description = models.TextField()
    last_modified = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, on_delete= models.CASCADE)
    status = models.CharField(max_length = 10, choices= Status.choices, default = Status.PENDING)
    available_from = models.DateField(default=datetime.today, help_text = "The date this room will be available for students")
    available_to = models.DateField(null=True, blank=True, help_text = "(Optional). Must be later than available from date. Null means room never expires")

    def __str__(self):
        return "Room: " + self.name

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    start = models.DateTimeField(auto_now = False, auto_now_add = False)
    end = models.DateTimeField(auto_now = False, auto_now_add = False)
    booker = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Booking#" + str(self.id)

    @property
    def booker_name(self):
        return User.objects.get(pk=self.booker_id).username

    @property
    def book_status(self):
        if (timmy.now() < self.start): #timezone.now() already returns utc time
            return 0 #Not started
        elif (self.start <= timmy.now() <= self.end):
            return 1 #In progress
        elif (timmy.now() > self.end):
            return 2 #Finished

    def occupied(self,time, dur_h): #Check if a specific time is occupied by this booking
        #Convert naive time to utc time
        #print(f'TIME BEFORE: {time.tzinfo} {time}')
        tz = self.start.tzinfo
        time = time.astimezone(tz) #Localize the desired time to the server time
        #print(f'TIME AFTER: {time.tzinfo} {time}')
        #print (f'COMPARE {time} TO {self.start} BOOK STATUS IS {self.book_status}')        
        if(self.book_status == 2): #If this booking has finished, it's not occupying
            return False
        #If this booking has not started
        if (time < self.start): #If we start before this booking
            check = time + timedelta(hours=dur_h)
            #print (f'CHECK CAN FINISH IN TIME: COMPARE {check} TO {self.start}')
            return check >= self.start #Do we finish before the booking starts? True means check can't finish before start
        else: #If we start after the booking
            return time < self.end #Do we start after it has finished? True means we start before the booking ends
            

class Promo(models.Model):
    code = models.CharField(max_length = 10)
    discount = models.IntegerField(help_text = "(0-100)% off")


