from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import HostelData1
from .models import HostelData2
from .models import HostelData3
from .models import Lists
from .models import Year
from .models import Students_login
from .models import Admin_login
from .models import Categories
@admin.register(HostelData1)
class HostelDataAdmin(admin.ModelAdmin):
    list_display = ('id','fno','Enroll','name' ,  'Email' ,'phone1' )


@admin.register(HostelData2)
class HostelDataAdmin(admin.ModelAdmin):
    list_display = ('id','fno','Enroll','percentage','mark1','outoff1','mark2','outoff2','status','name' ,  'Email' ,'phone1' )


@admin.register(HostelData3)
class HostelDataAdmin(admin.ModelAdmin):
    list_display = ('id','fno','Enroll','name' , 'Email' ,'phone1' )


@admin.register(Lists)
class HostelDataAdmin(admin.ModelAdmin):
    list_display = ("k",)


class Yer(admin.ModelAdmin):
     list_display = ("id","start","end",)

admin.site.register(Year,Yer) 

class student_login_list(admin.ModelAdmin):
    list_display=("id","enrollment_no","passwd")

admin.site.register(Students_login,student_login_list)

class admin_login_list(admin.ModelAdmin):
    list_display=("id","username","passwd")

admin.site.register(Admin_login,admin_login_list)


class categories(admin.ModelAdmin):
    list_display=("id","categories")

admin.site.register(Categories,categories)
    # street1 = models.CharField(max_length=50)
    # city1 = models.CharField(max_length=50)
    # state1 = models.CharField(max_length=50)
    # pincode1 = models.CharField(max_length=50)
    # street2 = models.CharField(max_length=50)
    # city2 = models.CharField(max_length=50)
    # state2 = models.CharField(max_length=50)
    # pincode2 = models.CharField(max_length=50)