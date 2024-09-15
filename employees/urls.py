from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('delete-employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('edit-employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),

]
