# Generated by Django 5.2 on 2025-05-05 08:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_remove_customuser_classroom_classroom_teacher_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='students',
        ),
        migrations.AddField(
            model_name='customuser',
            name='classroom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='main_app.classroom'),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='teacher',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teaching_classroom', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Teacher', 'Teacher'), ('Student', 'Student')], max_length=50),
        ),
    ]
