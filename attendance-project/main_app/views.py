# main_app/views.py
from rest_framework import permissions
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from .models import CustomUser, Role, ClassRoom, AttendanceProcess, Report
from .serializers import (
    CustomUserSerializer,
    RoleSerializer,
    ClassRoomSerializer,
    AttendanceProcessSerializer, ReportSerializer
)

class CustomUserListCreateView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class RoleListCreateView(ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class ClassRoomListCreateView(ListCreateAPIView):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer

class ClassRoomDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer

class AttendanceProcessListCreateView(ListCreateAPIView):
    """
    GET: قائمة كل السجلات
    POST: إضافة سجل جديد
    """
    queryset = AttendanceProcess.objects.all()
    serializer_class = AttendanceProcessSerializer

    # مثال: تقييد إضافة الغياب للمسؤول فقط:
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class AttendanceProcessDetailView(RetrieveUpdateDestroyAPIView):
    queryset = AttendanceProcess.objects.all()
    serializer_class = AttendanceProcessSerializer

    # مثال: تقييد التعديل/الحذف للمسؤول فقط:
    permission_classes = [permissions.IsAdminUser]


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
