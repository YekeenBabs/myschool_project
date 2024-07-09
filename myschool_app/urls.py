from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Ensure you import the views module

urlpatterns = [
    # Student URLs
    path('students/add/', views.add_student, name='add_student'),
    path('students/edit/<int:student_id>/',
         views.edit_student, name='edit_student'),
    path('students/list/', views.students, name='students'),
    path('students/details/<int:student_id>/',
         views.student_details, name='student_details'),
    path('students/search/', views.search_students, name='search_students'),
    path('students/bulk-delete/', views.bulk_delete_students,
         name='bulk_delete_students'),

    # Department URLs
    path('add_department/', views.add_department, name='add_department'),
    path('departments/', views.departments, name='departments'),
    path('edit_department/<int:department_id>/',
         views.edit_department, name='edit_department'),

    # Subject URLs
    path('subjects/add/', views.add_subject, name='add_subject'),
    path('subjects/edit/<int:pk>/', views.edit_subject, name='edit_subject'),
    path('subjects/', views.subjects, name='subjects'),

    # Teacher URLs
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('teachers/edit/<int:teacher_id>/',
         views.edit_teacher, name='edit_teacher'),
    path('teachers/details/<int:teacher_id>/',
         views.teacher_details, name='teacher_details'),
    path('teacher_grid/', views.teacher_grid,
         name='teacher_grid'),  # Ensure this view exists
    path('download_teachers/', views.download_teachers,
         name='download_teachers'),  # Ensure this view exists
    path('teachers/', views.teacher_list, name='teachers'),
    path('assign_subjects/', views.assign_subjects, name='assign_subjects'),

    # Other URL patterns as necessary


    # path('teacher/<int:teacher_id>/', views.teacher_details, name='teacher_details'),
]    

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
