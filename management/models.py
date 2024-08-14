from django.db import models

# Create your models here.
#makemigrations-create changes and store in a file
#migrate-apply the pending changes created by makemigrations
class Professor_info(models.Model):
    name=models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    phone_number=models.CharField(max_length=12)
    address=models.CharField(max_length=200)
    aadhar_number=models.CharField(max_length=12)
    professor_id=models.CharField(max_length=100,primary_key=True)
    password=models.CharField(max_length=255,default='default_password')

 
    def __str__(self):
        return self.name
    

class Student_info(models.Model):
    name=models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    phone_number=models.CharField(max_length=12)
    address=models.CharField(max_length=200)
    aadhar_number=models.CharField(max_length=12)
    year=models.CharField(max_length=2)
    student_id=models.CharField(max_length=100,primary_key=True)
    password=models.CharField(max_length=255,default='default_password')


    def __str__(self):
        return self.name
    

class professor_class_mapp(models.Model):
    professor =  models.ForeignKey(Professor_info, null=True, on_delete=models.CASCADE)
    year_of_stud=models.CharField(max_length=2)
    
    def __str__(self):
        return f"{self.year_of_stud} taught by {self.professor.name}"


class professor_sub_mapp(models.Model):
    professor =  models.ForeignKey(Professor_info, null=True, on_delete=models.CASCADE)
    subject=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subject} taught by {self.professor.name}"
    

class StudentMarks(models.Model):
    student=models.ForeignKey(Student_info,null=True,on_delete=models.CASCADE)
    dsa=models.CharField(max_length=3)
    os=models.CharField(max_length=3)

    def _str_(self):
        return  f"marks {self.dsa} and {self.os} of {self.student.name}"
    
class StudentAttendance(models.Model):
    student=models.ForeignKey(Student_info,null=True,on_delete=models.CASCADE)
    attendance_dsa=models.CharField(max_length=3,blank=True,null=True)
    attendance_os=models.CharField(max_length=3,blank=True,null=True)

    def _str_(self):
        return  f"attendance in {self.attendance_dsa} and {self.attendance_os} of {self.student.name}"


class contactus(models.Model):
    name=models.CharField(max_length=120)
    email=models.CharField(max_length=250)
    subject=models.CharField(max_length=250)
    message=models.CharField(max_length=500)

    def __str__(self) ->str:
        return self.name