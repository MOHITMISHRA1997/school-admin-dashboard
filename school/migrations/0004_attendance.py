# Generated by Django 4.2.3 on 2023-08-22 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_teacherextraform_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_no', models.CharField(max_length=10, null=True)),
                ('date', models.DateField()),
                ('cls', models.CharField(max_length=10)),
                ('present_status', models.CharField(max_length=10)),
            ],
        ),
    ]
