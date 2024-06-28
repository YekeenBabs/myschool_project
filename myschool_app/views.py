from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from .forms import StudentForm
from .models import Student


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
