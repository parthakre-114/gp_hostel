from django.shortcuts import render
from django.http import HttpResponse
from .models import HostelData3
from .models import HostelData2
from .models import HostelData1
from .models import Lists
from .models import Year
from .models import Students_login
import datetime 
import re
from . import form
from django.conf import settings
from django.shortcuts import get_object_or_404
import os
from email.message import EmailMessage
import ssl
import smtplib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth import authenticate, login
import subprocess
from django.core.files.storage import FileSystemStorage
from subprocess import run, PIPE
import json
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import form

file_path = os.path.join(settings.BASE_DIR, 'Hostel_Admission\\templates\\ext_file\\close.txt')
file_path2 = os.path.join(settings.BASE_DIR, 'Hostel_Admission\\templates\\ext_file\\impdates.txt')
file_path3 = os.path.join(settings.BASE_DIR, 'Hostel_Admission\\templates\\ext_file\\close2.txt')
file_path4 = os.path.join(settings.BASE_DIR, 'Hostel_Admission\\templates\\ext_file\\close1.txt')
file_path5 = os.path.join(settings.BASE_DIR, 'Hostel_Admission\\templates\\ext_file\\list.txt')

def get_obj(fno):
    tables = [HostelData3, HostelData2, HostelData1]
    
    for table in tables:
        row = get_object_or_404(table,fno=fno)
        if row:
            return row
    return 0  
def get_object_or_none(model_class, **kwargs):
    try:
        return model_class.objects.get(**kwargs)
    except model_class.DoesNotExist:
        return None
    
def change_delete_cascade(enroll,new):
    # List of tables to check
    tables = [HostelData3, HostelData2, HostelData1]
    
    for table in tables:
        row = table.objects.filter(Enroll=enroll).first()
        if row:
            row.Enroll = new
            row.save()
            return 
    return       
    
def pass_edit(req):
    if req.method == "POST":
       old = req.POST['oldenroll'] 
       en = req.POST['enroll']
       passwd = req.POST['passwd']
       
       new = get_object_or_none(Students_login,enrollment_no=en)
       row = get_object_or_none(Students_login,enrollment_no=old)
       if new != None:
           messages.error(req, 'Invalid Enrollment No')
           return redirect('admin_log')
       if row != None:
            row.Enroll = new
            row.passwd = passwd
            change_delete_cascade(old,en)
            row.save()
            messages.error(req, ' Enrollment No Changed')
       else:
            messages.error(req, 'Invalid Enrollment No')
       return redirect('admin_log')



def logout(request):
    request.session['username'] = None
    request.session['password'] = None
    return render(request , 'Home/index.html')

def home(request):
    #home page
    print("hello")
    return render(request , 'Home/index.html' )

def admin_log(request):
    #admin login page
    msg = ''
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if(username == 'gp' and password == 'gp'):
            msg = "Successfull"
            request.session['username'] = username
            request.session['password'] = password
            return render(request , 'Admin_OP/index.html')
        else:
            msg="Invalid Username or Password!"

    username = request.session.get('username')
    password = request.session.get('password')
    if username and password:
        return render(request , 'Admin_OP/index.html')
    return render(request , 'Admin_OP/login.html' ,{'msg':msg})



def firstyrdes(request):
    #first year home page with links
    enroll = request.session.get('enroll')
    exists = HostelData1.objects.filter(Enroll=enroll).exists()
    
    if exists:
        data = HostelData1.objects.get(Enroll=enroll)
        request.session['fno'] = data.fno
        return render(request , 'Home/firstyeardes.html',{'exists':'yes'} )
    else:
        sec = HostelData2.objects.filter(Enroll=enroll).exists()
        third = HostelData3.objects.filter(Enroll=enroll).exists()
        if sec or third:
            messages.error(request,"Form exists for Another Year ")
            return redirect(logged_home)
        return render(request , 'Home/firstyeardes.html' )


def secondyrdes(request):
     #second year home page with links
    enroll = request.session.get('enroll')
    exists = HostelData2.objects.filter(Enroll=enroll).exists()
    if exists:
        data = HostelData2.objects.get(Enroll=enroll)
        request.session['fno'] = data.fno
        return render(request , 'Home/secondyeardes.html',{'exists':'yes'} )
    else:
        sec = HostelData1.objects.filter(Enroll=enroll).exists()
        third = HostelData3.objects.filter(Enroll=enroll).exists()
        if sec or third:
            messages.error(request,"Form exists for Another Year ")
            return redirect(logged_home)
        return render(request , 'Home/secondyeardes.html' )
    

def thirdyrdes(request):
     #third year home page with links
    enroll = request.session.get('enroll')
    exists = HostelData3.objects.filter(Enroll=enroll).exists()
    if exists:
        data = HostelData3.objects.get(Enroll=enroll)

        request.session['fno'] = data.fno
        return render(request , 'Home/thirdyeardes.html',{'exists':'yes'} )
    else:
        sec = HostelData1.objects.filter(Enroll=enroll).exists()
        third = HostelData2.objects.filter(Enroll=enroll).exists()
        if sec or third:
            messages.error(request,"Form exists for Another Year ")
            return redirect(logged_home)
        return render(request , 'Home/thirdyeardes.html' )

def logged_home(req):
    return render(req,'Home/index2.html')

## Help page  
def HelpAdmin(request):    
    ## Help page  admin

    return render(request , 'Admin_OP/reports/help.html',{'da':''} )

def HelpStudent(request):
    ## Help page student

    return render(request , 'Home/help.html' )

#student login
def userlogin(request):
    if request.method == "POST":
         enroll = request.POST.get('enrollment_no')
         passwd = request.POST.get('password')
         exist = Students_login.objects.filter(enrollment_no=enroll,passwd=passwd).exists()
         if exist:
             request.session['enroll'] = enroll
             fno = get_data_from_enroll(enroll)
             if fno:
                request.session['fno'] = fno.fno
             else:
                 request.session['fno'] = fno
             # request.session['fno'] = enroll
             return render(request,'Home/index2.html')
         else:
             
             messages.error(request,"Invalid Credentials")
             return redirect('userlogin')
    else:
        return render(request,'Home/userlogin.html')     

#student register

def userregister(request):
    if request.method == 'POST':
        Enroll = request.POST.get('enrollment_no')
        passwd = request.POST.get('password')
        passwd2 = request.POST.get('password2')
        
        # a = check_name(request,Enroll)
        if Enroll[:3] == "DEN" and Enroll[3:].isdigit() or Enroll.isdigit():
            print("in regis ")
            
        else:
            messages.error(request,"Invalid Enrollment/DEN Number")
            return redirect('userregister')
        
        if not Enroll or not passwd or not passwd2:
            messages.error(request,"All Fields are required to fill!")
            return render(request,"Home/userregister.html")
        
        if passwd!=passwd2:
            messages.error(request,"Password should be same!")
            return render(request,"Home/userregister.html")
        
        if len(passwd)<8:
            messages.error(request,"Password should be of 8 digits!")
            return render(request,"Home/userregister.html")
        
        if Students_login.objects.filter(enrollment_no=Enroll).exists():
            messages.error(request,"Username already exists!")
            return render(request,"Home/userregister.html")
        
        # if Students_login.objects.filter(passwd=passwd).exists():
        #     messages.error(request,"Password already exists!")
        #     return render(request,"Home/userregister.html")
        
        stu=Students_login(enrollment_no=Enroll,passwd=passwd)
        stu.save()

        return redirect("../userlogin")
    return render(request,"Home/userregister.html")



def appl_report(req,year,type):
    if year == 'first':
        rep = HostelData1.objects.filter(status=type)
        return render(req,'Admin_OP/reports/appl_report.html',{'data':rep,'name':type,'Year':'First'})
    elif year == 'second':
        rep = HostelData2.objects.filter(status=type)
        return render(req,'Admin_OP/reports/appl_report.html',{'data':rep,'name':type,'Year':'Second'})
    elif year== 'third':
        rep = HostelData3.objects.filter(status=type)
        return render(req,'Admin_OP/reports/appl_report.html',{'data':rep,'name':type,'Year':'Third'})




## Admin Log
def admin_log(request):
    msg = ''
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if(username == 'gp' and password == 'gp'):
            msg = "Successfull"
            request.session['username'] = username
            request.session['password'] = password
            return render(request , 'Admin_OP/index.html')
        else:
            msg="Invalid Username or Password!"

    username = request.session.get('username')
    password = request.session.get('password')
    if username and password:
        return render(request , 'Admin_OP/index.html')
    return render(request , 'Admin_OP/login.html' ,{'msg':msg})


def check_name(request,name):
    if name[:3] == "DEN" or name.isdigit():
        print("in regis ")
        return None
    else:
        return render(request,'Home/index.html',{'msg':"Invalid Enrollment/DEN Number"})

#first year desktop + form submission

def First_year(request):
    with open(file_path3 , 'r') as file:
        current_value = file.read()
        print(current_value,type(current_value))
    if current_value == 'ON':
        if request.method == "POST":
            name = request.POST['name']
            enroll = request.session.get('enroll')
            Bdate = request.POST['DOB']
            cast = request.POST['cast']
            nationality = request.POST['nation']
            Bgroup = request.POST['Bgroup']
            number = request.POST['Number']
            address = request.POST['add']
            email = request.POST['email']
            branch = request.POST['Branch']
            # Shift = request.POST['Shift']
            obtain1 = float(request.POST['Obtained1']) 
            total1 = float(request.POST['Total1'])     

            if enroll[:3] == "DEN" or enroll.isdigit():
               print("in regis ")
            #    return None
            else:
               return render(request,'Home/userregister.html',{'msg':"Invalid Enrollment/DEN Number"})
            # check_name(request,enroll) 
            
            
            if total1 <= 0 or obtain1>total1 :
                messages.error(request,"Invalid Marks")
                redirect('First_year')
                
            
            obtain = obtain1
            total = total1
            per = (obtain / total) * 100

            fname = request.POST['fname']
            fphone = request.POST['fPhone']
            faddress = request.POST['fAddress']
            Occupation = request.POST['occupation']
            
            P_photo = request.FILES.get('photo')
            Signature = request.FILES.get('Signature')
            fSignature = request.FILES.get('fSignature')
            marksheet1 = request.FILES.get('Marksheet2')
            allotment = request.FILES.get('Allotment')
            domacile = request.FILES.get('Domacile')
            addmission = request.FILES.get('Addmission')
            cast_cert = request.FILES.get('cast_cert')
            ncl = request.FILES.get('ncl')
            
            registration = request.FILES.get('Registration')
            trans_id = request.POST.get('trans_id')
            payment= request.FILES.get('payment_ss')
           
            try:
                Bdate = datetime.datetime.strptime(Bdate, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request,"Invalid birthdate format.")
                redirect('First_year')

            if not re.fullmatch("[7-9][0-9]{9}",number):
                messages.error(request,"Invalid phone number format.")
                redirect('First_year')
                

            if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
                messages.error(request,"Invalid email format.")
                redirect('First_year')
                

            if not re.fullmatch("[7-9][0-9]{9}",number):
                messages.error(request,"Invalid father's phone number format")
                redirect('First_year')
                
            
            if number == fphone:
                messages.error(request,"Invalid Student and father contact number.")
                redirect('First_year')

                
                
            
            data = HostelData1.objects.all()
            for i in data:
                if i.Email == email or i.phone1 == number or i.Enroll == enroll:
                    return render(request,'1year/index.html',{'msg':"Form already exists"})
                

            year = Year.objects.all().values()
            last_id = HostelData1.objects.latest('id').id

            h = HostelData1()
            h.fno = str(enroll)+str(year[0]['start'])+str('01')+str(last_id+1)
            h.name = name
            h.Enroll = enroll
            h.DOB = Bdate
            h.cast = cast
            h.nationality = nationality 
            h.BGroup = Bgroup
            h.phone1 = number
            h.Address1 = address
            h.Email = email
            h.Branch = branch
            # h.shift = Shift
            h.percentage = per
            h.mark1 = obtain1 
            h.outoff1 = total1
            # h.mark2 = obtain2
            # h.outoff2 = total2
            h.Father_name = fname
            h.phone2 = fphone
            h.Address2 = faddress
            h.occupation = Occupation
            h.trans_id = trans_id
            
            
            if payment:
                h.payment_ss = payment
            if P_photo:
                h.SPhoto = P_photo
            if Signature:
                h.student_signature = Signature
            if fSignature:
                h.father_signature = fSignature
            if marksheet1:
                h.marksheet1 = marksheet1
            if allotment:
                h.Allotment = allotment
            if domacile:
                h.Domacile = domacile
            if addmission:
                h.Addmission = addmission
            if registration:
                h.Registration = registration
            if cast_cert:
                h.castecert=cast_cert
            if ncl:    
                h.ncl=ncl        
            if trans_id_checker(h.trans_id) != 0:
                return render(request,'1year/index.html',{'msg':"Transaction ID exists"})
            
            
            request.session['fno'] = h.fno
            h.save()
            return render(request , 'receipt.html' , {'s':h})

        return render(request,'1year/index.html',{'msg':""})
    else:
        
        return render(request,'Home/firstyeardes.html', {'message':'First Year Form Disabled For Now, Wait for further updates '})
        
# second year desktop + form submission

def Second_year(request):
    with open(file_path4 , 'r') as file:
        current_value = file.read()
        print(current_value,type(current_value))
    if current_value == 'ON':
        if request.method == "POST":
            print("ins econd ")
            name = request.POST['name']
            enroll = request.session.get('enroll')
            Bdate = request.POST['DOB']
            cast = request.POST['cast']
            nationality = request.POST['nation']
            Bgroup = request.POST['Bgroup']
            number = request.POST['Number']
            address = request.POST['add']
            email = request.POST['email']
            branch = request.POST['Branch']
            # Shift = request.POST['Shift']
            backlog = request.POST['Backlog']
            # noBack = request.POST['noBack']
            obtain1 = float(request.POST['Obtained1']) 
            total1 = float(request.POST['Total1'])      
            obtain2 = float(request.POST['Obtained2']) 
            total2 = float(request.POST['Total2'])      

            if backlog == 'YES':
                            noBack = request.POST['noBack']

            if total1 <= 0 or total2 <= 0 or obtain1>total1 or obtain2>total2:              
                messages.error(request,"Invalid Marks")
                redirect('Second_year')
            

            # if total <= 0:
            #     messages.error(request,"Total marks should be greater than 0")
            #     redirect('Second_year')
                
            sem1 = (obtain1/total1)*100
                        
            if obtain2 == 0 and total2 == 0: 
               sem2 = 0
            else: 
                sem2 = (obtain2/total2)*100
                
            per = (sem1+sem2)/2 
            
            # if enroll:
            
            fname = request.POST['fname']
            fphone = request.POST['fPhone']
            faddress = request.POST['fAddress']
            Occupation = request.POST['occupation']

            P_photo = request.FILES.get('photo')
            Signature = request.FILES.get('Signature')
            fSignature = request.FILES.get('fSignature')
            Marksheet1 = request.FILES.get('Marksheet1')
            marksheet2 = request.FILES.get('Marksheet2')
            allotment = request.FILES.get('Allotment')
            domacile = request.FILES.get('Domacile')
            addmission = request.FILES.get('Addmission')
            registration = request.FILES.get('Registration')
            trans_id = request.POST.get('trans_id')
            payment= request.FILES.get('payment_ss')
            cast_cert = request.FILES.get('cast_cert')
            ncl = request.FILES.get('ncl')
            try:
                Bdate = datetime.datetime.strptime(Bdate, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request,"Invalid birthdate format")
                redirect('Second_year')
            

            if not re.fullmatch("[7-9][0-9]{9}",number):
                messages.error(request,"Invalid phone number format")
                redirect('Second_year')

            if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
                messages.error(request,"Invalid Email format")
                redirect('Second_year')
                return HttpResponse("Invalid email format.")

            if not re.fullmatch("[7-9][0-9]{9}",number):
                messages.error(request,"Invalid Father's Phone format")
                redirect('Second_year')
            if number == fphone:
                messages.error(request,"Invalid student and father contact number")
                redirect('Second_year')
            data = HostelData2.objects.all()
            
            for i in data:
                if i.Email == email or i.phone1 == number or i.Enroll == enroll:
                     messages.error(request,"This student already exists!")
                     redirect('Second_year')
            
            year = Year.objects.all().values()
                # print(st[0]['start'])
            last_id = HostelData2.objects.latest('id').id
            
            exist = HostelData2.objects.filter(Enroll=enroll).exists()
            if exist:
                messages.error(request,"This student already exists!")
                return render(request,'Home/secondyeardes.html')
            
            
            
            h = HostelData2()
            h.fno = str(enroll)+str(year[0]['start'])+str('02')+str(last_id+1)
            h.name = name
            h.Enroll = enroll
            h.DOB = Bdate
            h.cast = cast
            h.nationality = nationality 
            h.BGroup = Bgroup
            h.phone1 = number
            h.Address1 = address
            h.Email = email
            h.Branch = branch
            h.mark1 = obtain1 
            h.outoff1 = total1
            h.mark2 = obtain2
            h.outoff2 = total2
            # h.shift = Shift
            h.Backlog = backlog
            if backlog == 'YES':
                            # noBack = request.POST['noBack']
                            h.Nu_Backlog = noBack
            h.percentage = per

            h.Father_name = fname
            h.phone2 = fphone
            h.Address2 = faddress
            h.occupation = Occupation
            h.trans_id = trans_id
            
            if payment:
                h.payment_ss = payment
            if P_photo:
                h.SPhoto = P_photo
            if Signature:
                h.student_signature = Signature
            if fSignature:
                h.father_signature = fSignature
            if Marksheet1:
                h.marksheet1 = Marksheet1
            if marksheet2:
                h.marksheet2 = marksheet2
            if allotment:
                h.Allotment = allotment
            if domacile:
                h.Domacile = domacile
            if addmission:
                h.Addmission = addmission
            if registration:
                h.Registration = registration
            if cast_cert:
                h.castecert=cast_cert
            if ncl:    
                h.ncl=ncl        
            
            ls = list(HostelData2.objects.values_list('Enroll', flat=True))
            if str(h.Enroll) in ls:
                messages.error(request,"Student already exists")
                redirect('Second_year')
            if trans_id_checker(h.trans_id) != 0:
                messages.error(request,"Transaction ID exists")
                redirect('Second_year')
            h.save()  
            request.session['fno'] = h.fno
            return render(request , 'receipt.html' , {'s':h})
        return render(request , '2year/index.html')
    else:
               return render(request,'Home/secondyeardes.html', {'message':'Second Year Form Disabled For Now, Wait for further updates '})



#Third year desktop + form submission



def Third_year(request):
        with open(file_path , 'r') as file:
            current_value = file.read()
        if current_value == 'ON':
            fno = request.session.get('fno')
            enroll = request.session.get('enroll')
            print(fno)
            if fno:
                # data = HostelData3.objects.get(fno=fno)
                data =  get_data_from_fno(fno)
                print(data)
                if data:
                        return HttpResponse("This student already exists!")            
            if request.method == 'POST':    
                name = request.POST['name']
                # print(request.POST['enroll'])
                enroll = request.session.get('enroll')
                Bdate = request.POST['DOB']
                cast = request.POST['cast']
                nationality = request.POST['nation']
                Bgroup = request.POST['Bgroup']
                number = request.POST['Number']
                address = request.POST['add']
                email = request.POST['email']
                branch = request.POST['Branch']
                # Shift = request.POST['Shift']
                backlog = request.POST['Backlog']
                if backlog == 'YES':
                            noBack = request.POST['noBack']
                obtain1 = float(request.POST['Obtained1']) if request.POST['Obtained1'].strip() else 0
                total1 = float(request.POST['Total1']) if request.POST['Total1'].strip() else 0
                obtain2 = float(request.POST['Obtained2']) if request.POST['Obtained2'].strip() else 0
                total2 = float(request.POST['Total2']) if request.POST['Total2'].strip() else 0   

                if total1 <= 0 or total2 <= 0 or obtain1>total1 or obtain2>total2:
                  messages.error(request,"Invalid Marks")
                  redirect('Third_year')
                
                obtain = obtain1 + obtain2
                total = total1 + total2

                sem1 = (obtain1/total)*100
                if obtain2 == 0 and obtain2 == 0: 
                   sem2 = 0
                   print(sem2)
                else: 
                   sem2 = (obtain2/total2)*100
                   print(sem2)
                per = (sem1+sem2)/2 
                 
                        
                

                fname = request.POST['fname']
                fphone = request.POST['fPhone'] 
                faddress = request.POST['fAddress']
                Occupation = request.POST['occupation']

                P_photo = request.FILES.get('photo')
                Signature = request.FILES.get('Signature')
                fSignature = request.FILES.get('fSignature')
                Marksheet1 = request.FILES.get('Marksheet1')
                marksheet2 = request.FILES.get('Marksheet2')
                allotment = request.FILES.get('Allotment')
                domacile = request.FILES.get('Domacile')
                addmission = request.FILES.get('Addmission')
                registration = request.FILES.get('Registration')
                ncl = request.FILES.get('ncl')
                trans_id = request.POST.get('trans_id')
                payment= request.FILES.get('payment_ss')
                cast_cert = request.FILES.get('cast_cert')
                
                       
                try:
                    Bdate = datetime.datetime.strptime(Bdate, '%Y-%m-%d').date()
                except ValueError:
                    messages.error(request,"Invalid birthdate format")
                    redirect('Third_year')
            

                if not re.fullmatch("[7-9][0-9]{9}",number):
                    messages.error(request,"Invalid phone number format")
                    redirect('Third_year')

                if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
                    messages.error(request,"Invalid Email format")
                    redirect('Third_year')
                if not re.fullmatch("[7-9][0-9]{9}",number):
                    messages.error(request,"Invalid Father's Phone format")
                    redirect('Third_year')
                if number == fphone:
                    messages.error(request,"Invalid student and father contact number")
                    redirect('Third_year')       
                
                data = HostelData3.objects.filter(Enroll=enroll)
                for i in data:
                  if i.Email == email or i.phone1 == number or i.Enroll == enroll:
                     messages.error(request,"This student already exists!")
                     redirect('Third_year')
                         
                # data = HostelData3.objects.all()        
                h = HostelData3()
                year = Year.objects.all().values()
                # print(st[0]['start'])
                last_id = HostelData3.objects.latest('id').id
                h.name = name
                h.Enroll = enroll
                h.fno = str(enroll)+str(year[0]['start'])+str('03')+str(last_id+1)
                print(h.fno)
                h.DOB = Bdate
                h.cast = cast
                h.nationality = nationality 
                h.BGroup = Bgroup
                h.phone1 = number
                h.Address1 = address
                h.Email = email
                h.Branch = branch
                # h.shift = Shift
                h.percentage = per
                h.Backlog = backlog
                h.mark1 = obtain1 
                h.outoff1 = total1
                h.mark2 = obtain2
                h.outoff2 = total2
                
                if backlog == 'YES':
                            # noBack = request.POST['noBack']
                            h.Nu_Backlog = noBack
                h.Father_name = fname
                h.phone2 = fphone
                h.Address2 = faddress
                h.occupation = Occupation
                h.ncl = ncl
                h.trans_id = trans_id
                
                if cast_cert:
                   h.castecert=cast_cert
                if ncl:    
                   h.ncl=ncl 
                   
                if payment:
                   h.payment_ss = payment
                if P_photo:
                    h.SPhoto = P_photo
                if Signature:
                    h.student_signature = Signature
                if fSignature:
                    h.father_signature = fSignature
                if Marksheet1:
                    h.marksheet1 = Marksheet1
                if marksheet2:
                    h.marksheet2 = marksheet2
                if allotment:
                    h.Allotment = allotment
                if domacile:
                    h.Domacile = domacile
                if addmission:
                    h.Addmission = addmission
                if registration:
                    h.Registration = registration
                if ncl:
                    h.ncl = ncl
                if h.castecert:
                    h.castecert = cast_cert    
                # try:
                # enroll = str(2201456)
                ls = list(HostelData3.objects.values_list('Enroll', flat=True))
                if str(h.Enroll) in ls:
                    return HttpResponse('Student already registered')
                if trans_id_checker(h.trans_id) != 0:
                    return render(request,'1year/index.html',{'msg':"Transaction ID exists"})    
                h.save() 
                # except:
                #     return HttpResponse('Something went wrong')   
                request.session['fno'] = h.fno
                request.session['enroll'] = h.Enroll
                dataobj = HostelData3.objects.get(fno=h.fno)
                data = vars(dataobj)
                print(data)
                return render(request , 'receipt.html' , {'s':data})
            else:
                 return render(request , '3year/index.html' )  
            # return HttpResponse('Form Disabled For Now')
        else:
            return render(request,'Home/thirdyeardes.html', {'message':'Third Year Form Disabled For Now, Wait for further updates '})
    # ####################################################
def admin_appl_edit(request,fno):
    if request.method == "GET":
           fno = fno           
           data = get_data_from_fno(fno)        
        #    var = vars(data)
           if data:
               return render(request,'Admin_OP/admin_appl_edit.html',{'data':data})
           return render(request,'Admin_OP/index.html')
       
    if request.method == "POST":
                print("in postr")
                name = request.POST['name']
                enroll = request.POST['enroll']
            
                Bdate = request.POST['DOB']
                cast = request.POST['cast']
                nationality = request.POST['nation']
                Bgroup = request.POST['Bgroup']
                number = request.POST['Number']
                address = request.POST['add']
                email = request.POST['email']
                branch = request.POST['Branch']
                # Shift = request.POST['Shift']
                backlog = request.POST['Backlog']
                noBack = request.POST['noBack']
                obtain1 = float(request.POST['Obtained1']) if request.POST['Obtained1'].strip() else 0
                total1 = float(request.POST['Total1']) if request.POST['Total1'].strip() else 0
                obtain2 = float(request.POST['Obtained2']) if request.POST['Obtained2'].strip() else 0
                total2 = float(request.POST['Total2']) if request.POST['Total2'].strip() else 0
                print(total2)
                
                if total1 <= 0 or total2 <= 0 or obtain1>total1 or obtain2>total2:              
                        messages.error(request,"Invalid Marks")
                        redirect('appl_edit')
                sem1 = (obtain1/total1)*100
                print(sem1)
            
                if obtain2 == 0 and obtain2 == 0: 
                  sem2 = 0
                  print(sem2)
                else: 
                  sem2 = (obtain2/total2)*100
                  print(sem2)
                  
                per = (sem1+sem2)/2 

                fname = request.POST['fname']
                fphone = request.POST['fPhone'] 
                faddress = request.POST['fAddress']
                Occupation = request.POST['occupation']

                P_photo = request.FILES.get('photo')
                Signature = request.FILES.get('Signature')
                fSignature = request.FILES.get('fSignature')
                Marksheet1 = request.FILES.get('Marksheet1')
                marksheet2 = request.FILES.get('Marksheet2')
                allotment = request.FILES.get('Allotment')
                domacile = request.FILES.get('Domacile')
                addmission = request.FILES.get('Addmission')
                registration = request.FILES.get('Registration')
                ncl = request.FILES.get('ncl')

                try:
                    Bdate = datetime.datetime.strptime(Bdate, '%Y-%m-%d').date()
                except ValueError:
                    messages.error(request,"Invalid birthdate format")
                    redirect('receipt')                
               
                if not re.fullmatch("[7-9][0-9]{9}",number):
                    messages.error(request,"Invalid phone number format")
                    redirect('receipt')
    
                if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
                    messages.error(request,"Invalid Email format")
                    redirect('receipt')
                    return HttpResponse("Invalid email format.")
    
                if not re.fullmatch("[7-9][0-9]{9}",number):
                    messages.error(request,"Invalid Father's Phone format")
                    redirect('receipt')
                if number == fphone:
                   messages.error(request,"Invalid student and father contact number")
                   redirect('receipt')
                   
                h = get_data_from_enroll(enroll)
                
                year = Year.objects.all().values()
                # print(st[0]['start'])
                last_id = HostelData3.objects.latest('id').id
                h.name = name
                h.Enroll = enroll
                h.fno = fno
                print(h.fno)
                h.DOB = Bdate
                h.cast = cast
                h.nationality = nationality 
                h.BGroup = Bgroup
                h.phone1 = number
                h.Address1 = address
                h.Email = email
                h.Branch = branch
                h.mark1 = obtain1 
                h.outoff1 = total1
                h.mark2 = obtain2
                h.outoff2 = total2
                # h.shift = Shift
                h.percentage = per
                h.Backlog = backlog
                h.Nu_Backlog = noBack
                h.Father_name = fname
                h.phone2 = fphone
                h.Address2 = faddress
                h.occupation = Occupation
                h.ncl = ncl


                if P_photo:
                    h.SPhoto = P_photo
                if Signature:
                    h.student_signature = Signature
                if fSignature:
                    h.father_signature = fSignature
                if Marksheet1:
                    h.marksheet1 = Marksheet1
                if marksheet2:
                    h.marksheet2 = marksheet2
                if allotment:
                    h.Allotment = allotment
                if domacile:
                    h.Domacile = domacile
                if addmission:
                    h.Addmission = addmission
                if registration:
                    h.Registration = registration
                if ncl:
                    h.ncl = ncl
                # try:
                # ls = list(HostelData3.objects.values_list('Enroll', flat=True))
                h.status = "edited"
               
                h.save()
                return render(request , 'Admin_OP/admin_appl_edit.html')          



def appl_edit(request):
    if request.method == "GET":
           fno = request.session.get("fno")
        #    fno = 22130222403113
           enroll = request.session.get("enroll")
           
           data = get_data_from_fno(fno)
           if not data:
               enroll = request.session.get("enroll_no")
               data = get_data_from_fno(enroll)
               if not enroll:
                 return render(request,'Home/userlogin.html',{'msg':"Please Login"})#change it to login page
           
        #    var = vars(data)
           if data.status == 'accepted':
               return render(request,'Home/index2.html',{'msg':"Application Locked"})
           return render(request,'Home/appl_edit.html',{'data':data})
    if request.method == "POST":
                print("in postr")
                name = request.POST['name']
                enroll = request.session.get('enroll')
                Bdate = request.POST['DOB']
                cast = request.POST['cast']
                nationality = request.POST['nation']
                Bgroup = request.POST['Bgroup']
                number = request.POST['Number']
                address = request.POST['add']
                email = request.POST['email']
                branch = request.POST['Branch']
                # Shift = request.POST['Shift']
                backlog = request.POST['Backlog']
                noBack = request.POST['noBack']
                obtain1 = float(request.POST['Obtained1']) if request.POST['Obtained1'].strip() else 0
                total1 = float(request.POST['Total1']) if request.POST['Total1'].strip() else 0
                obtain2 = float(request.POST['Obtained2']) if request.POST['Obtained2'].strip() else 0
                total2 = float(request.POST['Total2']) if request.POST['Total2'].strip() else 0
                print(total2)
                
                if total1 <= 0 or total2 <= 0 or obtain1>total1 or obtain2>total2:              
                        messages.error(request,"Invalid Marks")
                        redirect('appl_edit')
                sem1 = (obtain1/total1)*100
                print(sem1)
            
                if obtain2 == 0 and obtain2 == 0: 
                  sem2 = 0
                  print(sem2)
                else: 
                  sem2 = (obtain2/total2)*100
                  print(sem2)
                  
                per = (sem1+sem2)/2 

                fname = request.POST['fname']
                fphone = request.POST['fPhone'] 
                faddress = request.POST['fAddress']
                Occupation = request.POST['occupation']

                P_photo = request.FILES.get('photo')
                Signature = request.FILES.get('Signature')
                fSignature = request.FILES.get('fSignature')
                Marksheet1 = request.FILES.get('Marksheet1')
                marksheet2 = request.FILES.get('Marksheet2')
                allotment = request.FILES.get('Allotment')
                domacile = request.FILES.get('Domacile')
                addmission = request.FILES.get('Addmission')
                registration = request.FILES.get('Registration')
                ncl = request.FILES.get('ncl')

                try:
                    Bdate = datetime.datetime.strptime(Bdate, '%Y-%m-%d').date()
                except ValueError:
                    messages.error(request,"Invalid birthdate format")
                    redirect('receipt')                
               
                if not re.fullmatch("[7-9][0-9]{9}",number):
                    messages.error(request,"Invalid phone number format")
                    redirect('receipt')
    
                if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
                    messages.error(request,"Invalid Email format")
                    redirect('receipt')
                    return HttpResponse("Invalid email format.")
    
                if not re.fullmatch("[7-9][0-9]{9}",number):
                    messages.error(request,"Invalid Father's Phone format")
                    redirect('receipt')
                if number == fphone:
                   messages.error(request,"Invalid student and father contact number")
                   redirect('receipt')
                   
                h = get_data_from_enroll(enroll)
                
                year = Year.objects.all().values()
                # print(st[0]['start'])
                last_id = HostelData3.objects.latest('id').id
                h.name = name
                h.Enroll = enroll
                h.fno = str(enroll)+str(year[0]['start'])+str('03')+str(last_id)
                print(h.fno)
                h.DOB = Bdate
                h.cast = cast
                h.nationality = nationality 
                h.BGroup = Bgroup
                h.phone1 = number
                h.Address1 = address
                h.Email = email
                h.Branch = branch
                h.mark1 = obtain1 
                h.outoff1 = total1
                h.mark2 = obtain2
                h.outoff2 = total2
                # h.shift = Shift
                h.percentage = per
                h.Backlog = backlog
                h.Nu_Backlog = noBack
                h.Father_name = fname
                h.phone2 = fphone
                h.Address2 = faddress
                h.occupation = Occupation
                h.ncl = ncl


                if P_photo:
                    h.SPhoto = P_photo
                if Signature:
                    h.student_signature = Signature
                if fSignature:
                    h.father_signature = fSignature
                if Marksheet1:
                    h.marksheet1 = Marksheet1
                if marksheet2:
                    h.marksheet2 = marksheet2
                if allotment:
                    h.Allotment = allotment
                if domacile:
                    h.Domacile = domacile
                if addmission:
                    h.Addmission = addmission
                if registration:
                    h.Registration = registration
                if ncl:
                    h.ncl = ncl
                # try:
                # ls = list(HostelData3.objects.values_list('Enroll', flat=True))
                h.status = "edited"
                # print(ls)
                
                # print("helllll")
                # if str(h.Enroll) in ls:
                #     return HttpResponse('Student already registered')
                h.save()
                # except:
                #     return HttpResponse('Something went wrong')   
                request.session['fno'] = h.fno
                request.session['enroll']=h.Enroll
                # dataobj = HostelData3.objects.get(fno=h.fno)
                dataobj = get_data_from_fno(h.fno)
                data = vars(dataobj)
                print(data)
                return render(request , 'receipt.html' , {'s':data})          



def close_Forms(request):
    if request.method=="POST":
        decide  = str(request.POST['student_access'])
        if decide == 'OFF':
            with open(file_path, 'w') as file:
                file.write('OFF')
        if decide == 'ON':
            with open(file_path, 'w') as file:
                file.write('ON')
    return render(request , 'Admin_OP/closeform.html')

def close_Forms1(request):
    if request.method=="POST":
        decide  = str(request.POST['student_access'])
        if decide == 'OFF':
            with open(file_path3, 'w') as file:
                file.write('OFF')
        if decide == 'ON':
            with open(file_path3, 'w') as file:
                file.write('ON')
    return render(request , 'Admin_OP/closeform1.html')

def close_Forms2(request):
    if request.method=="POST":
        decide  = str(request.POST['student_access'])
        if decide == 'OFF':
            with open(file_path4, 'w') as file:
                file.write('OFF')
        if decide == 'ON':
            with open(file_path4, 'w') as file:
                file.write('ON')
    return render(request , 'Admin_OP/closeform2.html')


def logout(request):
    request.session['username'] = None
    request.session['password'] = None
    return render(request , 'Admin_OP/login.html')

def Year3_report(request):
    data = HostelData3.objects.all().filter(status="accepted")
    if request.method == 'POST':
        tseets = int(request.POST['Tseats'])
        print(str(tseets) + "tseats")
        OPENseets = int(request.POST['OPEN'])
        OBCseets = int(request.POST['OBC'])
        SCseets = int(request.POST['SC'])
        STseets = int(request.POST['ST'])
        NTseets = int(request.POST['NT'])
        SBCseets = int(request.POST['SBC'])
        
        data_dict = {}
        for key, value in request.POST.items():
            try:
                data_dict[key] = int(value)
            except ValueError:
                data_dict[key] = value
        del data_dict['Tseats']       
        sumseats = sum(value for value in data_dict.values() if isinstance(value, int))
        # sumseats = OPENseets+OBCseets+SCseets+STseets+NTseets+SBCseets
        if tseets != sumseats:
            return HttpResponse("Invalid Seats")
        backlog_YES_students = data.filter(Backlog='YES')
        backlog_NO_students = data.filter(Backlog='NO')
        
        available_seats = {
            'OBC': OBCseets,
            'SC': SCseets,
            'ST': STseets,
            'NT': NTseets,
            'SBC':SBCseets
        }
        
        Backlog_NO_students = sorted(backlog_NO_students ,key=lambda x:(-x.percentage))
        Backlog_Yes_students = sorted(backlog_YES_students ,key=lambda x:( x.Nu_Backlog , -x.percentage))
        
        print(data_dict)       
        Allocated_students = []
        count = 1
        open_student_seat = {}
        csmerit={
            'OPEN':0,
            'OBC':0,
            'SC':0,
            'SBC':0,
            'NT':0,
            'ST':0
        }
        ls = ['OBC','SC','SBC','NT','ST']
        
        # for OPENs
        for i in range(OPENseets):
            # print(i)
            if backlog_NO_students.__len__() == i:
                break
            
            student = Backlog_NO_students[i]
            stud = vars(student) 
            stud['merit_no'] = ''               
            csmerit[student.cast] += 1
            # print(csmerit[student.cast])
            seat = student.cast+'-'+ str(csmerit[student.cast]) #merit no
            stud['merit_no'] = ''
            stud['quota'] = 'OPEN'
            Allocated_students.append(stud)
            data_dict['OPEN'] -= 1
            
            print(stud['name'])
            # tseets -= 1 
            open_student_seat[student.name] = seat
            count += 1
        
        student_seat = {}
        rac = []
        
        #for other categories
        for student in Backlog_NO_students:
            stud = vars(student)
            # print(Allocated_students)
            if stud in Allocated_students:
                # print("in pass")
                pass
            else:
                student_category = student.cast
                if data_dict.get(student_category,0) > 0:
                    # allotment code
                    csmerit[student.cast] += 1
                    seat = student.cast+'-'+''+str(csmerit[student.cast])
                    # student_seat[student.name] = seat
                    data_dict[student_category] -= 1
                    stud['merit_no'] = seat
                    stud['quota'] = student.cast
                    Allocated_students.append(stud)
                    # print (student.name +'  '+ seat)
                else:
                    # obc to sbc
                    if student_category == 'SBC' and data_dict.get('OBC',0) > 0 :
                      csmerit['OBC'] += 1
                      seat = student.cast+'-'+''+str(csmerit[student.cast])
                    #   student_seat[student.name] = seat
                      data_dict['OBC'] -= 1
                      stud['merit_no'] = seat
                      stud['quota'] = 'OBC'
                      Allocated_students.append(stud)
                      
                      print(stud['name'])
                      rac.append(stud)
                      
                      # sc to st
                    if student_category == 'ST' and data_dict.get('SC',0) > 0 :
                      csmerit['SC'] += 1
                      seat = student.cast+'-'+''+str(csmerit[student.cast])
                    #   student_seat[student.name] = seat
                      data_dict['SC'] -= 1
                      stud['merit_no'] = seat
                      stud['quota'] = 'SC'
                      Allocated_students.append(stud)
                     ##  st to sc
                    if student_category == 'SC' and data_dict.get('ST',0) > 0 :
                      csmerit['ST'] += 1
                      seat = student.cast+'-'+''+str(csmerit[student.cast])
                    #   student_seat[student.name] = seat
                      data_dict['ST'] -= 1
                      stud['merit_no'] = seat
                      stud['quota'] = 'ST'
                      Allocated_students.append(stud)
                      
                    print(stud['name'])
                    rac.append(stud)  
             #rac       
                # print(rac)
                for i in range(len(rac)):
                    #   print(i)
                      print(tseets)
                      fn_available_seats = tseets - len(Allocated_students) 
                      if fn_available_seats > 0:
                            
                            print("in rac")
                            rac[i]['merit_no'] = ''
                            rac[i]['quota'] = 'RAC'
                            if data_dict.get(rac[i]['cast'], 0) > 0:
                                csmerit[rac[i]['cast']] += 1
                            else:
                                data_dict['OPEN'] -= 1
                            Allocated_students.append(rac[i])
                            rac.pop(0)
                             
                                                  
                      else:
                            break  
                    #  print(type(Allocated_students))
        # print(rac)        
        Allocated = sorted(Allocated_students ,key=lambda x:(-x['percentage']))
        
        return render(request , 'Admin_OP/Provisional/third_year.html',{
            'BACKLOG_YES':Backlog_Yes_students , 
            'BACKLOG_NO':Backlog_NO_students ,
            'Allocated_students':Allocated,
            'student_seat':student_seat,
            'waiting':rac,
            'open_student_seat':open_student_seat
        })
    request.session['year'] = 'third'
    countnew = HostelData3.objects.filter(status='not_verified').count()
    countgriv = HostelData3.objects.filter(status='not_accepted').count()
    countedit = HostelData3.objects.filter(status='edited').count()
    countaccepted = HostelData3.objects.filter(status='accepted').count()
    
    return render(request , 'Admin_OP/reports/year3.html',{'data':data,'new':countnew,'griv':countgriv,'edit':countedit,'accept':countaccepted} )

def Year2_report(request):
    data = HostelData2.objects.filter(status="accepted")
    if request.method == 'POST':
        tseets = int(request.POST['Tseats'])
        print(str(tseets) + "tseats")
        OPENseets = int(request.POST['OPEN'])
        OBCseets = int(request.POST['OBC'])
        SCseets = int(request.POST['SC'])
        STseets = int(request.POST['ST'])
        NTseets = int(request.POST['NT'])
        SBCseets = int(request.POST['SBC'])
        
        data_dict = {}
        for key, value in request.POST.items():
            try:
                data_dict[key] = int(value)
            except ValueError:
                data_dict[key] = value
        del data_dict['Tseats']       
        sumseats = sum(value for value in data_dict.values() if isinstance(value, int))
        # sumseats = OPENseets+OBCseets+SCseets+STseets+NTseets+SBCseets
        if tseets != sumseats:
            return HttpResponse("Invalid Seats")
        backlog_YES_students = data.filter(Backlog='YES')
        backlog_NO_students = data.filter(Backlog='NO')
        
        available_seats = {
            'OBC': OBCseets,
            'SC': SCseets,
            'ST': STseets,
            # 'NT': NTseets,
            'SBC':SBCseets
        }
        
        Backlog_NO_students = sorted(backlog_NO_students ,key=lambda x:(-x.percentage))
        Backlog_Yes_students = sorted(backlog_YES_students ,key=lambda x:( x.Nu_Backlog , -x.percentage))
        
        print(data_dict)       
        Allocated_students = []
        count = 1
        open_student_seat = {}
        csmerit={
            'OPEN':0,
            'OBC':0,
            'SC':0,
            'SBC':0,
            'DT/NT/VJ':0,
            'ST':0
        }
        ls = ['OBC','SC','SBC','NT','ST']
        
        # for OPENs
        for i in range(OPENseets):
            # print(i)
            if backlog_NO_students.__len__() == i:
                break
            
            student = Backlog_NO_students[i]
            stud = vars(student) 
            stud['merit_no'] = ''               
            csmerit[student.cast] += 1
            # print(csmerit[student.cast])
            seat = student.cast+'-'+ str(csmerit[student.cast]) #merit no
            if student.cast != "OPEN":
                stud['merit_no'] = seat
            else:
                stud['merit_no'] = ''         
            stud['quota'] = 'OPEN'
            Allocated_students.append(stud)
            data_dict['OPEN'] -= 1
            
            print(stud['name'])
            # tseets -= 1 
            open_student_seat[student.name] = seat
            count += 1
        
        student_seat = {}
        rac = []
        
        #for other categories
        for student in Backlog_NO_students:
            stud = vars(student)
            # print(Allocated_students)
            if stud in Allocated_students:
                # print("in pass")
                pass
            else:
                student_category = student.cast
                if data_dict.get(student_category,0) > 0:
                    # allotment code
                    csmerit[student.cast] += 1
                    seat = student.cast+'-'+''+str(csmerit[student.cast])
                    # student_seat[student.name] = seat
                    data_dict[student_category] -= 1
                    stud['merit_no'] = seat
                    stud['quota'] = student.cast
                    Allocated_students.append(stud)
                    # print (student.name +'  '+ seat)
                else:
                    # obc to sbc
                    if student_category == 'SBC' and data_dict.get('OBC',0) > 0 :
                      csmerit['OBC'] += 1
                      seat = student.cast+'-'+''+str(csmerit[student.cast])
                    #   student_seat[student.name] = seat
                      data_dict['OBC'] -= 1
                      stud['merit_no'] = seat
                      stud['quota'] = 'OBC'
                      Allocated_students.append(stud)
                      
                    #   print(stud['name'])
                    #   rac.append(stud)
                      
                      # sc to st
                    if student_category == 'ST' and data_dict.get('SC',0) > 0 :
                      csmerit['SC'] += 1
                      seat = student.cast+'-'+''+str(csmerit[student.cast])
                    #   student_seat[student.name] = seat
                      data_dict['SC'] -= 1
                      stud['merit_no'] = seat
                      stud['quota'] = 'SC'
                      Allocated_students.append(stud)
                     ##  st to sc
                    if student_category == 'SC' and data_dict.get('ST',0) > 0 :
                      csmerit['ST'] += 1
                      seat = student.cast+'-'+''+str(csmerit[student.cast])
                    #   student_seat[student.name] = seat
                      data_dict['ST'] -= 1
                      stud['merit_no'] = seat
                      stud['quota'] = 'ST'
                      Allocated_students.append(stud)
                      
                    print(stud['name'])
                    rac.append(stud)  
             #rac       
        # print(rac)
        # print(Allocated_students)
        fn_available_seats = tseets - len(Allocated_students) 
        for i in range(fn_available_seats):
                    #   print(i)
                      
                      print(fn_available_seats)
                      print(len(rac))
                      if fn_available_seats > 0:
                            print(i)
                            print(rac)
                            # rac
                            rac[i]['merit_no'] = ''
                            rac[i]['quota'] = 'General Merit Against Vacancy'
                            if data_dict.get(rac[i]['cast'], 0) > 0:
                                csmerit[rac[i]['cast']] += 1
                            else:
                                data_dict['OPEN'] -= 1
                            Allocated_students.append(rac[i])
                            rac.pop(0)
                             
                                                  
                      else:
                            break  
                    #  print(type(Allocated_students))
        # print(rac)        
        Allocated = sorted(Allocated_students ,key=lambda x:(-x['percentage']))
        
        return render(request , 'Admin_OP/Provisional/second_year.html',{
            'BACKLOG_YES':Backlog_Yes_students , 
            'BACKLOG_NO':Backlog_NO_students ,
            'Allocated_students':Allocated,
            'student_seat':student_seat,
            'waiting':rac,
            'open_student_seat':open_student_seat
        })
    request.session['year'] = 'second'
    countnew = HostelData2.objects.filter(status='not_verified').count()
    countgriv = HostelData2.objects.filter(status='not_accepted').count()
    countedit = HostelData2.objects.filter(status='edited').count()
    countaccepted = HostelData2.objects.filter(status='accepted').count()
    
    return render(request , 'Admin_OP/reports/year2.html',{'data':data,'new':countnew,'griv':countgriv,'edit':countedit,'accept':countaccepted} )


def Year1_report(request):
    data = HostelData3.objects.filter(status="accepted")
    if request.method == 'POST':
        tseets = int(request.POST['Tseats'])
        print(str(tseets) + "tseats")
        OPENseets = int(request.POST['OPEN'])
        OBCseets = int(request.POST['OBC'])
        SCseets = int(request.POST['SC'])
        STseets = int(request.POST['ST'])
        NTseets = int(request.POST['NT'])
        SBCseets = int(request.POST['SBC'])
        
        data_dict = {}
        for key, value in request.POST.items():
            try:
                data_dict[key] = int(value)
            except ValueError:
                data_dict[key] = value
        del data_dict['Tseats']       
        sumseats = sum(value for value in data_dict.values() if isinstance(value, int))
        # sumseats = OPENseets+OBCseets+SCseets+STseets+NTseets+SBCseets
        if tseets != sumseats:
            return HttpResponse("Invalid Seats")
        backlog_YES_students = data.filter(Backlog='YES')
        backlog_NO_students = data.filter(Backlog='NO')
        
        available_seats = {
            'OBC': OBCseets,
            'SC': SCseets,
            'ST': STseets,
            'NT': NTseets,
            'SBC':SBCseets
        }
        
        Backlog_NO_students = sorted(backlog_NO_students ,key=lambda x:(-x.percentage))
        Backlog_Yes_students = sorted(backlog_YES_students ,key=lambda x:( x.Nu_Backlog , -x.percentage))
        
        print(data_dict)       
        Allocated_students = []
        count = 1
        open_student_seat = {}
        csmerit={
            'OPEN':0,
            'OBC':0,
            'SC':0,
            'SBC':0,
            'NT':0,
            'ST':0
        }
        ls = ['OBC','SC','SBC','NT','ST']
        
        # for OPENs
        for i in range(OPENseets):
            # print(i)
            if backlog_NO_students.__len__() == i:
                break
            
            student = Backlog_NO_students[i]
            stud = vars(student) 
            stud['merit_no'] = ''               
            csmerit[student.cast] += 1
            # print(csmerit[student.cast])
            seat = student.cast+'-'+ str(csmerit[student.cast]) #merit no
            stud['merit_no'] = ''
            stud['quota'] = 'OPEN'
            Allocated_students.append(stud)
            data_dict['OPEN'] -= 1
            
            print(stud['name'])
            # tseets -= 1 
            open_student_seat[student.name] = seat
            count += 1
        
        student_seat = {}
        rac = []
        
        #for other categories
        for student in Backlog_NO_students:
            stud = vars(student)
            # print(Allocated_students)
            if stud in Allocated_students:
                # print("in pass")
                pass
            else:
                student_category = student.cast
                if data_dict.get(student_category,0) > 0:
                    # allotment code
                    csmerit[student.cast] += 1
                    seat = student.cast+'-'+''+str(csmerit[student.cast])
                    # student_seat[student.name] = seat
                    data_dict[student_category] -= 1
                    stud['merit_no'] = seat
                    stud['quota'] = student.cast
                    Allocated_students.append(stud)
                    # print (student.name +'  '+ seat)
                else:
                    # obc to sbc
                    if student_category == 'SBC' and data_dict.get('OBC',0) > 0 :
                      csmerit['OBC'] += 1
                      seat = student.cast+'-'+''+str(csmerit[student.cast])
                    #   student_seat[student.name] = seat
                      data_dict['OBC'] -= 1
                      stud['merit_no'] = seat
                      stud['quota'] = 'OBC'
                      Allocated_students.append(stud)
                      
                      print(stud['name'])
                      rac.append(stud)
                      
                      # sc to st
                    if student_category == 'ST' and data_dict.get('SC',0) > 0 :
                      csmerit['SC'] += 1
                      seat = student.cast+'-'+''+str(csmerit[student.cast])
                    #   student_seat[student.name] = seat
                      data_dict['SC'] -= 1
                      stud['merit_no'] = seat
                      stud['quota'] = 'SC'
                      Allocated_students.append(stud)
                     ##  st to sc
                    if student_category == 'SC' and data_dict.get('ST',0) > 0 :
                      csmerit['ST'] += 1
                      seat = student.cast+'-'+''+str(csmerit[student.cast])
                    #   student_seat[student.name] = seat
                      data_dict['ST'] -= 1
                      stud['merit_no'] = seat
                      stud['quota'] = 'ST'
                      Allocated_students.append(stud)
                      
                    print(stud['name'])
                    rac.append(stud)  
             #rac       
                # print(rac)
                for i in range(len(rac)):
                    #   print(i)
                      print(tseets)
                      fn_available_seats = tseets - len(Allocated_students) 
                      if fn_available_seats > 0:
                            
                            print("in rac")
                            rac[i]['merit_no'] = ''
                            rac[i]['quota'] = 'General Merit Against Vacancy'
                            if data_dict.get(rac[i]['cast'], 0) > 0:
                                csmerit[rac[i]['cast']] += 1
                            else:
                                data_dict['OPEN'] -= 1
                            Allocated_students.append(rac[i])
                            rac.pop(0)
                             
                                                  
                      else:
                            break  
                    #  print(type(Allocated_students))
        # print(rac)        
        Allocated = sorted(Allocated_students ,key=lambda x:(-x['percentage']))
        
        return render(request , 'Admin_OP/Provisional/first_year.html',{
            'BACKLOG_YES':Backlog_Yes_students , 
            'BACKLOG_NO':Backlog_NO_students ,
            'Allocated_students':Allocated,
            'student_seat':student_seat,
            'waiting':rac,
            'open_student_seat':open_student_seat
        })
        
    request.session['year'] = 'first'
    countnew = HostelData1.objects.filter(status='not_verified').count()
    countgriv = HostelData1.objects.filter(status='not_accepted').count()
    countedit = HostelData1.objects.filter(status='edited').count()
    countaccepted = HostelData1.objects.filter(status='accepted').count()
    
    return render(request , 'Admin_OP/reports/year1.html',{'data':data,'new':countnew,'griv':countgriv,'edit':countedit,'accept':countaccepted} )


def important_dates(request):
    with open(file_path2, 'r') as file:
        lines = file.readlines()
    print("lines", lines)
    p3 = lines[0]
    p3y=p3[0:4]
    p3m=p3[5:7]
    p3d=p3[8:10]
    f3 = lines[1]
    f3y=f3[0:4]
    f3m=f3[5:7]
    f3d=f3[8:10]
    ED = lines[2]
    edy=ED[0:4]
    edm=ED[5:7]
    edd=ED[8:10]
    SD = lines[3]
    sdy=SD[0:4]
    sdm=SD[5:7]
    sdd=SD[8:10]
    acc = lines[13].strip()  
    if acc == "ON":
        return render(request, 'studates/dates.html', {'p3y': p3y,'p3m':p3m,'p3d':p3d, 'f3y': f3y,'f3m':f3m,'f3d':f3d,'edy': edy,'edm':edm,'edd':edd,'sdy': sdy,'sdm':sdm,'sdd':sdd})
    else:
        return render(request,'Home/thirdyeardes.html', {'message':'Link is Disabled For Now, Wait for further updates '})


def important_dates2(request):
    with open(file_path2, 'r') as file:
        lines = file.readlines()
    p3 = lines[4]
    p3y=p3[0:4]
    p3m=p3[5:7]
    p3d=p3[8:10]
    f3 = lines[5]
    f3y=f3[0:4]
    f3m=f3[5:7]
    f3d=f3[8:10]
    ED = lines[6]
    edy=ED[0:4]
    edm=ED[5:7]
    edd=ED[8:10]
    SD = lines[7]
    sdy=SD[0:4]
    sdm=SD[5:7]
    sdd=SD[8:10]
    acc = lines[14].strip()  
    if acc == "ON":
        return render(request, 'studates/date2.html',{'p3y': p3y,'p3m':p3m,'p3d':p3d, 'f3y': f3y,'f3m':f3m,'f3d':f3d,'edy': edy,'edm':edm,'edd':edd,'sdy': sdy,'sdm':sdm,'sdd':sdd})
    else:
               return render(request,'Home/secondyeardes.html', {'message':'Link is Disabled For Now, Wait for further updates '})


def important_dates1(request):
    with open(file_path2, 'r') as file:
        lines = file.readlines()
    p3 = lines[8]
    print(p3)
    p3y=p3[0:4]
    p3m=p3[5:7]
    p3d=p3[8:10]
    f3 = lines[9]
    f3y=f3[0:4]
    f3m=f3[5:7]
    f3d=f3[8:10]
    ED = lines[10]
    edy=ED[0:4]
    edm=ED[5:7]
    edd=ED[8:10]
    SD = lines[11]
    sdy=SD[0:4]
    sdm=SD[5:7]
    sdd=SD[8:10]
    acc = lines[15].strip()  
    print(f3)
    if acc == "ON":
        return render(request, 'studates/dates1.html', {'p3y': p3y,'p3m':p3m,'p3d':p3d, 'f3y': f3y,'f3m':f3m,'f3d':f3d,'edy': edy,'edm':edm,'edd':edd,'sdy': sdy,'sdm':sdm,'sdd':sdd})
    else:
        return render(request,'Home/firstyeardes.html', {'message':'Link is Disabled For Now, Wait for further updates '})

def close_impdates3(request):
    if request.method=="POST":
        decide  = str(request.POST['student_access'])
        if decide == 'OFF':
            with open(file_path2, 'r+') as file:
                lines = file.readlines()
                lines[13] = "OFF\n"
                file.seek(0)
                file.writelines(lines)
        if decide == 'ON':
            with open(file_path2, 'r+') as file:
                lines = file.readlines()
                lines[13] = "ON\n"
                file.seek(0)
                file.writelines(lines)
    return render(request , 'Admin_OP\closeimdates.html\cimp3.html')

def close_impdates2(request):
    if request.method=="POST":
        decide  = str(request.POST['student_access'])
        if decide == 'OFF':
            with open(file_path2, 'r+') as file:
                lines = file.readlines()
                lines[14] = "OFF\n"
                file.seek(0)
                file.writelines(lines)
        if decide == 'ON':
            with open(file_path2, 'r+') as file:
                lines = file.readlines()
                lines[14] = "ON\n"
                file.seek(0)
                file.writelines(lines)
    return render(request , 'Admin_OP\closeimdates.html\cimp2.html')

def close_impdates1(request):
    if request.method=="POST":
        decide  = str(request.POST['student_access'])
        if decide == 'OFF':
            with open(file_path2, 'r+') as file:
                lines = file.readlines()
                lines[15] = "OFF\n"
                file.seek(0)
                file.writelines(lines)
        if decide == 'ON':
            with open(file_path2, 'r+') as file:
                lines = file.readlines()
                lines[15] = "ON\n"
                file.seek(0)
                file.writelines(lines)
    return render(request , 'Admin_OP\closeimdates.html\cimp1.html')

def closeplist(request):
    decide = None
    if request.method=="POST":
        decide  = str(request.POST['student_access'])
    if decide == 'ON':
        with open(file_path5 , 'r+') as file:
            lines = file.readlines()
            lines[0] = 'ON\n'
            file.seek(0)
            file.writelines(lines)
    if decide == 'OFF':
        with open(file_path5 , 'r+') as file:
            lines = file.readlines()
            lines[0] = 'OFF\n'
            file.seek(0)
            file.writelines(lines)
    return render(request , 'Admin_OP/closeimdates.html/plist3.html')    

def closeflist(request):
    decide = None
    if request.method=="POST":
        decide  = str(request.POST['student_access'])
    if decide == 'ON':
        with open(file_path5 , 'r+') as file:
            lines = file.readlines()
            lines[1] = 'ON\n'
            file.seek(0)
            file.writelines(lines)
    if decide == 'OFF':
        with open(file_path5 , 'r+') as file:
            lines = file.readlines()
            lines[1] = 'OFF\n'
            file.seek(0)
            file.writelines(lines)
    return render(request , 'Admin_OP/closeimdates.html/flist3.html')    

def closeplist2(request):
    decide = None
    if request.method=="POST":
        decide  = str(request.POST['student_access'])
    if decide == 'ON':
        with open(file_path5 , 'r+') as file:
            lines = file.readlines()
            lines[2] = 'ON\n'
            file.seek(0)
            file.writelines(lines)
    if decide == 'OFF':
        with open(file_path5 , 'r+') as file:
            lines = file.readlines()
            lines[2] = 'OFF\n'
            file.seek(0)
            file.writelines(lines)
    return render(request , 'Admin_OP/closeimdates.html/plist2.html')    

def closeflist2(request):
    decide = None
    if request.method=="POST":
        decide  = str(request.POST['student_access'])
    if decide == 'ON':
        with open(file_path5 , 'r+') as file:
            lines = file.readlines()
            lines[3] = 'ON\n'
            file.seek(0)
            file.writelines(lines)
    if decide == 'OFF':
        with open(file_path5 , 'r+') as file:
            lines = file.readlines()
            lines[3] = 'OFF\n'
            file.seek(0)
            file.writelines(lines)
    return render(request , 'Admin_OP/closeimdates.html/flist2.html')    


def closeplist1(request):
    decide = None
    if request.method=="POST":
        decide  = str(request.POST['student_access'])
    if decide == 'ON':
        with open(file_path5 , 'r+') as file:
            lines = file.readlines()
            lines[4] = 'ON\n'
            file.seek(0)
            file.writelines(lines)
    if decide == 'OFF':
        with open(file_path5 , 'r+') as file:
            lines = file.readlines()
            lines[4] = 'OFF\n'
            file.seek(0)
            file.writelines(lines)
    return render(request , 'Admin_OP/closeimdates.html/plist1.html')    

def closeflist1(request):
    decide = None
    if request.method=="POST":
        decide  = str(request.POST['student_access'])
    if decide == 'ON':
        with open(file_path5 , 'r+') as file:
            lines = file.readlines()
            lines[5] = 'ON'
            file.seek(0)
            file.writelines(lines)
    if decide == 'OFF':
        with open(file_path5 , 'r+') as file:
            lines = file.readlines()
            lines[5] = 'OF'
            file.seek(0)
            file.writelines(lines)
    return render(request, 'Admin_OP/closeimdates.html/flist1.html')

def plistshow(request):
    with open(file_path5 , 'r') as file:
        lines = file.readlines()
    if lines[0] == 'ON\n':
        data = Lists.objects.all()
        return render(request , 'studates/lists_show.html',{'data':data})
    else:
        messages.error(request,"Link is Disabled by Admin")
        redirect('thirdyrdes')    
    
def flistshow(request):
    with open(file_path5 , 'r') as file:
        lines = file.readlines()
    if lines[1] == 'ON\n':
        data = Lists.objects.all()
        return render(request , 'studates/list_show2.html',{'data':data})
    else:
        messages.error(request,"Link is Disabled by Admin")
        redirect('thirdyrdes')
        
def plistshow22(request):
    with open(file_path5 , 'r') as file:
        lines = file.readlines()
    if lines[2] == 'ON\n':
        data = Lists.objects.all()
        return render(request , 'studates/listyear2.html',{'data':data})
    else:
        messages.error(request,"Link is Disabled by Admin")
        redirect('secondyrdes')
        
        
def flistshow22(request):
    with open(file_path5 , 'r') as file:
        lines = file.readlines()
    if lines[3] == 'ON\n':
        data = Lists.objects.all()
        return render(request , 'studates/listyears2.html',{'data':data})
    else:
        messages.error(request,"Link is Disabled by Admin")
        redirect('secondyrdes')
    
def plistshow11(request):
    with open(file_path5 , 'r') as file:
        lines = file.readlines()
    if lines[4] == 'ON\n':
        data = Lists.objects.all()
        return render(request , 'studates/listyear1.html',{'data':data})
    else:
        messages.error(request,"Link is Disabled by Admin")
        return redirect('firstyrdes')
        
def flistshow11(request):
    with open(file_path5 , 'r') as file:
        lines = file.readlines()
    if lines[5] == 'ON':
        data = Lists.objects.all()
        return render(request , 'studates/listyears1.html',{'data':data})
    else:
        messages.error(request,"Link is Disabled by Admin")
        return redirect('firstyrdes')

    
def plistUP(request):
    s = Lists.objects.get(k=101010)
    if request.method == 'POST':
        p3 = request.FILES.get('p3')
        if p3:
            s.p3 = p3
        s.save()          
        return render(request , 'Admin_OP/lists/plist.html', {'message':'Provisional List uploaded successfully'})
  
    return render(request , 'Admin_OP/lists/plist.html')


def plistUP2(request):
    s = Lists.objects.get(k=101010)
    if request.method == 'POST':
        p2 = request.FILES.get('p1')
        if p2:
            s.p2 = p2
        s.save() 
        return render(request , 'Admin_OP/lists/plist2.html', {'message':'Provisional List uploaded successfully'})
           
    return render(request , 'Admin_OP/lists/plist2.html')


def plistUP1(request):
    s = Lists.objects.get(k=101010)
    if request.method == 'POST':
        p1 = request.FILES.get('p1')
        if p1:
            s.p1 = p1
        s.save()
        return render(request , 'Admin_OP/lists/plist1.html', {'message':'Provisional List uploaded successfully'})
            
    return render(request , 'Admin_OP/lists/plist1.html')


def flistUP(request):
    s = Lists.objects.get(k=101010)
    if request.method == 'POST':
        f3 = request.FILES.get('f3')
        if f3:
            s.f3 = f3 
        s.save()
        return render(request , 'Admin_OP/lists/flist.html', {'message':'Final Merit List uploaded successfully'})
      
    return render(request , 'Admin_OP/lists/flist.html')

def flistUP2(request):
    s = Lists.objects.get(k=101010)
    if request.method == 'POST':
        f2 = request.FILES.get('f2')
        if f2:
            s.f2 = f2
        s.save()
        return render(request , 'Admin_OP/lists/flist2.html', {'message':'Final Merit List uploaded successfully'})
      
    return render(request , 'Admin_OP/lists/flist2.html')

def flistUP1(request):
    s = Lists.objects.get(k=101010)
    if request.method == 'POST':
        f1 = request.FILES.get('f1')
        if f1:
            s.f1 = f1  
        s.save()
        return render(request , 'Admin_OP/lists/flist1.html', {'message':'Final Merit List uploaded successfully'})
      
    return render(request , 'Admin_OP/lists/flist1.html')

def up_date(request):
    if request.method == 'POST':
        p3 = str(request.POST['p3'])
        f3 = str(request.POST['f3'])
        ED = str(request.POST['ED'])
        SD = str(request.POST['SD'])
        with open(file_path2, 'r+') as file:
            lines = file.readlines()
            lines[0] = p3+"\n"
            lines[1] = f3+"\n"
            lines[2] = ED+"\n"
            lines[3] = SD+"\n"
            file.seek(0)
            file.writelines(lines)
    return render(request,'Admin_OP/dateChange/date.html')

def up_date2(request):
    SD = 0
    if request.method == 'POST':
        p3 = str(request.POST['p3'])
        f3 = str(request.POST['f3'])
        ED = str(request.POST['ED'])
        SD = str(request.POST['SD'])
        with open(file_path2, 'r+') as file:
            lines = file.readlines()
            lines[4] = p3+"\n"
            lines[5] = f3+"\n"
            lines[6] = ED+"\n"
            lines[7] = SD+"\n"
            file.seek(0)
            file.writelines(lines)
    return render(request,'Admin_OP/dateChange/date2.html')

def up_date1(request):
    if request.method == 'POST':
        p3 = str(request.POST['p3'])
        f3 = str(request.POST['f3'])
        ED = str(request.POST['ED'])
        SD = str(request.POST['SD'])
        print(SD)
        with open(file_path2, 'r+') as file:
            lines = file.readlines()
            lines[8] = p3+"\n"
            lines[9] = f3+"\n"
            lines[10] = ED+"\n"
            lines[11] = SD+"\n"
            file.seek(0)
            file.writelines(lines)
    return render(request,'Admin_OP/dateChange/date1.html')
def Provisional_list3(request):
    data = HostelData3.objects.all()
    data = sorted(data ,key=lambda x:(-x.percentage))
    return render(request , 'Admin_OP/Provisional1/third_year.html',{'data':data} )

def Provisional_list2(request):
    data = HostelData2.objects.all()
    data = sorted(data ,key=lambda x:(-x.percentage))
    return render(request , 'Admin_OP/Provisional1/second_year.html',{'data':data} )


def Provisional_list1(request):
    data = HostelData1.objects.all()
    data = sorted(data ,key=lambda x:(-x.percentage))
    return render(request , 'Admin_OP/Provisional1/first_year.html',{'data':data} )


def Search3(request):
    data1 = HostelData3.objects.all()

    data = sorted(data1 ,key=lambda x:(-x.percentage))
    name = ""
    if request.method == "POST":
        name = str(request.POST["search"])
    for i in data:
        if i.name == name or str(i.Enroll) == name:
            i1 = i
            return render(request, 'Admin_OP/form_Preview/formview2.html', {'s': i1})
    return render(request , 'Admin_OP/search.html')


def Search2(request):
    data1 = HostelData2.objects.all()

    data = sorted(data1 ,key=lambda x:(-x.percentage))
    name = ""
    if request.method == "POST":
        name = str(request.POST["search"])
    for i in data:
        if i.name == name or str(i.Enroll) == name:
            i1 = i
            return render(request, 'Admin_OP/form_Preview/formview1.html', {'s': i1})
    return render(request , 'Admin_OP/search2.html')


def get_data_from_fno(fno):
    # List of tables to check
    tables = [HostelData3, HostelData2, HostelData1]
    
    for table in tables:
        row = table.objects.filter(fno=fno).first()
        if row:
            return row
    return 0  
   
def get_data_from_enroll(enroll):
    # List of tables to check
    tables = [HostelData3, HostelData2, HostelData1]
    
    for table in tables:
        row = table.objects.filter(Enroll=enroll).first()
        if row:
            return row
    return 0  
   


def trans_id_checker(trans_id):
    # List of tables to check
    tables = [HostelData3, HostelData2, HostelData1]
    
    for table in tables:
        row = table.objects.filter(trans_id=trans_id).first()
        if row:
            return row
    return 0         

def Search1(request):
    data1 = HostelData1.objects.all()

    data = sorted(data1 ,key=lambda x:(-x.percentage))
    name = ""
    if request.method == "POST":
        name = str(request.POST["search"])
        i1 = get_data_from_enroll(name) 
     
        return render(request, 'Admin_OP/form_Preview/formview1.html', {'s': i1})

    return render(request , 'Admin_OP/search1.html')

def admin_Preview3(request, fno):
    s = HostelData3.objects.get(fno=fno)
    if request.method == "POST":
        print("hell")
        remark = request.POST["remark"]
        s.status = request.POST['application_status']
        s.remark = remark
        print(s.remark)
        s.save()
        return render(request, 'Admin_OP/reports/year3.html', {'s': s})


    return render(request, 'Admin_OP/form_Preview/formview2.html', {'s': s})


def admin_Preview2(request, fno):
    print("hellloo")
    s = HostelData2.objects.get(fno=fno)
    if request.method == "POST":
        remark = request.POST["remark"]
        s.status = request.POST['application_status']
        s.remark = remark
        print(s.remark)
        s.save()
        return render(request, 'Admin_OP/reports/year2.html', {'s': s})
    return render(request, 'Admin_OP/form_Preview/formview1.html', {'s': s})


def admin_Preview1(request, fno):
    print("hello")
    s = HostelData1.objects.get(fno=fno)
    if request.method == "POST":
        remark = request.POST["remark"]
        s.status = request.POST['application_status']
        s.remark = remark
        print(s.remark)
        s.save()
        return render(request, 'Admin_OP/reports/year1.html', {'s': s})
    return render(request, 'Admin_OP/form_Preview/formview.html', {'s': s})



def student_Preview(request):
        fno = request.session.get('fno')
        if fno:
            s = HostelData3.objects.get(fno=fno)
            return render(request, '3year\studentview.html', {'s': s})
        else:
            return render(request,'Home/thirdyeardes.html', {'message':"You Have not Filled Form Yet"})    



def student_Preview2(request):
        fno = request.session.get('fno')
        if fno:
            s = HostelData2.objects.get(fno=fno)
            return render(request, '2year\studentview.html', {'s': s})
        else:
                       return render(request,'Home/secondyeardes.html', {'message':"You Have not Filled Form Yet"})
   
def student_Preview1(request):
        fno = request.session.get('fno')
        if fno:
            s = HostelData1.objects.get(fno=fno)
            return render(request, '1year\studentview.html', {'s': s})
        else:
                       return render(request,'Home/firstyeardes.html', {'message':"You Have not Filled Form Yet"})



def stud_regis(request):
    #  if request.method == 'POST':
        # enroll = request.POST.get('enrollment_no')
        # passwd = request.POST.get('passwd')
        enroll = "2207061"
        paswd = "parth"
        obj = Students_login.objects.all().values()
        std_obj = std_usr(enroll,paswd)
        print("hi")
        if std_obj.is_valid():
          if Students_login.objects.filter(enrollment_no=enroll).exists():
             print(obj)
          else:
             std_obj.save() 
                 
        return HttpResponse("hey rez")
   


def newappl1(request):
    data = HostelData1.objects.all()
    not_verified = data.filter(status="not_verified")
    return render(request ,'Admin_OP/reports/newapplication.html',{"data":not_verified}) 


def newappl2(request):
    data = HostelData2.objects.all()
    not_verified = data.filter(status="not_verified")
    return render(request ,'Admin_OP/reports/newapplication.html',{"data":not_verified}) 


def newappl3(request):
    data = HostelData3.objects.all()
    not_verified = data.filter(status="not_verified")
    return render(request ,'Admin_OP/reports/newapplication.html',{"data":not_verified}) 


def receipt(request):
    if request.method == "POST":
        data = get_data_from_enroll(request.POST['enroll'])
        return render(request ,'receipt.html',{"s":data,'admin':'yes'})
        

    en = request.session.get('enroll')
    data = get_data_from_fno(request.session.get('fno'))
    # print(data.Backlog)
    return render(request ,'receipt.html',{"s":data})



def del_form(request):
    
        found = False
        for table in [HostelData3, HostelData2, HostelData1]:
            try:
                row = table.objects.get(fno=request.POST.get('fno'))
                row.delete()
                messages.success(request, "Form Deleted")
                found = True
                break  # Exit the loop if the row was found and deleted
            except table.DoesNotExist:
                # Continue to the next table if the row does not exist
                continue

        if not found:
            messages.error(request, "Form not found")
        
        return redirect('admin_log')
        
            

def admin_receipt(request):
    en = request.POST['enroll']
    # fno = request.POST['fno']
    print(en)
    data = get_data_from_enroll(en)
    if data != 0:
      print(data.SPhoto)
      return render(request ,'receipt.html',{"s":data}) 
    else:
        return render(request,'Admin_OP/index.html',{'msg':'Student not found '})



def accepted3(request):
    data = HostelData3.objects.all()
    accepted = data.filter(status="accepted")
    return render(request ,'Admin_OP/reports/accepted.html',{"data":accepted}) 

def accepted2(request):
    data = HostelData2.objects.all()
    accepted = data.filter(status="accepted")
    return render(request ,'Admin_OP/reports/accepted.html',{"data":accepted}) 


def accepted1(request):
    data = HostelData1.objects.all()
    accepted = data.filter(status="accepted")
    return render(request ,'Admin_OP/reports/accepted.html',{"data":accepted}) 



def griv3(request):
    data = HostelData3.objects.all()
    grivence = data.filter(status="not_accepted")
    return render(request ,'Admin_OP/reports/grivence.html',{"data":grivence}) 


def griv2(request):
    data = HostelData2.objects.all()
    grivence = data.filter(status="not_accepted")
    return render(request ,'Admin_OP/reports/grivence.html',{"data":grivence}) 


def griv1(request):
    data = HostelData1.objects.all()
    grivence = data.filter(status="not_accepted")
    return render(request ,'Admin_OP/reports/grivence.html',{"data":grivence}) 

def edit3(request):
    data = HostelData3.objects.all()
    grivence = data.filter(status="edited")
    return render(request ,'Admin_OP/reports/edited.html',{"data":grivence}) 

def edit2(request):
    data = HostelData2.objects.all()
    grivence = data.filter(status="edited")
    return render(request ,'Admin_OP/reports/edited.html',{"data":grivence}) 

def edit1(request):
    data = HostelData1.objects.all()
    grivence = data.filter(status="edited")
    return render(request ,'Admin_OP/reports/edited.html',{"data":grivence}) 


def form_preview3(request,fno):
    # try:
        # print(request)
        data = get_object_or_404(HostelData3, fno=fno)
        # 
        if request.method == "POST":
            # print(request['remark'])
            # data = vars(data)
            data.status = request.POST['application_status']
            data.remark = request.POST['remark']
            data.save()
            return render(request ,'Admin_OP/form_Preview/formview2.html',{"s":data})
        return render(request ,'Admin_OP/form_Preview/formview2.html',{"s":data})


def form_preview(request, fno):
        data = get_object_or_404(HostelData1, fno=fno)
        # 
        if request.method == "POST":
            # print(request['remark'])  
            # data = vars(data)
            data.status = request.POST['application_status']
            data.remark = request.POST['remark']
            data.save()
            return render(request ,'Admin_OP/form_Preview/formview.html',{"s":data})
        return render(request ,'Admin_OP/form_Preview/formview.html',{"s":data})


def form_preview2(request, fno):
        data = get_data_from_fno(fno)
        # data = get_object_or_404(HostelData2, fno=fno)
        
        if request.method == "POST":
            # print(request['remark'])
            # data = vars(data)
            data.status = request.POST['application_status']
            data.remark = request.POST['remark']
            data.save()
            return render(request ,'Admin_OP/form_Preview/formview1.html',{"s":data})
        return render(request ,'Admin_OP/form_Preview/formview1.html',{"s":data})



def grivence_render(request):
    data = HostelData1.objects.all()
    grivence = data.filter(status="not_accepted")
    return render(request, 'Admin_OP/reports/year1applications/grivence.html',{"data":grivence})

def grivence_render2(request):
    data = HostelData2.objects.all()
    grivence = data.filter(status="not_accepted")
    return render(request, 'Admin_OP/reports/year2applications/grivence.html',{"data":grivence})

def grivence_render3(request):
    data = HostelData3.objects.all()
    grivence = data.filter(status="not_accepted")
    return render(request, 'Admin_OP/reports/year3applications/grivence.html',{"data":grivence})

def accepted3(request):
    data = HostelData3.objects.all()
    accepted = data.filter(status="accepted")
    return render(request, 'Admin_OP/reports/year3applications/accepted.html',{"data":accepted})

def accepted2(request):
    data = HostelData2.objects.all()
    accepted = data.filter(status="accepted")
    return render(request, 'Admin_OP/reports/year2applications/accepted.html',{"data":accepted})

def accepted(request):
    data = HostelData1.objects.all()
    accepted = data.filter(status="accepted")
    return render(request, 'Admin_OP/reports/year1applications/accepted.html',{"data":accepted})

def edited(request):
    data = HostelData1.objects.all()
    edited = data.filter(status="edited")
    return render(request, 'Admin_OP/reports/year1applications/edited.html',{"data":edited})

def edited2(request):
    data = HostelData2.objects.all()
    edited = data.filter(status="edited")
    return render(request, 'Admin_OP/reports/year2applications/edited.html',{"data":edited})

def edited3(request):
    data = HostelData3.objects.all()
    edited = data.filter(status="edited")
    return render(request, 'Admin_OP/reports/year3applications/edited.html',{"data":edited})



def newapplication(request):
    data = HostelData1.objects.all()
    new = data.filter(status="not_verified")
    return render(request,"Admin_OP/reports/year1applications/newapplication.html",{'data':new})

def newapplication2(request):
    data = HostelData2.objects.all()
    new = data.filter(status="not_verified")
    return render(request,"Admin_OP/reports/year2applications/newapplication.html",{'data':new})

def newapplication3(request):
    data = HostelData3.objects.all()
    new = data.filter(status="not_verified")
    return render(request,"Admin_OP/reports/year3applications/newapplication.html",{'data':new})

    
def error(req):
   return render(req,'404.html',{'msg':''}) 




def up_per(req):
    if req.method == "GET":
      objs = HostelData2.objects.all()
      for data in objs:
            # print(data.outoff1)
            sem1 = (data.mark1/data.outoff1)*100
            print(sem1)
            
            if data.mark2 == 0 and data.outoff2 == 0: 
               sem2 = 0
               print(sem2)
            else: 
                sem2 = (data.mark2/data.outoff2)*100
                print(sem2)
            tot = (sem1+sem2)/2 
            data.percentage = tot
    #         # data.status = "accepted"
            print(tot)
            print("auto")
            data.save()
    
        #  mark1 = 865.00
        #  mar2 = 783.00
        #  t1 = 925.00
        #  t2 = 825.00
         
        #  sem1 = (mark1/t1)*100
        #  sem2 = (mar2/t2)*100
        #  per = (sem1+sem2)/2
        #  print(per)
         
###################################################################################








                 #JUST ANOTHER CODE BY PARTH THAKRE#

                 















####################################################################################