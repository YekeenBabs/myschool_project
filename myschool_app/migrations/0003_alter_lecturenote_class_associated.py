# Generated by Django 5.0.4 on 2024-07-08 14:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "myschool_app",
            "0002_alter_studentprogress_document_remove_video_subject_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="lecturenote",
            name="class_associated",
            field=models.ForeignKey(
                default="default_value_here",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="documents",
                to="myschool_app.class",
            ),
        ),
    ]