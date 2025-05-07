from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Role, CustomUser, ClassRoom, AttendanceProcess, Report, Lesson, Toy, Capybara, Photo, Feeding

User = get_user_model()

class ModelsTestCase(TestCase):
    def setUp(self):
        # Create Role
        self.role_teacher = Role.objects.create(name='teacher')
        self.role_student = Role.objects.create(name='student')

        # Create Teacher and Student
        self.teacher = User.objects.create_user(username='teacher1', password='testpass', role='teacher')
        self.student = User.objects.create_user(username='student1', password='testpass', role='student')

        # Create ClassRoom
        self.classroom = ClassRoom.objects.create(name='1A', year='2025', teacher=self.teacher)

        # Assign student to classroom
        self.student.classroom = self.classroom
        self.student.save()

        # Create Toy
        self.toy = Toy.objects.create(name="Ball", color="Red")

        # Create Capybara
        self.capybara = Capybara.objects.create(
            name="Capy",
            breed="Giant",
            description="Friendly",
            age=3,
            user=self.teacher
        )
        self.capybara.toys.add(self.toy)

        # Create Photo
        self.photo = Photo.objects.create(
            url="http://image.com/capy.jpg",
            title="Capy Photo",
            capybara=self.capybara
        )

        # Create Feeding
        self.feeding = Feeding.objects.create(
            date=timezone.now().date(),
            meal='B',
            capybara=self.capybara
        )

        # Create Attendance
        self.attendance = AttendanceProcess.objects.create(
            date=timezone.now().date(),
            status="Present",
            note="On time",
            student=self.student,
            classroom=self.classroom
        )

        # Create Report
        self.report = Report.objects.create(
            title="Weekly Attendance",
            created_by=self.teacher
        )
        self.report.attendances.add(self.attendance)

        # Create Lesson
        self.lesson = Lesson.objects.create(
            title="Math Lesson",
            description="Algebra Basics",
            day="Sunday"
        )

    def test_capybara_creation(self):
        self.assertEqual(self.capybara.name, "Capy")
        self.assertEqual(self.capybara.toys.first().name, "Ball")

    def test_photo_str(self):
        expected = f"Photo for capybara_id: {self.capybara.id} @{self.photo.url}"
        self.assertEqual(str(self.photo), expected)

    def test_attendance_str(self):
        expected = f"{self.student.username} - {self.attendance.date} - {self.attendance.status}"
        self.assertEqual(str(self.attendance), expected)

    def test_report_creation(self):
        self.assertEqual(self.report.attendances.count(), 1)
        self.assertEqual(str(self.report), f"{self.report.title} - {self.report.created_at.strftime('%Y-%m-%d')}")

    def test_custom_user_roles(self):
        self.assertEqual(self.teacher.role, "teacher")
        self.assertEqual(self.student.classroom.name, "1A")

    def test_lesson_str(self):
        self.assertEqual(str(self.lesson), "Math Lesson")
