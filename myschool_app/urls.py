# myschool_app/urls.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import edit_student, students, student_details, search_students, add_student, bulk_delete_students

urlpatterns = [
    path('students/add/', add_student, name='add_student'),
    path('students/edit/<int:student_id>/', edit_student, name='edit_student'),
    path('students/list/', students, name='students'),
    path('students/details/<int:student_id>/',
         student_details, name='student_details'),
    path('students/search/', search_students, name='search_students'),
    path('students/bulk-delete/', bulk_delete_students,
         name='bulk_delete_students'),
    # Other URL patterns

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
