from django.contrib import admin

from .models import staffTrack, staffVacation

# Register your models here.

class StaffTrackAdmin(admin.ModelAdmin):
    list_display = ['id','user_id', 'username', 'login_time', 'logout_time']

admin.site.register(staffTrack, StaffTrackAdmin)

class StaffVacationAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'vacationTime']

admin.site.register(staffVacation, StaffVacationAdmin)


