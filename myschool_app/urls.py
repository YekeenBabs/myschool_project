# # myschool_app/urls.py

# from django.urls import path
# from django.conf import settings
# from django.conf.urls.static import static
# from .views import edit_student, students, student_details, search_students, add_student, bulk_delete_students

# urlpatterns = [
#     path('students/add/', add_student, name='add_student'),
#     path('students/edit/<int:student_id>/', edit_student, name='edit_student'),
#     path('students/list/', students, name='students'),
#     path('students/details/<int:student_id>/',
#          student_details, name='student_details'),
#     path('students/search/', search_students, name='search_students'),
#     path('students/bulk-delete/', bulk_delete_students,
#          name='bulk_delete_students'),
#     path('add_department/', views.add_department, name='add_department'),
#     path('departments/', views.departments, name='departments'), 
#     # Other URL patterns

# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Ensure you import views module

urlpatterns = [
    path('students/add/', views.add_student, name='add_student'),
    path('students/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('students/list/', views.students, name='students'),
    path('students/details/<int:student_id>/', views.student_details, name='student_details'),
    path('students/search/', views.search_students, name='search_students'),
    path('students/bulk-delete/', views.bulk_delete_students, name='bulk_delete_students'),
    path('add_department/', views.add_department, name='add_department'),
    path('departments/', views.departments, name='departments'), 
    path('edit_department/<int:department_id>/', views.edit_department, name='edit_department'), 
    # path('department_details/<int:department_id>/', views.department_details, name='department_details'), 
    # path('subjects/', views.subject_list, name='subjects'),  # List all subjects
    path('subjects/add/', views.add_subject, name='add_subject'),  # Add a new subject
    path('subjects/edit/<int:pk>/', views.edit_subject, name='edit_subject'),  # Edit an existing subject
    path('subjects/', views.subjects, name='subjects'), # List all subjects
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('assign_subjects/', views.assign_subjects, name='assign_subjects'),
    # Other URL patterns
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
