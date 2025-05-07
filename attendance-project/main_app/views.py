from rest_framework import permissions, status, viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from .models import CustomUser, ClassRoom, AttendanceProcess, Report, Lesson
from .serializers import LessonSerializer


from .models import (
    CustomUser,ClassRoom,
    AttendanceProcess, Report, # Role,
  
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
                attendance=attendance_process,
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
                continue
            except ClassRoom.DoesNotExist:
                continue

            attendance_instance = AttendanceProcess(
                student=student,
                classroom=classroom,
                date=date,
                status=status_value,
                note=note
            )
            attendance_instances.append(attendance_instance)

        AttendanceProcess.objects.bulk_create(attendance_instances)

        created_attendances = AttendanceProcess.objects.filter(
            classroom_id=classroom_id, date=date
        )

        if created_attendances.exists():
            report = Report.objects.create(
                title=f"Attendance Report for {date}",
                content=f"Attendance recorded for classroom {classroom.name} on {date}.",
                created_by=request.user,
            )
            report.attendances.set(created_attendances)

            return Response({"message": "Attendance has been recorded and the report was successfully created."}, status=status.HTTP_201_CREATED)

        # ✅ If no attendance was created
        return Response({"message": "Attendance has been recorded, but no report was created."}, status=status.HTTP_201_CREATED)

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

    @api_view(['PUT'])
    def update_report(request, report_id):
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return Response({'error': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PUT':
            report.title = request.data.get('title', report.title)
            report.content = request.data.get('content', report.content)
            report.save()
            return Response({'message': 'Report updated successfully'}, status=status.HTTP_200_OK)

    @api_view(['DELETE'])
    def delete_report(request, report_id):
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return Response({'error': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'DELETE':
            report.delete()
            return Response({'message': 'Report deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated] 
    def get_queryset(self):
       
        return Report.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ReportDetail(APIView):
    permission_classes = [IsAuthenticated]  # أو [IsAdminUser] حسب الحاجة

    def delete(self, request, pk):
        try:
            report = Report.objects.get(pk=pk)
            report.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Report.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer