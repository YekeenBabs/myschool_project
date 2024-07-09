from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from .forms import StudentForm, DepartmentForm, SubjectForm, TeacherForm, TeacherSubjectClassForm
from .models import Student, Department, Teacher, Subject, TeacherSubjectClass
from django.http import HttpResponse
import csv


# STUDENT VIEWS.PY

# Add student
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student_data = form.cleaned_data
            # Set "Not Available" status explicitl
            student_data['result'] = {
                "subject": "",
                "score": 0,
                "grade": "NA",
                "status": "Not Available"
                }
            student = Student.objects.create(**student_data)
            messages.success(request, 'Student added successfully.')
            # Use reverse for better URL handling
            return redirect(reverse('students'))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})


# Edit student
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            # Use reverse for better URL handling
            return redirect(reverse('students'))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm(instance=student)
    return render(request, 'edit_student.html', {'form': form})


# Students list
def students(request):
    students = Student.objects.all()
    return render(request, 'students.html', {'students': students})


# Search students
def search_students(request):
    search_by_id = request.GET.get('searchById', '')
    search_by_name = request.GET.get('searchByName', '')
    search_by_phone = request.GET.get('searchByPhone', '')

    students = Student.objects.all()

    if search_by_id:
        students = students.filter(id__icontains=search_by_id)
    if search_by_name:
        students = students.filter(name__icontains=search_by_name)
    if search_by_phone:
        students = students.filter(phone__icontains=search_by_phone)

    serialized_students = [{'id': student.id, 'name': student.name,
                            'phone': student.phone} for student in students]

    return JsonResponse(serialized_students, safe=False)


# Bulk delete students
def bulk_delete_students(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')
        Student.objects.filter(id__in=ids).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


# Student details
def student_details(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'student_details.html', {'student': student})


# DEPARTMENT VIEWS.PY

# Add department
def add_department(request):
    if request.method == 'POST':
        department_id = request.POST['department_id']
        department_name = request.POST['department_name']
        head_of_department = request.POST['head_of_department']
        start_date = request.POST['start_date']
        number_of_students = request.POST['number_of_students']
        description = request.POST.get('description', '')

        Department.objects.create(
            department_id=department_id,
            department_name=department_name,
            head_of_department=head_of_department,
            start_date=start_date,
            number_of_students=number_of_students,
            description=description
        )
        messages.success(request, 'Department added successfully.')
        return redirect(reverse('departments'))
    else:
        messages.error(request, 'Please correct the errors below.')

    return render(request, 'add_department.html')


# Edit Department
def edit_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'DEpartment updated successfully.')
            return redirect(reverse('departments'))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DepartmentForm(instance=department)

    return render(request, 'edit_department.html', {'form': form, 'department': department})


# department details
def departments(request):
    departments = Department.objects.all()
    return render(request, 'departments.html', {'departments': departments})


# Search departments
def search_departments(request):
    search_by_id = request.GET.get('searchById', '')
    search_by_name = request.GET.get('searchByName', '')
    search_by_phone = request.GET.get('searchByPhone', '')

    departments = Department.objects.all()

    if search_by_id:
        departments = departments.filter(id__icontains=search_by_id)
    if search_by_name:
        departments = departments.filter(name__icontains=search_by_name)
    if search_by_phone:
        departments = departments.filter(phone__icontains=search_by_phone)

    serialized_departments = [{'id': department.id, 'name': department.name,
                               'phone': department.phone} for department in departments]

    return JsonResponse(serialized_departments, safe=False)


# Bulk delete departments
def bulk_delete_departments(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')
        Department.objects.filter(id__in=ids).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


# SUBJECTS VIEWS.PY

# Add Subject
def add_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added successfully.')
            return redirect('subjects')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SubjectForm()

    departments = Department.objects.all()
    teachers = Teacher.objects.all()

    return render(request, 'add_subject.html', {
        'form': form,
        'departments': departments,
        'teachers': teachers,
    })


# Edit Subject
def edit_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully.')
            return redirect('subjects')
    else:
        form = SubjectForm(instance=subject)

    return render(request, 'edit_subject.html', {
        'form': form,
        'subject': subject,
    })


# Subject details
def subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects.html', {'subjects': subjects})


# Search subjects
def search_subjects(request):
    search_by_id = request.GET.get('searchById', '')
    search_by_name = request.GET.get('searchByName', '')
    search_by_phone = request.GET.get('searchByPhone', '')

    subjects = Subject.objects.all()

    if search_by_id:
        subjects = subjects.filter(id__icontains=search_by_id)
    if search_by_name:
        subjects = subjects.filter(name__icontains=search_by_name)
    if search_by_phone:
        subjects = subjects.filter(phone__icontains=search_by_phone)

    serialized_subjects = [{'id': subject.id, 'name': subject.name,
                            'phone': subject.phone} for subject in subjects]

    return JsonResponse(serialized_subjects, safe=False)


# Bulk delete subjects
def bulk_delete_subjects(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')
        Subject.objects.filter(id__in=ids).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


# TEACHER VIEWS.PY

# Add Teacher
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher added successfully.')
            # Redirect to a list of teachers or another page
            return redirect('teachers')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherForm()

    return render(request, 'myschool_app/add_teacher.html', {'form': form})


# Assign subjects
def assign_subjects(request):
    if request.method == 'POST':
        form = TeacherSubjectClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_assignment_list')
    else:
        form = TeacherSubjectClassForm()
    return render(request, 'assign_subjects.html', {'form': form})


# edit teacher
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher updated successfully.')
            return redirect('teachers')  # Redirect to teachers list page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherForm(instance=teacher)

    return render(request, 'myschool_app/edit_teacher.html', {'form': form, 'teacher': teacher})


# teachers
def teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'myschool_app/teachers.html', {'teachers': teachers})


# list of all teachers
def teacher_list(request):
    teachers = Teacher.objects.all()
    context = {
        'teachers': teachers
    }
    return render(request, 'teachers.html', context)


# Details of a specific teacher
def teacher_details(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'myschool_app/teacher_details.html', {'teacher': teacher})


# teacher grid
def teacher_grid(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_grid.html', {'teachers': teachers})


# teacher download
def download_teachers(request):
    teachers = Teacher.objects.all()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="teachers.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['Name', 'Class', 'Department', 'Email', 'Mobile Number'])

    for teacher in teachers:
        writer.writerow([teacher.name, teacher.class_name,
                        teacher.department, teacher.email, teacher.mobile_number])

    return response


# Search teachers
def search_teachers(request):
    search_by_id = request.GET.get('searchById', '')
    search_by_name = request.GET.get('searchByName', '')
    search_by_phone = request.GET.get('searchByPhone', '')

    teachers = Teacher.objects.all()

    if search_by_id:
        teachers = teachers.filter(id__icontains=search_by_id)
    if search_by_name:
        teachers = teachers.filter(name__icontains=search_by_name)
    if search_by_phone:
        teachers = teachers.filter(phone__icontains=search_by_phone)

    serialized_teachers = [{'id': teacher.id, 'name': teacher.name,
                            'phone': teacher.phone} for teacher in teachers]

    return JsonResponse(serialized_teachers, safe=False)


# Bulk delete teachers
def bulk_delete_teachers(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')
        Teacher.objects.filter(id__in=ids).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)
