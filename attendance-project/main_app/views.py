from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import (
    CustomUser, Role, ClassRoom,
    AttendanceProcess, Report,
    StudentProfile, TeacherProfile, AttendanceOfficerProfile
)
from .serializers import (
    CustomUserSerializer, ClassRoomSerializer,
    AttendanceProcessSerializer, ReportSerializer
)

# لو ما عندك CurrentUserSerializer، استخدم CustomUserSerializer بداله
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
class ClassRoomListCreateView(ListCreateAPIView):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer

class ClassRoomDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer


# ---------- Attendance ----------
class AttendanceProcessListCreateView(ListCreateAPIView):
    queryset = AttendanceProcess.objects.all()
    serializer_class = AttendanceProcessSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class AttendanceProcessDetailView(RetrieveUpdateDestroyAPIView):
    queryset = AttendanceProcess.objects.all()
    serializer_class = AttendanceProcessSerializer
    permission_classes = [permissions.IsAdminUser]


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
