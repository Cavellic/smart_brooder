# Generated by Django 5.1.2 on 2024-10-09 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_decsription_feedingtimetable_description'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FeedingTimeTable',
        ),
    ]
