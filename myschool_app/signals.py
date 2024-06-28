from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Document, Notification, Student

@receiver(post_save, sender=Document)
def send_document_upload_notification(sender, instance, created, **kwargs):
    if created:
        subject = instance.subject
        class_name = instance.class_associated

        # Notify admin and teachers
        admin_users = User.objects.filter(is_staff=True)
        teachers = User.objects.filter(groups__name='Teachers')
        for user in admin_users | teachers:
            Notification.objects.create(
                recipient=user,
                message=f'{instance.title} has been uploaded for {subject.name} ({class_name.name}).'
            )

        # Notify students
        students = Student.objects.filter(subjects=subject, classes=class_name)
        for student in students:
            Notification.objects.create(
                recipient=student.user,
                message=f'{subject.name} document for {class_name.name} has been uploaded.'
            )
