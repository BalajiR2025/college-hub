from django.db import models

class Subject(models.Model):
    DEPT = [('CSE','CSE'),('ECE','ECE'),
            ('MECH','MECH'),('CIVIL','CIVIL')]
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=10, choices=DEPT)
    semester = models.IntegerField()
    def __str__(self): return f"{self.department} - {self.name}"
