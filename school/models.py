from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
CLASS_CHOICES = [('First','First'),('Second','Second'),('Third','Third'),('Fourth','Fourth'),('Fifth','Fifth'),('Sixth','Sixth'),('Seventh','Seventh'),('Eigth','Eigth'),('Ninth','Ninth'),('Tenth','Tenth')]

class StudentExtraForm(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    roll_no = models.PositiveIntegerField()
    cls = models.CharField(choices=CLASS_CHOICES,max_length=20,default='First')
    mobile = models.CharField(max_length=40,null=True)
    fee=models.PositiveIntegerField(null=True)
    status=models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Student {self.user}"



class Teacherextraform(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    sallery = models.PositiveIntegerField(null=False)
    joined_date = models.DateField()
    mobile = models.CharField(max_length=15)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Teacher {self.user}'

    

# class Attendance(models.Model):
#     roll_no = models.CharField(max_length=10,null=True)
#     date = models.DateField()
#     cls = models.CharField(max_length=10)
#     present_status = models.CharField(max_length=10)

class Attendance(models.Model):
    student = models.CharField(max_length=30)
    roll_no = models.CharField( max_length=50,default="")
    cls = models.CharField(max_length=10)
    present_choices = models.CharField(max_length=10,null=True)
    date = models.DateField()

    def __str__(self) -> str:
        return f'Attendance of {self.student} of class {self.cls}'
    

class Notice(models.Model):
    sno = models.AutoField(primary_key=True)
    posted_by = models.CharField(max_length=20,null=True,default='school')
    posted_on = models.DateField(default=now)
    message = models.TextField()
