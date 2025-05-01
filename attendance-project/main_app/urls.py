# urls.py
from django.urls import path
from .views import (
    CustomUserListCreateView, CustomUserDetailView,
    RoleListCreateView, RoleDetailView,
    ClassroomListCreateView, ClassroomDetailView
)

urlpatterns = [
    path('users/', CustomUserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),

    path('roles/', RoleListCreateView.as_view(), name='role-list'),
    path('roles/<int:pk>/', RoleDetailView.as_view(), name='role-detail'),

    path('classrooms/', ClassroomListCreateView.as_view(), name='classroom-list'),
    path('classrooms/<int:pk>/', ClassroomDetailView.as_view(), name='classroom-detail'),
]
