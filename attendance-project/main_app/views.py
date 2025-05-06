from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, ClassRoom, AttendanceProcess, Report  # assuming these models are in your models.py


from .models import (
    CustomUser,ClassRoom,
    AttendanceProcess, Report, # Role,
    # StudentProfile, TeacherProfile, AttendanceOfficerProfile
)
from .serializers import (
    CustomUserSerializer, ClassRoomSerializer,
    AttendanceProcessSerializer, ReportSerializer
)


from .serializers import CustomUserSerializer as CurrentUserSerializer


# ---------- Users ----------
class CustomUserListCreateView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("❌ Signup Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomUserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


# ---------- Roles ----------
# class RoleListCreateView(ListCreateAPIView):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer

# class RoleDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer


# ---------- Current User ----------
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data)


# ---------- Classrooms ----------

class GetClassrooms(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            classrooms = ClassRoom.objects.all()
        except Exception as e:
            print("❌ Error fetching classrooms:", str(e))
            return Response({"error": "An error occurred while fetching classrooms."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = ClassRoomSerializer(classrooms, many=True)
        return Response(serializer.data)

class StudentsByClassroomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, classroom_id):
        students = CustomUser.objects.filter(role='student', classroom__id=classroom_id)
        print(students)
        serializer = CustomUserSerializer(students, many=True)
        return Response(serializer.data)

class StudentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = CustomUser.objects.filter(role='student')
        serializer = CustomUserSerializer(students, many=True)
        return Response(serializer.data)


# class StudentListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         students = CustomUser.objects.filter(role='Student')
#         serializer = CustomUserSerializer(students, many=True)
#         return Response(serializer.data)

# class StudentDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = CustomUser.objects.filter(role='Student')
#     serializer_class = CustomUserSerializer
#     permission_classes = [IsAuthenticated]

class ClassRoomListCreateView(ListCreateAPIView):
    print("ClassRoomListCreateView")
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer

class ClassRoomDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer


# ---------- Attendance ----------
class AttendanceProcessListCreateView(ListCreateAPIView):
    queryset = AttendanceProcess.objects.all()
    serializer_class = AttendanceProcessSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("❌ Attendance Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the attendance process
        self.perform_create(serializer)
        attendance_process = serializer.instance

        # Create a new attendance report
        try:
            report = Report.objects.create(
                attendance_process=attendance_process,
                created_by=request.user
            )
            print("✅ Attendance Report Created:", report.id)
        except Exception as e:
            print("❌ Error creating attendance report:", str(e))
            return Response({"error": "An error occurred while creating the attendance report."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class AttendanceProcessDetailView(RetrieveUpdateDestroyAPIView):
    queryset = AttendanceProcess.objects.all()
    serializer_class = AttendanceProcessSerializer
    permission_classes = [permissions.IsAdminUser]


class BulkAttendanceView(APIView):
    def post(self, request):
        print("request.data", request.data)
        data = request.data
        classroom_id = data.get('classroom_id')
        date = data.get('date')
        attendances = data.get('attendances', [])

        # Validate input
        if not classroom_id or not date or not attendances:
            return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        attendance_instances = []
        for entry in attendances:
            student_id = entry.get('student_id')
            status_value = entry.get('status')
            note = entry.get('note', '')

            try:
                student = CustomUser.objects.get(id=student_id)
                classroom = ClassRoom.objects.get(id=classroom_id)
            except CustomUser.DoesNotExist:
                continue  # Skip if student does not exist
            except ClassRoom.DoesNotExist:
                continue  # Skip if classroom does not exist

            # Create the AttendanceProcess instance
            attendance_instance = AttendanceProcess(
                student=student,
                classroom=classroom,
                date=date,
                status=status_value,
                note=note
            )
            attendance_instances.append(attendance_instance)

        # Bulk create attendance instances
        AttendanceProcess.objects.bulk_create(attendance_instances)

        # Create the Report object after creating AttendanceProcess instances
        attendance = AttendanceProcess.objects.filter(
            classroom_id=classroom_id, date=date
        ).first()  # Ensure we have a valid attendance instance

        if attendance:  # Only create a report if attendance exists
            report = Report.objects.create(
                title=f"Attendance Report for {date}",
                content=f"Attendance recorded for classroom {classroom.name} on {date}.",
                created_by=request.user,
                attendance=attendance  # Link the report to the attendance instance
            )

        return Response({'message': 'Attendance recorded successfully.'}, status=status.HTTP_201_CREATED)

# ---------- Reports ----------
class ReportListCreateView(ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class ReportDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAdminUser]
