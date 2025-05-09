# Generated by Django 5.2 on 2025-05-05 08:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_remove_studentprofile_student_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='classroom',
        ),
        migrations.AddField(
            model_name='classroom',
            name='teacher',
            field=models.OneToOneField(blank=True, limit_choices_to={'role': 'Teacher'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='attendanceprocess',
            name='student',
            field=models.ForeignKey(limit_choices_to={'role': 'Student'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('teacher', 'teacher'), ('student', 'student')], max_length=50),
        ),
    ]
