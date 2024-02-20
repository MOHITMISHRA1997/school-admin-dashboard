"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('adminsignup/', views.AdminSignupView, name='adminsignup'),
    path('teachersignup/', views.TeacherSignup_Form, name='teachersignup'),
    path('studentsignup/', views.StudentSignupView, name='studentsignup'),

    path('adminlogin/', LoginView.as_view(template_name="login.html"), name='adminlogin'),
    path('teacherlogin/', LoginView.as_view(template_name="teacherlogin.html"), name='teacherlogin'),
    path('studentlogin/', LoginView.as_view(template_name="Studentlogin.html"), name='studentlogin'),
    path('adminlogout/', LogoutView.as_view(template_name="home.html"), name='adminlogout'),
    path('studentlogout/', LogoutView.as_view(template_name="home.html"), name='studentlogout'),
    path('teacherlogout/', LogoutView.as_view(template_name="home.html"), name='teacgerlogout'),


    path('after_login/', views.after_login, name='afterlogin'),
    path('admindashboard/', views.admin_dashboard_view, name='admindashboard'),
    path('admin-teacher/', views.admin_teacher, name='admin_teacher'),
    path('admin-add-teacher/', views.admin_add_teacher_View, name='admin_add_teacher'),
    path('admin-teacher-view/', views.admin_teacher_View, name='admin_teacher_view'),
    path('admin-teacher-salary/', views.view_teacher_salary, name='view_teacher_salary'),
    path('admin_aprove_teacher_view/', views.admin_aprove_teacher_view, name='admin_aprove_teacher_view'),
    path('admin_aprove_teacher/<int:sno>/', views.admin_teacher_aprove, name='admin_teacher_aprove'),
    path('delete_aprove_teacher/<int:sno>/', views.delete_aprove_teacher, name='delete_aprove_teacher'),
    path('update_teacher/<int:sno>/', views.update_teacher_info, name='update_teacher_info'),
    path('delete_teacher/<int:sno>/', views.delete_teacher, name='delete_teacher'),


    path('admin-student/', views.admin_student, name='admin_student'),


    ####################
    path('admin-add-student/', views.admin_Add_student, name='admin_add_student'),
    path('admin-student-view/', views.admin_student_view, name='admin_student_view'),
    path('admin-approve-student/', views.admin_approve_student, name='admin_approve_student'),
    path('admin_now_approve_student/<int:sno>', views.admin_now_approve_student, name='admin_now_approve_student'),
    path('admin_not_approve_student/<int:sno>', views.admin_not_approve_student, name='admin_not_approve_student'),
    path('admin_student_fee/', views.admin_student_fee, name='admin_student_fee'),
    path('admin_student_update/<int:sno>/', views.admin_student_update, name='admin_student_fee'),
    path('admin_delete_student/<int:sno>/', views.admin_delete_student, name='admin_delete_student'),
    path('admin-attendance/', views.admin_attendance, name='admin_attendance'),
    path('admin-take-attendance/<str:cls>/', views.admin_take_attendance_view, name='admin_take_attendance_view'),
    path('view-students-attendance/<str:cls>/', views.view_students_attendance, name='view_students_attendance'),

    ######################################fee

    path('admin-fee/', views.students_fees_view, name='students_fees_view'),    
    path('admin-fee-per-class/<str:cls>/', views.view_fee_per_class, name='view_fee_per_class'),    
    path('admin-notice/', views.Write_notice, name='Write_notice'),    


    ############### techer
    path('teacher-dashboard/', views.teacherdashboard, name='teacherdashboard'),    
    path('teacher-attendance/', views.teacher_attendance, name='teacher_attendance'),    
    path('teacher-set_stud_attendance/<str:cls>/', views.teacher_view_stud_attendance, name='teacher_view_stud_attendance'),    
    path('teacher-stud-attendance-view/<str:cls>/', views.teacher_stud_attendance_view, name='teacher_stud_attendance_view'), 
    path('teacher-write-notice/', views.teacher_write_notice, name='teacher_write_notice'), 

    ############## students

    path('student-dashboard/', views.student_dashboard, name='studentdashboard'), 
    path('student-check-attendance/', views.student_check_attendance, name='student_check_attendance'), 


]
