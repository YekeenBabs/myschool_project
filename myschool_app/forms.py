from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
)
from .models import (
    Student, CustomUser, Quiz, Question, Option, Answer, Teacher, Skill,
    Lesson, Event, ClassArm, Grade, Submission, Project, LectureVideo, Assignment,
    Department, Subject, Class, TeacherSubjectClass
)
from .validators import CustomPasswordValidator
from django.core.exceptions import ValidationError


# Student form
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'datetimepicker'}),
            'gender': forms.Select(attrs={'class': 'form-control select'}),
            'student_class': forms.Select(attrs={'class': 'form-control select'}),
            'photo': forms.FileInput(),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise ValidationError('Name should be at least 2 characters long.')
        return name

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('date_of_birth')
        admin_number = cleaned_data.get('admin_number')
        if dob and admin_number:
            if dob.year > 2000 and not admin_number.startswith('20'):
                raise ValidationError(
                    'Admin number should start with "20" for students born after 2000.')
        return cleaned_data


# department form
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_id', 'department_name', 'head_of_department',
                  'start_date', 'number_of_students', 'description']

# subject form
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_code', 'subject_name', 'subject_department',
                  'assigned_teacher', 'description', 'no_of_students']
        widgets = {
            'assigned_teacher': forms.CheckboxSelectMultiple,
        }

# teacher form
class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Teacher
        fields = [
            'employee_id', 'first_name', 'last_name', 'middle_name', 'email',
            'phone_number', 'date_of_birth', 'highest_qualification', 'certifications',
            'department', 'office_location', 'profile_picture', 'bio', 'subject_specialization',
            'classes', 'subject_taught'
        ]
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'type': 'tel'}),
            'email': forms.EmailInput(),
            'profile_picture': forms.FileInput(),
            'classes': forms.CheckboxSelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = user.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        teacher = super().save(commit=False)
        teacher.user = user
        if commit:
            teacher.save()
            self.save_m2m()
        return teacher


class TeacherSubjectClassForm(forms.ModelForm):
    class Meta:
        model = TeacherSubjectClass
        fields = '__all__'
