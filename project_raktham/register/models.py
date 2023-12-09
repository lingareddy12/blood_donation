from django.db import models

class user_registration(models.Model):
    username=models.CharField(max_length=24)
    email=models.EmailField()
    password=models.CharField(max_length=256)
    otp=models.IntegerField( null=True, blank=True) 
    isVerified = models.BooleanField(default=False)


class acceptor(models.Model):
    name = models.CharField(max_length=20)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10) 
    mobile= models.CharField(max_length=13)
    email=models.EmailField()
    hospital_name = models.CharField(max_length=255)
    hospital_address = models.CharField(max_length=255)
    emergency = models.CharField(max_length=255, null=True, blank=True)
    blood_group = models.CharField(max_length=16)
    blood_type = models.CharField(max_length=27)
    units=models.PositiveIntegerField(default=0)
    required_by = models.DateField() 
    agree=models.BooleanField()

    def __str__(self):
        return f"{self.name}'s Blood Donation Request"
    
class donor(models.Model):
    name = models.CharField(max_length=20)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10) 
    mobile= models.CharField(max_length=13)
    email=models.EmailField()
    address= models.CharField(max_length=255)
    blood_group = models.CharField(max_length=16)
    health_status=models.CharField(max_length=20)
    last_donated = models.DateField() 
    agree=models.BooleanField()


