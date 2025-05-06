from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    # Authentication
    path('token/',          TokenObtainPairView.as_view(),     name='token_obtain_pair'),
    path('token/refresh/',  TokenRefreshView.as_view(),        name='token_refresh'),
    path('users/me/',       CurrentUserView.as_view(),         name='current-user'),

    # Users
    path('users/',          CustomUserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(),     name='user-detail'),

    # Roles
    # path('roles/',          RoleListCreateView.as_view(),       name='role-list'),
    # path('roles/<int:pk>/', RoleDetailView.as_view(),           name='role-detail'),

    # Classrooms
    path('classrooms/',          GetClassrooms.as_view(),  name='classroom-list'),
    path('classrooms/<int:pk>/', ClassRoomDetailView.as_view(),      name='classroom-detail'),

    # Attendance
    path('attendance/', BulkAttendanceView.as_view(), name='bulk_attendance'),

    # path('attendance/',          AttendanceProcessListCreateView.as_view(),  name='attendance-list'),
    path('attendance/<int:pk>/', AttendanceProcessDetailView.as_view(),      name='attendance-detail'),

    # Reports
    path('reports/',          ReportListCreateView.as_view(),     name='report-list'),
    path('reports/<int:pk>/', ReportDetailView.as_view(),         name='report-detail'),

    # Student List
    # path('students/', StudentListView.as_view(), name='student-list'),
    # path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    # Get students by classroom
    path('classrooms/<int:classroom_id>/students/', StudentsByClassroomView.as_view(), name='students-by-classroom'),
    path('students/', StudentListView.as_view(), name='student-list'),
]
