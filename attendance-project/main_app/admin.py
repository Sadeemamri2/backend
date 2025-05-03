
from django.contrib import admin
from .models import Role, CustomUser, ClassRoom, AttendanceProcess, Report

admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(ClassRoom)
admin.site.register(AttendanceProcess)
admin.site.register(Report)
