# main_app/serializers.py
from rest_framework import serializers
from .models import CustomUser, Role, ClassRoom, AttendanceProcess, Report


# ---------- Role Serializer ----------
# class RoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = ['id', 'name']


# ---------- CustomUser Serializer ----------


# ---------- Current User Serializer ----------
class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']
        depth = 1  # يرجع تفاصيل الدور بدل فقط الـ ID


# ---------- ClassRoom Serializer ----------
class ClassRoomSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()

    class Meta:
        model = ClassRoom
        fields = ['id', 'name', 'year', 'teacher', 'students']  # assuming 'teacher' is added to the model

    def get_students(self, obj):
        students = CustomUser.objects.filter(classroom=obj, role='Student')
        return CustomUserSerializer(students, many=True).data


class CustomUserSerializer(serializers.ModelSerializer):

    classroom = ClassRoomSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role', 'classroom']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        pwd = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(pwd)
        user.save()
        return user



# ---------- AttendanceProcess Serializer ----------
class AttendanceProcessSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='Student'),
        write_only=True
    )
    classroom = ClassRoomSerializer(read_only=True)
    classroom_id = serializers.PrimaryKeyRelatedField(
        queryset=ClassRoom.objects.all(),
        source='classroom',
        write_only=True
    )

    class Meta:
        model = AttendanceProcess
        fields = [
            'id',
            'date',
            'status',
            'note',
            'student', 'student_id',
            'classroom', 'classroom_id',
        ]


# ---------- Report Serializer ----------
class ReportSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='created_by',
        write_only=True
    )
    attendance = AttendanceProcessSerializer(read_only=True)
    attendance_id = serializers.PrimaryKeyRelatedField(
        queryset=AttendanceProcess.objects.all(),
        source='attendance',
        write_only=True
    )

    class Meta:
        model = Report
        fields = [
            'id',
            'title',
            'created_at',
            'content',
            'created_by', 'created_by_id',
            'attendance', 'attendance_id'
        ]
