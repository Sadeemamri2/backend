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
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

   
    def __str__(self):
        return self.name or self.email or self.username


# ---------- ClassRoom Model ----------
class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=10, null=False)
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