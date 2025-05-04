from django.contrib import admin
from .models import (
    Role, CustomUser,
    ClassRoom, AttendanceProcess, Report,
    StudentProfile, TeacherProfile, AttendanceOfficerProfile
)

admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(ClassRoom)
admin.site.register(AttendanceProcess)
admin.site.register(Report)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(AttendanceOfficerProfile)
