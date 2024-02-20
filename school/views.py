from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import AdminSignupForm,StudentSignupForm,ExtraStudentForm,TeacherExtraForm,TeacherSignupForm,AttendanceForm,AskDateForm,NoticeForm
from django.contrib.auth.models import Group
from .models import StudentExtraForm,Teacherextraform,Attendance,Notice
from django.db.models import Sum


# Create your views here.


def home(request):
    return render(request,'home.html')

def AdminSignupView(request):
    if request.method == 'POST':
        form1 = AdminSignupForm(request.POST)
        if form1.is_valid():
            print('working perfecly')
            user = form1.save()
            print(user.username)

            user.set_password(user.password)
            user.save()
            Admin_user_group= Group.objects.get_or_create(name='ADMIN')
            Admin_user_group[0].user_set.add(user)
            return redirect("adminlogin")

    print('some error om ADmin signup')
 
    form1 = AdminSignupForm()
    return render(request,'Adminsignup.html',{'form':form1})

def StudentSignupView(request):
    if request.method == 'POST':
        form1 = StudentSignupForm(request.POST)
        form2 = ExtraStudentForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()

            f2 = form2.save(commit=False)
            f2.user = user
            f2.save()

            Student_user_group= Group.objects.get_or_create(name='STUDENT')
            Student_user_group[0].user_set.add(user)
            return redirect("studentlogin")

    
    form1 = StudentSignupForm()
    form2 = ExtraStudentForm()
    return render(request,'Studentsignup.html',{'form1':form1,'form2':form2})





def TeacherSignup_Form(request):
    if request.method == 'POST':
        form1 = TeacherSignupForm(request.POST)
        form2 = TeacherExtraForm(request.POST)

        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            f2.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            print('ok')
            return redirect('teacherlogin')
    print('something is wrong')
    form1 = TeacherSignupForm()
    form2 = TeacherExtraForm()
    
    return render(request,'teachersignup.html',{'form1':form1,'form2':form2})




# to check if the user is ADMIN STUDENT or TEACHER
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()





###################

def after_login(request):
    if is_admin(request.user):
        print('working fine')
        return redirect("admindashboard")
    elif is_teacher(request.user):
        teacher = Teacherextraform.objects.filter(user_id = request.user.id,status = True)
        if teacher:
            return redirect("teacherdashboard")
        else:
            return render(request,'school/teacher_wait_for_approval.html')
    elif is_student(request.user):
        student = StudentExtraForm.objects.filter(user_id = request.user.id,status = True)
        if student:
            return redirect("studentdashboard")
        else:
            return render(request,'student_wait_approvel.html')
    else:
        print('user is not defined.')



@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount = Teacherextraform.objects.all().filter(status = True).count()
    print(teachercount)
    pendingteacher = Teacherextraform.objects.all().filter(status=False).count()
    print(pendingteacher)

    studentcount = StudentExtraForm.objects.filter(status = True).count()
    print(studentcount)
    pendingstudent = StudentExtraForm.objects.filter(status = False).count()
    print(pendingstudent)

    teacher_payment = Teacherextraform.objects.filter(status = True).aggregate(Sum('sallery',default=0))
    #{'sallery__sum': None} <- output
    print(teacher_payment)
    pending_teacher_payment = Teacherextraform.objects.filter(status= False).aggregate(Sum('sallery',default=0))
    # {'sallery__sum': None} <- output
    print(pending_teacher_payment)
    studentfee = StudentExtraForm.objects.filter(status=True).aggregate(Sum('fee',default = 0))
    print(studentfee)
    student_pending_fee = StudentExtraForm.objects.filter(status=False).aggregate(Sum('fee',default=0))
    print(student_pending_fee)


    context = {
        'all_teacher':teachercount,
        'pending_teacher':pendingteacher,
        'all_student':studentcount,
        'pending_student':pendingstudent,
        'teacher_payment':teacher_payment['sallery__sum'],
        'teacher_pending_payment':pending_teacher_payment['sallery__sum'],
        'student_fee':studentfee['fee__sum'],
        'student_pending_fee':student_pending_fee['fee__sum']
    }

    return render(request,'admindashboard.html',context)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_teacher(request):
    return render(request,'admin-teacher.html')


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_teacher_View(request):
    if request.method == 'POST':
        form1 = TeacherSignupForm(request.POST)
        form2 = TeacherExtraForm(request.POST)
        
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            f2 = form2.save(commit=False)
            f2.user = user
            f2.status = True
            f2.save()

            my_teacher_group = Group.objects.get_or_create(name="TEACHER")
            my_teacher_group[0].user_set.add(user)
            return redirect('admin_add_teacher')
    else:
        form1 = TeacherSignupForm()
        form2 = TeacherExtraForm()
    
    return render(request,'admin_add_teacher.html',{'form1':form1,'form2':form2})


#template where all the approved teachers are present.
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_teacher_View(request):
    teachers = Teacherextraform.objects.all().filter(status=True)
    print(teachers)
    return render(request,'admin_teacher_view.py',{'teachers':teachers})


#template where all the non aprovel teachers are.
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_aprove_teacher_view(request):
    teachers = Teacherextraform.objects.all().filter(status = False)
    return render(request,'admin_aprove_teacher_view.html',{'teachers':teachers})



#approve the teacher
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_teacher_aprove(request,sno):
    teacher = Teacherextraform.objects.get(id=sno)
    print(teacher)
    teacher.status = True
    teacher.save()
    return redirect(reverse('admin_aprove_teacher_view'))



#delete the teachers if you dont want to approve them

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_aprove_teacher(request,sno):
    teacher = Teacherextraform.objects.get(id = sno)
    print(teacher)
    user = User.objects.get(id = teacher.user_id)
    teacher.delete()
    user.delete()
    return redirect(reverse('admin_aprove_teacher_view'))



#payment
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def view_teacher_salary(request):
    teachers = Teacherextraform.objects.filter(status = True)
    return render(request,'teacher_salary.html',{'teachers':teachers})


#update the infromations of aproved teachers.

# def update_teacher_info(request,sno):
#     teacher = Teacherextraform.objects.get(id = sno)
#     user = User.objects.get(id = teacher.user_id)
#     if request.method == 'POST':
#         form1 = TeacherSignupForm(request.POST,instance=user)
#         form2 = TeacherExtraForm(request.POST,instance=teacher)
#         if form1.is_valid() and form2.is_valid():
#             user = form1.save()
#             user.set_password(user.password)
#             user.save()
#             f2 = form2.save(commit=False)
#             f2.user = user
#             f2.save()
#     form1 = TeacherSignupForm(instance=user)
#     form2 = TeacherExtraForm(instance=teacher)        
#     return render(request,"update_teacher_info.html",{'form1':form1,'form2':form2})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_teacher_info(request,sno):
    teacher = Teacherextraform.objects.get(id = sno)
    user = User.objects.get(id = teacher.user_id)
    
    if request.method == 'POST':
        form1 =TeacherSignupForm(request.POST,instance=user)
        form2 = TeacherExtraForm(request.POST,instance=teacher)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            f2.save()
    
    form1 =TeacherSignupForm(instance=user)
    form2 = TeacherExtraForm(instance=teacher)

    return render(request,"update_teacher_info.html",{'form1':form1,'form2':form2})


#delete Teacher

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher(request,sno):
    teacher = Teacherextraform.objects.get(id=sno)
    user = User.objects.get(id = teacher.user_id)
    teacher.delete()
    user.delete()
    return redirect(reverse('admin_teacher_view'))



#student infoo...

@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_student(request):
    return render(request,'admin_student.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_Add_student(request):
    if request.method == 'POST':
        form1= StudentSignupForm(request.POST)
        form2= ExtraStudentForm(request.POST)

        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            f2.status = True
            f2.save()
            Student_user_group= Group.objects.get_or_create(name='STUDENT')
            Student_user_group[0].user_set.add(user)

    form1= StudentSignupForm()
    form2= ExtraStudentForm()        
    return render(request,'admin_add_student.html',{'form1':form1,'form2':form2})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_view(request):
    students = StudentExtraForm.objects.all().filter(status = True)
    return render(request,"admin_student_view.html",{'students':students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_student(request):
    students = StudentExtraForm.objects.all().filter(status = False)
    return render(request,"admin_approve_student.html",{'students':students})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_now_approve_student(request,sno):
    student = StudentExtraForm.objects.get(id = sno)
    student.status = True
    student.save()
    return redirect(reverse('admin_approve_student'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_not_approve_student(request,sno):
    student = StudentExtraForm.objects.get(id = sno)
    user = User.objects.get(id= student.user_id)
    student.delete()
    user.delete()
    return redirect(reverse('admin_approve_student'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_fee(request):
    students = StudentExtraForm.objects.filter(status=True)
    return render(request,'admin_student_fee.html',{'students':students})


#update student informations
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_update(request,sno):
    student = StudentExtraForm.objects.get(id = sno)
    user = User.objects.get(id=student.user_id)

    if request.method == 'POST':
        form1 = StudentSignupForm(request.POST,instance=user)
        form2 = ExtraStudentForm(request.POST,instance=student)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit = False)
            f2.satus = True
            f2.save()
    form1 = StudentSignupForm(instance=user)
    form2 = ExtraStudentForm(instance=student)
    return render(request,'admin_student_update.html',{'form1':form1,'form2':form2})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_delete_student(request,sno):
    student = StudentExtraForm.objects.get(id = sno)
    user = User.objects.get(id= student.user_id)
    student.delete()
    user.delete()
    return redirect(reverse('admin_student_view'))


################ attendance
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_attendance(request):
    return render(request,'attendance_view.html')



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_take_attendance_view(request,cls):
#     students = StudentExtraForm.objects.all().filter(cls=cls)
#     aform = AttendanceForm()
#     if request.method == 'POST':
#         form = AttendanceForm(request.POST)
#         if form.is_valid():
#             Attendances = request.POST.getlist('present_status')
#             date = form.cleaned_data['date']

#             for x in range(len(Attendances)):
#                 AttendanceModel = Attendance() #this is a modeel from models.py
#                 AttendanceModel.cls = cls
#                 AttendanceModel.date = date
#                 AttendanceModel.present_status = Attendances[x]
#                 AttendanceModel.roll_no = students[x].roll_no
#                 AttendanceModel.save()
#             return redirect('admin_attendance')
#         else:
#             print('form invalid')
#         return render(request,'admin_take_attendance.html',{'students':students,'aform':aform})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_take_attendance_view(request, cls):
    students = StudentExtraForm.objects.all().filter(cls=cls)
    aform = AttendanceForm()

    if request.method == 'POST':
        aform = AttendanceForm(request.POST)

        if aform.is_valid():
            Attendances=request.POST.getlist('present_choices')    
            date=aform.cleaned_data['date']
            for x in range(len(Attendances)):
                attendance_model = Attendance()
                attendance_model.student = students[x].user
                attendance_model.cls = cls
                attendance_model.roll_no = students[x].roll_no
                attendance_model.present_choices= Attendances[x]
                attendance_model.date = date
                attendance_model.save()
 
            return redirect(reverse('admin_attendance'))
        else:
            print('not working fine')
            pass
    else:
         print('Form Errors:', aform.errors)


    return render(request, 'admin_take_attendance.html', {'students': students, 'aform': aform})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def view_students_attendance(request,cls):
    if request.method == 'POST':
        form = AskDateForm(request.POST)
        if form.is_valid():
            specific_date = form.cleaned_data['date']
            students = Attendance.objects.all().filter(date=specific_date)
            print('this is the student :',students)
            return render(request,'see_attedance.html',{'students':students})
        else:
            print('mohit something went wrong')
    date = AskDateForm()
    return render(request,'student_class_attendance_view.html',{'date':date})

############## admin fee

def students_fees_view(request):
    return render(request,"admin_fee.html")

def view_fee_per_class(request,cls):
    students = StudentExtraForm.objects.all().filter(cls=cls)
    
    return render(request,'view_fee_per_class.html',{'feedetails':students})




########## write notice


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def Write_notice(request):
    if request.method == 'POST':
        form1 = NoticeForm(request.POST)
        if form1.is_valid():
            form1.save(commit=False)
            form1.posted_by = request.user.first_name
            form1.save()
            print('This',form1.posted_by)
            return redirect(reverse('Write_notice'))
        return
    form1 = NoticeForm()    
    return render(request,'notice.html',{'form1':form1})


############################## Teacher Login ########


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacherdashboard(request):
    teacher = Teacherextraform.objects.get(status=True,user_id=request.user.id)
    notice = Notice.objects.all()
    print('this is',teacher)
    return render(request,'teacher_dashboard.html',{'teacher':teacher,'notice':notice})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_attendance(request):
    return render(request,'teacher_attendance.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_stud_attendance(request,cls):
    students = StudentExtraForm.objects.all().filter(cls=cls,status=True)
    aform = AttendanceForm()
    if request.method == 'POST':

        aform = AttendanceForm(request.POST)
        if aform.is_valid():
            Attendances = request.POST.getlist('present_choices')
            date = aform.cleaned_data['date']
            print(Attendances)
            print(date)
            for x in range(len(Attendances)):
                attendance_model = Attendance() # or insted of aform of forms.py you can also use direct class of models.py (Attendance)
                attendance_model.student=students[x].user
                print('this is:',attendance_model.student)
                attendance_model.cls=cls
                attendance_model.roll_no = students[x].roll_no
                attendance_model.present_choices = Attendances[x]
                attendance_model.date = date
                attendance_model.save()
                
            return redirect(reverse('teacher_attendance'))
    
    return render(request,'set_stud_attendance.html',{'aform':aform,'students':students})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_stud_attendance_view(request,cls):

    
    if request.method == 'POST':
        form = AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            attendancedata = Attendance.objects.all().filter(date=date,cls=cls)
            students = StudentExtraForm.objects.all().filter(cls=cls,status=True)

            mylist = zip(attendancedata,students)
            return render(request,'see_stud_attendance.html',{'cls':cls,'mylist':mylist,'date':date})
    date = AskDateForm()
    return render(request,'show_attendance.html',{'date':date})


############## Teacher Notice ########3
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_write_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            writer = form.save(commit=False)
            writer.posted_by = request.user.first_name
            writer.save()
            return redirect('teacherdashboard')
    form = NoticeForm()
    return render(request,'teacher_notice.html',{'form':form})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard(request):
    student = StudentExtraForm.objects.get(user=request.user)
    print(student)
    return render(request,'student_dashboard.html',{'student':student})


def student_check_attendance(request):
    if request.method=='POST':
        form = AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            print(date)
            return render(request,"student_see_attendance.html")
    form=AskDateForm()
    return render(request,'student_check_attendance.html',{'form':form})
