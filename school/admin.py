from django.contrib import admin
from .models import StudentExtraForm,Teacherextraform,Attendance,Notice

# Register your models here.
admin.site.register(StudentExtraForm)
admin.site.register(Teacherextraform)
admin.site.register(Attendance)
admin.site.register(Notice)
