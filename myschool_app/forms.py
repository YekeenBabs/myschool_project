from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
)
from .models import (
    Student, CustomUser, Quiz, Question, Option, Answer, Document, Teacher, Skill,
    Lesson, Event, ClassArm, Grade, Submission, Project, LectureVideo, Assignment
)
from .validators import CustomPasswordValidator
from django.core.exceptions import ValidationError


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
