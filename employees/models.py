from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    mobile = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='employee_photos/',blank=True,null=True) 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
