from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add-employee/', views.add_employee, name='add_employee'),
    # path('edit-employee/<int:id>/', views.edit_employee, name='edit_employee'),  # For editing employee details
    # path('employees/', views.employee_list, name='employee_list'),  # A page to list employees
]
