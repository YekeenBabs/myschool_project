from django.contrib import admin
from .models import (
    CustomUser, Department, Class, LectureVideo,
    Student, Teacher, Subject, Quiz, Question,
    Option, Notification, StudentQuizAttempt,
    TeacherSubjectClass, TeacherClass, Attendance,
    LectureNote, Assignment, Result, Parent,
    UserProfile
)
from django.utils import timezone
from datetime import timedelta

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Notification)
admin.site.register(StudentQuizAttempt)
admin.site.register(TeacherSubjectClass)
admin.site.register(UserProfile)

# Custom admin classes
@admin.register(TeacherClass)
class TeacherClassAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'class_assigned')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'class_assigned__name')
    list_filter = ('teacher', 'class_assigned')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['date', 'student', 'status']
    list_filter = ['date']

    def changelist_view(self, request, extra_context=None):
        if request.GET.get('date__gte') and request.GET.get('date__lte'):
            date_format = '%Y-%m-%d'
            start_date = timezone.datetime.strptime(request.GET.get('date__gte'), date_format)
            end_date = timezone.datetime.strptime(request.GET.get('date__lte'), date_format) + timedelta(days=1)

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'department', 'subject_specialization',)
    search_fields = ('first_name', 'last_name', 'subject_specialization')
    list_filter = ('department',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth',)
    search_fields = ('first_name', 'last_name')
    list_filter = ('date_of_birth',)


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    search_fields = ('first_name', 'last_name')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'subject_code', 'subject_department',)
    search_fields = ('subject_name', 'subject_code',)
    list_filter = ('subject_department',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('students',)  # Removed 'teachers' if causing issues


@admin.register(LectureNote)
class LectureNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'class_associated', 'teacher', 'document_week', 'uploaded_at')
    search_fields = ('title', 'description')
    list_filter = ('subject', 'class_associated', 'teacher', 'document_week', 'uploaded_at')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'due_date',)
    search_fields = ('title',)
    list_filter = ('subject', 'teacher', 'due_date',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher')
    search_fields = ('title',)
    list_filter = ('subject', 'teacher',)


@admin.register(LectureVideo)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher')
    search_fields = ('title',)
    list_filter = ('subject', 'teacher')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score')
    search_fields = ('student__first_name', 'student__last_name', 'subject__name')
    list_filter = ('subject',)



    
