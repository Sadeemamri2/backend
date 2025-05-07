from django.db import models
from django.contrib.auth.models import AbstractUser


# ---------- Role Model ----------
class Role(models.Model):
    name = models.CharField(max_length=50)  # مثل: طالب، معلم، مدير
    def __str__(self):
        return self.name

# ---------- Custom User Model ----------

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'admin'),
        ('teacher', 'teacher'),
        ('student', 'student'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    email = models.EmailField(blank=True, null=True)
    classroom = models.ForeignKey('ClassRoom', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')


# ---------- ClassRoom Model ----------
class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=10)
    teacher = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='teaching_classroom')


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
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'Student'})
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.username} - {self.date} - {self.status}"


# ---------- Report Model ----------
class Report(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    attendances = models.ManyToManyField(AttendanceProcess)


    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%Y-%m-%d')}"

#  ---------- lesson Model ----------
class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    day = models.CharField(max_length=20)  # يمكنك تحديد الخيارات لاحقًا إذا رغبت

    def __str__(self):
        return self.title

