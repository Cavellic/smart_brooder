# Generated by Django 5.1.2 on 2024-10-10 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_feedingtimetable'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedingtimetable',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
