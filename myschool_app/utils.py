from django.template.backends import django
from django.contrib.auth import get_user_model

PARENT_GROUP_NAME = 'Parents'
STUDENT_GROUP_NAME = 'Students'
TEACHER_GROUP_NAME = 'Teachers'
ADMIN_GROUP_NAME = 'Admin'


def create_groups():
    django.contrib.auth.models.Group.objects.get_or_create(name=PARENT_GROUP_NAME)
    django.contrib.auth.models.Group.objects.get_or_create(name=STUDENT_GROUP_NAME)
    django.contrib.auth.models.Group.objects.get_or_create(name=TEACHER_GROUP_NAME)
    django.contrib.auth.models.Group.objects.get_or_create(name=ADMIN_GROUP_NAME)


def create_parent_user(username, password, email):
    user = get_user_model().objects.create_user(username, email, password)
    parent_group = django.contrib.auth.models.Group.objects.get(name=PARENT_GROUP_NAME)
    user.groups.add(parent_group)
    # Add any additional profile information
    user.save()


"""
def create_parent_user(username, password, email, first_name, last_name, phone_number):
    user = User.objects.create_user(username, email, password)
    parent = Parent.objects.create(user=user, first_name=first_name, last_name=last_name, phone_number=phone_number)
    # Add to a parent group if needed (similar to the previous example)
    parent.save()
    return user  # Returning the user object can be useful for further actions
"""

def create_student_user(username, password, email):
    user = get_user_model().objects.create_user(username, email, password)
    student_group = django.contrib.auth.models.Group.objects.get(name=STUDENT_GROUP_NAME)
    user.groups.add(student_group)
    # Add any additional profile information
    user.save()


def create_teacher_user(username, password, email):
    user = get_user_model().objects.create_user(username, email, password)
    teacher_group = django.contrib.auth.models.Group.objects.get(name=TEACHER_GROUP_NAME)
    user.groups.add(teacher_group)
    # Add any additional profile information
    user.save()


def create_admin_user(username, password, email):
    user = get_user_model().objects.create_user(username, email, password)
    admin_group = django.contrib.auth.models.Group.objects.get(name=ADMIN_GROUP_NAME)
    user.groups.add(admin_group)
    # Add any additional profile information
    user.save()

from .models import Notification

def create_notification(user, message):
    Notification.objects.create(user=user, message=message)
