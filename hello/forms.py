from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput

from datetime import datetime

class RoomSearchForm(forms.Form):
    date = forms.DateField(
        widget=DatePickerInput(
            format='%d/%m/%Y',
            attrs={'width':'50%',},
            options= {
                'minDate': datetime.today().strftime('%Y-%m-%d 00:00:00'),
            }
        ), 
        help_text = "Select a day in dd/mm/yyyy format", label = "Date", 
        initial=timezone.now(),
        input_formats=("%d/%m/%Y",),
    )
    start_time = forms.TimeField(
        help_text = "Select check in time",
        widget=TimePickerInput(
            options = {
                "stepping": 15, "keepOpen": True, "showClose": False, "showClear": False, "showTodayButton": False}
        ),
        initial = "09:00",
    )
    duration = forms.IntegerField(
        label = "Duration",
        help_text = "hour(s)",
        initial = 1,
        min_value=1,
        max_value=3,
    )
    room_name = forms.CharField(
        help_text = "Search by name",
        max_length=60,
        required = False,
    )

class RoomBookForm(forms.Form):
    b_room_id = forms.IntegerField()
    b_date = forms.DateField(input_formats=("%d/%m/%Y",),)
    b_start_time = forms.TimeField()
    b_duration = forms.IntegerField()
    b_price = forms.DecimalField()

class CancelBookForm(forms.Form):
    c_room_id = forms.IntegerField()