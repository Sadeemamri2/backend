# main_app/urls.py
from django.urls import path
from .views import (
    CustomUserListCreateView, CustomUserDetailView,
    RoleListCreateView, RoleDetailView,
    ClassRoomListCreateView, ClassRoomDetailView,
    AttendanceProcessListCreateView, AttendanceProcessDetailView,
)

urlpatterns = [
    path('users/',       CustomUserListCreateView.as_view(),        name='user-list'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(),         name='user-detail'),

    path('roles/',       RoleListCreateView.as_view(),              name='role-list'),
    path('roles/<int:pk>/', RoleDetailView.as_view(),               name='role-detail'),

    path('classrooms/',  ClassRoomListCreateView.as_view(),         name='classroom-list'),
    path('classrooms/<int:pk>/', ClassRoomDetailView.as_view(),     name='classroom-detail'),

    path('attendance/',            AttendanceProcessListCreateView.as_view(),    name='attendance-list'),
    path('attendance/<int:pk>/',   AttendanceProcessDetailView.as_view(),        name='attendance-detail'),
]
