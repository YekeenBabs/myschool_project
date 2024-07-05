from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from .forms import StudentForm, DepartmentForm, SubjectForm, TeacherForm, TeacherSubjectClassForm
from .models import Student, Department, Teacher, Subject, TeacherSubjectClass


# Add student
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Use reverse for better URL handling
            return redirect(reverse('students'))
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
            # Use reverse for better URL handling
            return redirect(reverse('students'))
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

        return redirect(reverse('departments'))

    return render(request, 'add_department.html')


# Edit Department
def edit_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect(reverse('departments'))
    else:
        form = DepartmentForm(instance=department)

    return render(request, 'edit_department.html', {'form': form, 'department': department})

# department details
def departments(request):
    departments = Department.objects.all()
    return render(request, 'departments.html', {'departments': departments})

# Add Subject
def add_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subjects')
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

# Add Teacher
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to a list of teachers or another page
            return redirect('teachers')
    else:
        form = TeacherForm()
    return render(request, 'myschool_app/add_teacher.html', {'form': form})


def assign_subjects(request):
    if request.method == 'POST':
        form = TeacherSubjectClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_assignment_list')
    else:
        form = TeacherSubjectClassForm()
    return render(request, 'assign_subjects.html', {'form': form})


# from django.shortcuts import render, redirect
# from .forms import TeacherForm, TeacherAssignmentForm

# def add_teacher(request):
#     if request.method == 'POST':
#         teacher_form = TeacherForm(request.POST)
#         assignment_form = TeacherAssignmentForm(request.POST)
        
#         if teacher_form.is_valid() and assignment_form.is_valid():
#             teacher = teacher_form.save()
#             assignment = assignment_form.save(commit=False)
#             assignment.teacher = teacher
#             assignment.save()
#             return redirect('teachers')  # Redirect to the teachers list after adding
#     else:
#         teacher_form = TeacherForm()
#         assignment_form = TeacherAssignmentForm()
    
#     return render(request, 'add_teacher.html', {
#         'teacher_form': teacher_form,
#         'assignment_form': assignment_form,
#     })
