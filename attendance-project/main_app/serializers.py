# main_app/serializers.py
from rest_framework import serializers
from .models import CustomUser, Role, ClassRoom, AttendanceProcess

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'role_type']

class CustomUserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source='role',
        write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role', 'role_id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        pwd = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(pwd)
        user.save()
        return user

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['id', 'name', 'year', 'role']

class AttendanceProcessSerializer(serializers.ModelSerializer):
    # إذا أردت تضمين بيانات الدور والغرفة كاملة:
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source='role',
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
            'role', 'role_id',
            'classroom', 'classroom_id',
        ]
