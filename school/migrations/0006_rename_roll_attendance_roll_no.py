# Generated by Django 4.2.3 on 2023-08-22 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_rename_roll_no_attendance_present_choices_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='roll',
            new_name='roll_no',
        ),
    ]
