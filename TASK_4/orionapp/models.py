from django.db import models

# Create your models here.


class EmployeeDetails(models.Model):
    emp_key = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    company = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    updated_time = models.DateField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'employee_details'

class ServerDetails(models.Model):
    server_key = models.AutoField(primary_key=True)
    server_name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    server_url = models.URLField()
    app = models.CharField(max_length=255)
    updated_time = models.DateField()

    def __str__(self):
        return self.server_name
    
    class Meta:
        db_table='server_details'

class AccessDetails(models.Model):
    access_key = models.AutoField(primary_key=True)  
    user_name = models.CharField(max_length=500,unique=True)
    app = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    email = models.EmailField()
    status = models.CharField(max_length=50)
    server_name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"{self.user_name} - {self.app}"
    class Meta:
        db_table='access_details'
    
