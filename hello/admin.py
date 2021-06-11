from django.contrib import admin
from .models import Room, Booking, Promo

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.html import format_html

from .admin_form import AdminRoomUseForm

#Custom Admin Models
class RoomAdmin(admin.ModelAdmin):
    change_form_template = 'admin/room_change_approve.html'
    exclude = ('created_by','status')
    search_fields = ('name','location')
    list_filter = ('status',)

    def colored_status(self, obj): #Color text based on status
        if obj.status == 'PENDING':
            return format_html(
                '<span style = "color: orange;">Pending approval</span>',
            )
        elif obj.status == 'APPROVED':
            return format_html(
                '<span style = "color: green;">Approved for use</span>',
            )
        else:
            return format_html(
                '<span style = "color: red;">Rejected</span>',
            )
    colored_status.short_description = "Status" #Appear as Status instead of Colored Status
    colored_status.admin_order_field = 'status' #Enable ordering again
    
    list_display = ('name', 'location', 'created_by','colored_status', 'last_modified',)

    def save_model(self, request, obj, form, change):
        if not change: #Only add to the staff id if it's being created
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    #Override the view render to pass in information
    def change_view(self, request, object_id, form_url='', extra_context = None):
        extra_context = extra_context or {} #Init extra_content
        extra_context['status'] = Room.objects.get(pk=object_id).status
        #Let our html page know what group the user is in
        if request.user.groups.filter(name='Staff').exists():
            extra_context['group'] = 'Staff'
        else:
            extra_context['group'] = 'Admin'
            extra_context['use_form'] = AdminRoomUseForm()
        extra_context['r_id'] = object_id
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Admin').exists():
            return ('name','capacity','location','price','img','description','last_modified',
            'created_by', 'status', 'available_from','available_to',)
        else:
            return super(RoomAdmin, self).get_readonly_fields(request, obj)
    #Handle the admin's custom actions
    def response_change(self, request, obj):
        if "_approve" in request.POST: #Approve a room
            #Database code
            obj.status = 'APPROVED'
            obj.save()
            
            #Alert user and return
            self.message_user(request, f'{obj} successfully approved!', messages.SUCCESS)
            return HttpResponseRedirect(reverse("admin:hello_room_changelist")) #Hardcode cause lazy
        elif "_reject" in request.POST: #Reject a room
            #Database code
            obj.status = 'REJECTED'
            obj.save()

            #Alert user and return 
            self.message_user(request, f'{obj} successfully rejected!', messages.SUCCESS)
            return HttpResponseRedirect(reverse("admin:hello_room_changelist")) #Hardcode cause lazy
        return super().response_change(request, obj)

class BookingAdmin(admin.ModelAdmin):
    def colored_status(self, obj): #Color text based on status
        if obj.book_status == 0:
            return format_html(
                '<span style = "color: black;">Not started</span>',
            )
        elif obj.book_status == 1:
            return format_html(
                '<span style = "color: orange;">In progress</span>',
            )
        else:
            return format_html(
                '<span style = "color: green;">Finished</span>',
            )
    colored_status.short_description = "Status" #Appear as Status instead of Colored Status
    colored_status.admin_order_field = 'end' #Enable ordering again
    
    list_display = ('booker', 'room', 'start', 'end', 'colored_status')
    search_fields = ('booker__username', 'room__name')

class PromoAdmin(admin.ModelAdmin):
    list_display = ('code','discount')
    search_fields = ('code',)
    

# Register your models here.
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Promo, PromoAdmin)

#Customize admin page
admin.site.site_header = "UOW Room Booking administration"
admin.site.index_title = "UOW Room Booking System"
admin.site.site_title = "Staff"

