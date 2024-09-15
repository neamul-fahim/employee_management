from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


def employee_list(request):
    employees = Employee.objects.all()

    # Filtering by search query
    name = request.GET.get('name')
    email = request.GET.get('email')
    mobile = request.GET.get('mobile')
    dob = request.GET.get('dob')
    
    if name:
        employees = employees.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
    if email:
        employees = employees.filter(email__icontains=email)
    if mobile:
        employees = employees.filter(mobile__icontains=mobile)
    if dob:
        employees = employees.filter(date_of_birth__icontains=dob)
    
    
     # Sorting
    sort_field = request.GET.get('sort')
    if sort_field:
        sort_order = request.GET.get('order', 'asc')
        if sort_order == 'desc':
            sort_field = '-' + sort_field
        employees = employees.order_by(sort_field)

    # Pagination
    paginator = Paginator(employees, 6) 
    page_number = request.GET.get('page')
    employees_page = paginator.get_page(page_number)

    context = {
        'employees': employees_page,
        'sort_field': sort_field,

    }
    return render(request, 'employee_list.html', context)


def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, 'Employee added successfully!')
    else:
        form = EmployeeForm()
    
    return render(request, 'add_employee.html', {'form': form})



def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    messages.success(request, "Employee has been deleted successfully.")
    return redirect('employee_list') 



def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    
    context = {
        'form': form,
        'employee': employee,
    }
    
    return render(request, 'edit_employee.html', context)