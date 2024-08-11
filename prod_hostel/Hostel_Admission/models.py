from django.db import models

# Create your models here.
from django.db import models

class HostelData1(models.Model):
    id = models.AutoField(primary_key=True)
    fno = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    DOB = models.DateField()
    cast = models.CharField(max_length=10)
    nationality = models.CharField(max_length=10)
    BGroup = models.CharField(max_length=4)
    phone1 = models.IntegerField()
    Address1 = models.CharField(max_length=50)
    Email = models.EmailField(max_length=30)

    Branch = models.CharField(max_length=40)
    mark1 = models.FloatField(default=0)
    outoff1 = models.FloatField(default=0)
    mark2 = models.FloatField(default=0)
    outoff2 = models.FloatField(default=0)
    percentage = models.FloatField()

    Father_name = models.CharField(max_length=100)
    phone2 = models.IntegerField()
    Address2 = models.CharField(max_length=50)

    occupation = models.CharField(max_length=50)
    # shift = models.CharField(max_length=8)
    Enroll = models.CharField(max_length=15)
    Year = models.CharField(max_length=7,default="First")
    SPhoto = models.FileField(upload_to='3signatures/student/',default='file.jpg')
    student_signature = models.FileField(upload_to='signatures/student/',default='file.jpg')
    father_signature = models.FileField(upload_to='signatures/father/',default='file.jpg')
    marksheet1 = models.FileField(upload_to='marksheet/', default='file.pdf')
    Domacile = models.FileField(upload_to='Domacile/', default='file.pdf')
    Allotment = models.FileField(upload_to='Allotment/', default='file.pdf')
    Addmission = models.FileField(upload_to='Addmission/', default='file.pdf')
    Registration  = models.FileField(upload_to='Registration/', default='file.pdf')
    ncl = models.FileField(upload_to='ncl/', default='NA')
    castecert = models.FileField(upload_to='3castecert/',default='NA')
    remark = models.CharField(max_length=200, default='NA')
    status = models.CharField(max_length=200,default='not_verified')
    payment_ss = models.FileField(upload_to='payment/', default='NA')
    trans_id = models.CharField(max_length=255,default=0)
    # a = models.IntegerField(default=0)

class HostelData2(models.Model):
    id = models.AutoField(primary_key=True)
    fno = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    DOB = models.DateField()
    cast = models.CharField(max_length=10)
    nationality = models.CharField(max_length=10)
    BGroup = models.CharField(max_length=4)
    phone1 = models.IntegerField()
    Address1 = models.CharField(max_length=50)
    Email = models.EmailField(max_length=30)
    Year = models.CharField(max_length=7,default="Second")

    Branch = models.CharField(max_length=40)
    Backlog = models.CharField(max_length=3,default='YES')
    Nu_Backlog = models.IntegerField(default=0)
    mark1 = models.FloatField(default=0)
    outoff1 = models.FloatField(default=0)
    mark2 = models.FloatField(default=0)
    outoff2 = models.FloatField(default=0)
    percentage = models.FloatField()

    Father_name = models.CharField(max_length=100)
    phone2 = models.IntegerField()
    Address2 = models.CharField(max_length=50)

    occupation = models.CharField(max_length=50)
    # shift = models.CharField(max_length=8)
    Enroll = models.CharField(max_length=15)
  
    SPhoto = models.FileField(upload_to='3signatures/student/',default='file.jpg')
    student_signature = models.FileField(upload_to='2signatures/student/',default='file.jpg')
    father_signature = models.FileField(upload_to='2signatures/father/',default='file.jpg')
    marksheet1 = models.FileField(upload_to='2marksheet1/', default='file.pdf')
    marksheet2 = models.FileField(upload_to='2marksheet2/', default='file.pdf')
    Domacile = models.FileField(upload_to='2Domacile/', default='file.pdf')
    Allotment = models.FileField(upload_to='2Allotment/', default='file.pdf')
    Addmission = models.FileField(upload_to='2Addmission/', default='file.pdf')
    Registration  = models.FileField(upload_to='2Registration/', default='file.pdf')
    ncl = models.FileField(upload_to='2ncl/', default='NA')
    status = models.CharField(max_length=200,default='not_verified')
    castecert = models.FileField(upload_to='3castecert/',default='NA')
    remark = models.CharField(max_length=200, default='NA')
    payment_ss = models.FileField(upload_to='payment/', default='NA')
    trans_id = models.CharField(max_length=255,default=0)

class HostelData3(models.Model):
    id = models.AutoField(primary_key=True)
    fno = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    DOB = models.DateField() 
    cast = models.CharField(max_length=50)
    nationality = models.CharField(max_length=10)
    BGroup = models.CharField(max_length=4)
    phone1 = models.IntegerField()
    Address1 = models.CharField(max_length=50)
    Email = models.EmailField(max_length=50)    

    Branch = models.CharField(max_length=40)
    Backlog = models.CharField(max_length=3,default='YES')
    Nu_Backlog = models.IntegerField(default=0)
    mark1 = models.FloatField(default=0)
    outoff1 = models.FloatField(default=0)
    mark2 = models.FloatField(default=0)
    outoff2 = models.FloatField(default=0)
    percentage = models.FloatField()
    Year = models.CharField(max_length=7,default="Third")


    Father_name = models.CharField(max_length=100)
    phone2 = models.IntegerField()
    Address2 = models.CharField(max_length=50)
    
    occupation = models.CharField(max_length=50)
    # shift = models.CharField(max_length=8)
    Enroll = models.CharField(max_length=15)

    SPhoto = models.FileField(upload_to='3signatures/student/',default='NA')
    student_signature = models.FileField(upload_to='3signatures/student/',default='NA')
    father_signature = models.FileField(upload_to='3signatures/father/',default='NA')
    marksheet1 = models.FileField(upload_to='3marksheet1/', default='NA')
    marksheet2 = models.FileField(upload_to='3marksheet2/', default='NA')
    Domacile = models.FileField(upload_to='3Domacile/', default='NA')
    Allotment = models.FileField(upload_to='3Allotment/', default='NA')
    Addmission = models.FileField(upload_to='3Addmission/', default='NA')
    ncl = models.FileField(upload_to='3ncl/', default='NA')
    castecert = models.FileField(upload_to='3castecert/',default='NA')
    Registration  = models.FileField(upload_to='3Registration/', default='NA')
    status = models.CharField(max_length=200,default='not_verified')
    remark = models.CharField(max_length=200, default='NA')
    payment_ss = models.FileField(upload_to='payment/', default='NA')
    trans_id = models.CharField(max_length=255,default=0)



class Lists(models.Model):
    
    k = models.IntegerField(default=101010)
    p3 = models.FileField(upload_to='lists/', default='file.pdf')
    f3 = models.FileField(upload_to='lists/', default='file.pdf')
    p2 = models.FileField(upload_to='lists/', default='file.pdf')
    f2 = models.FileField(upload_to='lists/', default='file.pdf')
    p1 = models.FileField(upload_to='lists/', default='file.pdf')
    f1 = models.FileField(upload_to='lists/', default='file.pdf')



class Year(models.Model):
    id = models.AutoField(primary_key=True)
    start = models.IntegerField()
    end = models.IntegerField()
    # def __str__(self):
    #     return self.name


class Students_login(models.Model):
    id = models.AutoField(primary_key=True)
    enrollment_no = models.CharField(max_length=255)
    passwd = models.CharField(max_length=255)




class Admin_login(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    passwd = models.CharField(max_length=255)



class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    categories = models.CharField(max_length=255)