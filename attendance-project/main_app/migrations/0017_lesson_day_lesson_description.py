# Generated by Django 5.2 on 2025-05-07 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_lesson_remove_studentprofile_classroom_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='day',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
