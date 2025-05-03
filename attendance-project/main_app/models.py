from django.db import models
from django.contrib.auth.models import AbstractUser


# ---------- Role Model ----------
class Role(models.Model):
    name = models.CharField(max_length=50)
    role_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.role_type})"
# ---------- Custom User Model ----------

class CustomUser(AbstractUser):
    name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)  # يمكن نخليه optional
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

# ---------- ClassRoom Model ----------
class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=10)  # تأكد من إضافة هذا السطر
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} ({self.year})"


# ---------- Attendance Process Model ----------
class AttendanceProcess(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Excused', 'Excused'),
    ]

    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    note = models.TextField(blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    def __str__(self):
        return f"Attendance on {self.date} - {self.status}"

# ---------- Report Model ----------
class Report(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, null=True)

    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    attendance = models.ForeignKey(AttendanceProcess, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%Y-%m-%d')}"