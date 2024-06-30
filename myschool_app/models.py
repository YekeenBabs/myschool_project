# Create your models here.

# models.py

from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
from .validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('admin', 'Admin'),
    )
    username_validator = RegexValidator(
        r'^[\w.@+-]+$',
        'Invalid username. Username must consist of letters, numbers, or underscores.',
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits, underscores, dots, '
            '@, +, -, and spaces allowed.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    role = models.CharField(max_length=10, choices=ROLES, default='student')
    email = models.EmailField(_('email address'), unique=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^(\+98|0)?9\d{9}$', message="Phone number must enter in this format")
    ida_regex = RegexValidator(
        regex=r'[0-9]{8}', message="ida must enter in this format")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=20, blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_superuser = models.BooleanField(_('is_superuser'), default=False)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_active = models.BooleanField(_('is_active'), default=True)
    full_name = models.CharField(_('full name'), max_length=130, blank=False)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    groups = models.ManyToManyField(
        'auth.Group', related_name='customuser_set')
    phone = models.CharField(
        validators=[phone_regex], max_length=13, unique=True, blank=False)
    ida = models.CharField(
        validators=[ida_regex], max_length=8, unique=True, blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='customuser_set_permissions', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.email


class Profile(models.Model):
    profile = models.ImageField(upload_to='profiles/')
    student_card = models.ImageField(upload_to='student_cards/')
    points = models.PositiveIntegerField(default=0)
    gender = models.BinaryField()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    verified = models.BooleanField(default=False)
    slug = models.SlugField(blank=False)

    def __str__(self):
        return self.user.full_name


class MyForm(forms.Form):
    username = forms.CharField(validators=[UnicodeUsernameValidator])


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(
        'auth.Permission', related_name='roles')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.email


class Department(models.Model):
    department_id = models.CharField(max_length=20, unique=True)
    department_name = models.CharField(max_length=100)
    head_of_department = models.CharField(max_length=100)
    start_date = models.DateField()
    number_of_students = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.department_name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    assigned_teacher = models.ManyToManyField(
        'Teacher', related_name='assigned_subjects')
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=10)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    # teachers = models.ManyToManyField('Teacher')

    def __str__(self):
        return self.name

    def get_assigned_teachers(self):
        return ", ".join([teacher.name for teacher in self.assigned_teacher.all()])


class Class(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ManyToManyField(
        'Subject', related_name='classes', blank=True)
    grade_level = models.CharField(max_length=50, blank=True)
    section = models.CharField(max_length=10, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    meeting_time = models.CharField(max_length=100, blank=True)
    classroom = models.CharField(max_length=100, blank=True)
    capacity = models.IntegerField(blank=True, null=True)
    students = models.ManyToManyField(
        'Student', related_name='enrolled_classes')
    teachers = models.ManyToManyField(
        'Teacher', blank=True, related_name='teaching_classes')
    description = models.TextField(blank=True)
    resources = models.URLField(blank=True)
    materials_list = models.TextField(blank=True)
    total_students = models.IntegerField(default=0)
    total_lessons = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    total_hours = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, default="")
    middle_name = models.CharField(max_length=255, default="")
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    highest_qualification = models.CharField(max_length=100, blank=True)
    certifications = models.TextField(blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True)
    employee_id = models.CharField(max_length=20, blank=True)
    office_location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    bio = models.TextField(blank=True)
    subject_specialization = models.CharField(max_length=100, blank=True)
    classes = models.ManyToManyField(
        Class, related_name='teachers_classes', default="")
    subject_taught = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='teachers_subjects', default="")
    subjects = models.ManyToManyField(
        Subject, through='TeacherSubjectClass', related_name='teachers')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TeacherSubjectClass(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        db_table = 'teacher_subject_class'
        unique_together = ('teacher', 'subject')

    def __str__(self):
        return f"{self.teacher} - {self.subject} - {self.class_assigned}"


class TeacherClass(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        db_table = 'teacher_class'

    def __str__(self):
        return f"{self.teacher} - {self.class_assigned}"


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_confirmed = models.BooleanField(default=False)
    class_name = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='lessons')  # Added related_name


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField(default=0)
    end_time = models.TimeField(default=0)


class Document(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='documents')
    class_associated = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='documents')
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document_week = models.IntegerField(default=1)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default='')
    week = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.subject.name} - {self.class_associated.name} - Week {self.week}"


class LectureVideo(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='videos')
    class_associated = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='videos')
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    week = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.class_associated.name} - Week {self.week}"


class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    week = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='assignments/')
    upload_date = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='received_notifications', default="")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_notifications',
                               default="")  # Changed user to sender
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.email} - Read: {self.is_read}"


class ClassArm(models.Model):
    name = models.CharField(max_length=50)
    students = models.ManyToManyField('Student', related_name='class_arms')


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=[(
        'Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    roll_number = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True)
    blood_group = models.CharField(max_length=10, choices=[(
        'B+', 'B+'), ('A+', 'A+'), ('O+', 'O+')], blank=True)
    student_class = models.CharField(max_length=20, choices=[
        ('J.S.S. 1', 'J.S.S. 1'), ('J.S.S. 2',
                                   'J.S.S. 2'), ('J.S.S. 3', 'J.S.S. 3'),
        ('S.S.S. 1', 'S.S.S. 1'), ('S.S.S. 2',
                                   'S.S.S. 2'), ('S.S.S. 3', 'S.S.S. 3')
    ])
    class_arm = models.CharField(max_length=10, choices=[(
        'A', 'A'), ('B', 'B'), ('C', 'C')], blank=True)
    department = models.CharField(max_length=50, choices=[
        ('Art', 'Art'), ('Commercial', 'Commercial'), ('Science', 'Science')
    ], blank=True)
    address = models.TextField(blank=True)
    admission_id = models.CharField(max_length=20, blank=True, null=True)
    courses = models.ManyToManyField('Course', blank=True)
    grades = models.JSONField(blank=True, null=True)
    gpa = models.FloatField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    admission_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='students/', null=True,
                              blank=True, default='students/default_student.jpg')
    bio = models.TextField(blank=True)
    profile_bg_url = models.URLField(max_length=200, blank=True, null=True)
    profile_img_url = models.URLField(max_length=200, blank=True, null=True)
    club = models.CharField(max_length=100, blank=True, null=True)
    club_duties = models.CharField(max_length=100, blank=True, null=True)
    societies = models.CharField(max_length=100, blank=True, null=True)
    societies_duties = models.CharField(max_length=100, blank=True, null=True)
    sport = models.CharField(max_length=100, blank=True, null=True)
    sport_duties = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    preferred_name = models.CharField(max_length=100, blank=True)
    registration_number = models.CharField(max_length=20, unique=True)
    grade_level = models.IntegerField()
    parent_name = models.CharField(max_length=100)
    parent_email = models.EmailField()
    parent_phone = models.CharField(max_length=15)
    classes = models.ManyToManyField(Class)
    subjects = models.ManyToManyField(Subject, related_name='students')
    student_id = models.CharField(max_length=10, default=get_random_string)
    class_assigned = models.CharField(max_length=50, default='JSS1')
    class_arm = models.CharField(max_length=10, default='A')
    ca1 = models.PositiveIntegerField(default=0)
    ca2 = models.PositiveIntegerField(default=0)
    ca3 = models.PositiveIntegerField(default=0)
    ca4 = models.PositiveIntegerField(default=0)
    test_score = models.PositiveIntegerField(default=0, null=True, blank=True)
    exam_score = models.PositiveIntegerField(default=0, null=True, blank=True)
    total_score = models.PositiveIntegerField(default=0)
    grade = models.CharField(max_length=20, default='')
    as1 = models.PositiveIntegerField(default=0, null=True, blank=True)
    as2 = models.PositiveIntegerField(default=0, null=True, blank=True)
    as3 = models.PositiveIntegerField(default=0, null=True, blank=True)
    as4 = models.PositiveIntegerField(default=0, null=True, blank=True)
    as5 = models.PositiveIntegerField(default=0, null=True, blank=True)
    as6 = models.PositiveIntegerField(default=0, null=True, blank=True)
    as7 = models.PositiveIntegerField(default=0, null=True, blank=True)
    as8 = models.PositiveIntegerField(default=0, null=True, blank=True)
    as9 = models.PositiveIntegerField(default=0, null=True, blank=True)
    as10 = models.PositiveIntegerField(default=0, null=True, blank=True)
    total_assignment = models.PositiveIntegerField(default=0)
    quiz1 = models.IntegerField(default=0, null=True, blank=True)
    quiz2 = models.IntegerField(default=0, null=True, blank=True)
    quiz3 = models.IntegerField(default=0, null=True, blank=True)
    quiz4 = models.IntegerField(default=0, null=True, blank=True)
    quiz5 = models.IntegerField(default=0, null=True, blank=True)
    quiz6 = models.IntegerField(default=0, null=True, blank=True)
    quiz7 = models.IntegerField(default=0, null=True, blank=True)
    quiz8 = models.IntegerField(default=0, null=True, blank=True)
    quiz9 = models.IntegerField(default=0, null=True, blank=True)
    quiz10 = models.IntegerField(default=0, null=True, blank=True)
    total_quiz = models.IntegerField(default=0)
    personal_project = models.IntegerField(default=0, null=True, blank=0)
    group_project = models.IntegerField(default=0, null=True, blank=0)
    class_project = models.IntegerField(default=0, null=True, blank=0)
    department_project = models.IntegerField(default=0, null=True, blank=0)
    total_project = models.IntegerField(default=0)
    assignment_score = models.IntegerField(null=True, blank=True)
    quiz_score = models.IntegerField(null=True, blank=True)
    project_score = models.IntegerField(null=True, blank=True)
    result = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def calculate_total_score(self):
        self.test_score = self.ca1 + self.ca2 + self.ca3 + self.ca4
        self.total_score = (
            self.test_score +
            self.exam_score +
            self.assignment_score +
            self.quiz_score +
            self.project_score
        )
        self.calculate_grade()
        self.save()

    def calculate_grade(self):
        if self.total_score >= 175:
            self.grade = 'A'
        elif self.total_score >= 171:
            self.grade = 'B2'
        elif self.total_score >= 165:
            self.grade = 'B3'
        elif self.total_score >= 160:
            self.grade = 'C4'
        elif self.total_score >= 155:
            self.grade = 'C5'
        elif self.total_score >= 150:
            self.grade = 'C6'
        elif self.total_score >= 145:
            self.grade = 'D7'
        elif self.total_score >= 140:
            self.grade = 'E8'
        else:
            self.grade = 'F9'

    @property
    def total_ca(self):
        return self.ca1 + self.ca2 + self.ca3 + self.ca4

    @property
    def total_assignment(self):
        return self.as1 + self.as2 + self.as3 + self.as4 + self.as5 + self.as6 + self.as7 + self.as8 + self.as9 + self.as10


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classes = models.ManyToManyField('ClassArm')


class StudentProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)


class SchoolClass(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    subjects = models.ManyToManyField('Subject', related_name='courses')

    def __str__(self):
        return self.name


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deadline = models.DateTimeField(default=timezone.now)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    # teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text


class Option(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Answer(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='answers')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f'Answer by {self.student} for {self.quiz}'


class StudentQuizAttempt(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student} attempt for {self.quiz}'


class QuizResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    attempted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)


class Parent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    contact_info = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    emergency_contact_email = models.EmailField(blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Result(models.Model):
    student = models.ForeignKey(
        Student, related_name='results', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
    remarks = models.TextField(blank=True, null=True)
    date = models.DateField()
    score = models.IntegerField()

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.grade}"


class LectureNote(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    file = models.FileField(upload_to='lecture_notes/')
    date_uploaded = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='assignments/', blank=True, null=True)
    due_date = models.DateField()
    date_assigned = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Video(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    date_uploaded = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[
                              ('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date} - {self.status}"


class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    duration = models.DurationField()
    total_marks = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class ReportCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_issued = models.DateField()
    remarks = models.TextField(blank=True, null=True)
    grades = models.JSONField()

    def __str__(self):
        return f"Report Card for {self.student}"


class Schedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    duration = models.DurationField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"Schedule for {self.subject} on {self.date} at {self.time}"


class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    payment_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=[
                              ('Paid', 'Paid'), ('Unpaid', 'Unpaid')])
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Fee for {self.student} - {self.amount}"


class LibraryBook(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=100)
    publication_date = models.DateField()
    number_of_copies = models.IntegerField()

    def __str__(self):
        return self.title


class Borrow(models.Model):
    book = models.ForeignKey(LibraryBook, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.student} borrowed {self.book}"


class YourModel:
    pass


class TeacherSubjectClass:
    pass


class Skill:
    pass


class Grade(models.Model):
    student = models.ForeignKey(
        Student, related_name='grades_assigned', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)
    type = models.CharField(max_length=50)  # Test, Exam, Assignment, etc.


class StudentProfile:
    pass


class Project(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('group', 'Group'),
        ('class', 'Class'),
        ('department', 'Department'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    project_type = models.CharField(
        max_length=50, choices=PROJECT_TYPE_CHOICES)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_projects')
    assigned_students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='assigned_projects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Submission(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    submission_file = models.FileField(upload_to='submissions/')
