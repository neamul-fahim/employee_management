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
    ordering = request.GET.get('ordering', 'first_name')
    employees = employees.order_by(ordering)

    # Pagination
    paginator = Paginator(employees, 6)  # Show 10 employees per page
    page_number = request.GET.get('page')
    employees_page = paginator.get_page(page_number)

    context = {
        'employees': employees_page
    }
    return render(request, 'employee_list.html', context)


def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)  # Handle file uploads too
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, 'Employee added successfully!')
    else:
        form = EmployeeForm()
    
    return render(request, 'add_employee.html', {'form': form})

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Employee

def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    messages.success(request, "Employee has been deleted successfully.")
    return redirect('employee_list')  # Assuming 'employee_list' is your employee list page's URL name.



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