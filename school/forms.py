from django.contrib.auth.models import User
from django import forms
from .models import StudentExtraForm,Teacherextraform,Attendance,Notice


class AdminSignupForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("first_name","last_name","username","email","password")
        widgets = {
            "first_name": forms.TextInput(attrs={'class':'form-control'}),
            "last_name": forms.TextInput(attrs={'class':'form-control'}),
            "username": forms.TextInput(attrs={'class':'form-control'}),
            "email": forms.EmailInput(attrs={'class':'form-control'}),
            "password": forms.PasswordInput(attrs={'class':'form-control'}),
        }



class StudentSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name","last_name","username","email","password")
        widgets = {
            "first_name": forms.TextInput(attrs={'class':'form-control'}),
            "last_name": forms.TextInput(attrs={'class':'form-control'}),
            "username": forms.TextInput(attrs={'class':'form-control'}),
            "email": forms.EmailInput(attrs={'class':'form-control'}),
            "password": forms.PasswordInput(attrs={'class':'form-control'}),
        }


class ExtraStudentForm(forms.ModelForm):
    class Meta:
        model = StudentExtraForm
        fields = ("roll_no","cls",'mobile','fee')

        widgets = {
            "roll_no": forms.TextInput(attrs={'class':'form-control'}),
            "cls": forms.Select(attrs={'class':'form-control'}),
            "mobile": forms.TextInput(attrs={'class':'form-control'}),
            "fee": forms.TextInput(attrs={'class':'form-control'}),

        }



class TeacherSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name","last_name","username","email","password")
        widgets={
            "first_name":forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            "password": forms.PasswordInput(attrs={'class':'form-control'}),
        }


class TeacherExtraForm(forms.ModelForm):
    class Meta:
        model = Teacherextraform
        fields = ("sallery","joined_date","mobile")
        widgets = {
            'sallery':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.TextInput(attrs={'class':'form-control'}),
            'joined_date':forms.DateInput(attrs={'class':'form-control'})
        }


        


# for Attendance related form
# presence_choices=(('Present','Present'),('Absent','Absent'))
# class AttendanceForm(forms.Form):
#     present_status = forms.ChoiceField(choices=presence_choices)
#     date = forms.DateField()

presence_choices=(('Present','Present'),('Absent','Absent'))
class AttendanceForm(forms.ModelForm):
    present_choices = forms.ChoiceField(choices=presence_choices)
    class Meta:
        model = Attendance
        fields = ['present_choices','date'] # dont add extra elements here only use that one which are required
        widgets = {
            'date':forms.DateInput(attrs={'class':'form-control','placeholder': 'Type date as in this format : mm/dd/year'})
        }

# ask date from
class AskDateForm(forms.Form):
    date = forms.DateField()



############ NOtice Form#########3


class NoticeForm(forms.ModelForm):
    
    class Meta:
        model = Notice
        fields = ("posted_by","posted_on","message")
        widgets={
            'posted_by':forms.TextInput(attrs={'class':'form-control', 'style': 'width: 300px; height: 40px;'}),
            'posted_on':forms.DateInput(attrs={'class':'form-control', 'style': 'width: 300px; height: 40px;'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'style': ' width: 800px; text-align: left;'}),

        }
