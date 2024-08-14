
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.conf.urls import handler404
from django.shortcuts import render



def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404= 'Hostel_Admission.urls.custom_404'


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('Hostel_Admission.urls')),
    #Home pages
    path('',views.home,name='home'),
        path('up_per',views.up_per,name='up_per'),

    
    path('pass_edit',views.pass_edit,name='pass_edit'),
    path('Admin_Login/',views.admin_log,name='admin_log'),
    path('Firstyear_Des/',views.firstyrdes,name='firstyrdes'),
    path('Secondyear_Des/',views.secondyrdes,name='secondyrdes'),
    path('Thirdyear_Des/',views.thirdyrdes,name='thirdyrdes'),
    path('logged_home/',views.logged_home,name='logged_home'),
    path('logout/',views.logout,name='logout'), 
    path('del_form/',views.del_form,name='del_form'), 
  
    path('HelpStudentPage/',views.HelpStudent,name='HelpStudent'),
    path('userregister/',views.userregister,name="userregister"),

    path('HelpAdminPage/',views.HelpAdmin,name='HelpAdmin'),
    path('userlogin/',views.userlogin,name='userlogin'),
 path('receipt/',views.receipt,name='receipt'),
  path('admin_receipt/',views.admin_receipt,name='admin_receipt'),

    #search students in admin dashboard
        path('search_student_3rdYear/',views.Search3,name='search3'),
        path('search_student_2ndYear/',views.Search2,name='search2'),
        path('search_student_1stYear/',views.Search1,name='search1'),
   
    path('student_access',views.close_Forms,name='close_form'),
    path('student_access2',views.close_Forms2,name='close_form2'),
    path('student_access1',views.close_Forms1,name='close_form1'),

    # student desktops
    path('appl_report/<str:year>/<str:type>',views.appl_report,name="appl_report"),
    
    path('Firstyear_Des/',views.firstyrdes,name='firstyrdes'),
    path('Secondyear_Des/',views.secondyrdes,name='secondyrdes'),
    path('Thirdyear_Des/',views.thirdyrdes,name='thirdyrdes'),

    #student forms
    path('First_year/',views.First_year,name='First_year'),
 path('Second_year/',views.Second_year,name='Second_year'),
        path('Third_year/',views.Third_year,name='Third_year'),

    path('error/',views.error,name='error'),
    ## Admin Log
    path('Admin_Login/',views.admin_log,name='admin_log'),

    path('admin_appl_edit/<str:fno>',views.admin_appl_edit,name='admin_appl_edit'),

          path('appl_edit/',views.appl_edit,name='appl_edit'),path('Student_view/',views.receipt,name='S_view1'),
        path('Student_view2/',views.receipt,name='S_view2'),
        path('Student_view3/',views.receipt,name='S_view3'),

        path('important_datea/',views.important_dates,name='imp_dates'),
        path('important_datea2/',views.important_dates2,name='imp_dates2'),
        path('important_datea1/',views.important_dates1,name='imp_dates1'),

        path('Up_Date/',views.up_date,name='up_date'),
        path('Up_Date2/',views.up_date2,name='up_date2'),
        path('Up_Date1/',views.up_date1,name='up_date1'),

        path('plist/',views.plistshow,name='plist'),
        path('flist/',views.flistshow,name='flist'),
        path('plist22/',views.plistshow22,name='plist22'),
        path('flist22/',views.flistshow22,name='flist22'),
        path('plist11/',views.plistshow11,name='plist11'),
        path('flist11/',views.flistshow11,name='flist11'),

        path('closeplist3/',views.closeplist,name='cplist3'),
        path('closeflist3/',views.closeflist,name='cflist3'),
        path('closeplist2/',views.closeplist2,name='cplist2'),
        path('closeflist2/',views.closeflist2,name='cflist2'),
        path('closeplist1/',views.closeplist1,name='cplist1'),
        path('closeflist1/',views.closeflist1,name='cflist1'),

        path('Addplist/',views.plistUP,name='addplist'),
        path('Addplist2/',views.plistUP2,name='addplist2'),
        path('Addplist1/',views.plistUP1,name='addplist1'),

        path('Addflist/',views.flistUP,name='addflist'),
        path('Addflist2/',views.flistUP2,name='addflist2'),
        path('Addflist1/',views.flistUP1,name='addflist1'),

        path('cimp3/',views.close_impdates3,name='cimp33'),
        path('cimp2/',views.close_impdates2,name='cimp22'),
        path('cimp1/',views.close_impdates1,name='cimp11'),

        # path('printstudentform/<int:fno3>/',views.printform,name='printf'),
        # path('printstudentform2/<int:fno2>/',views.printform2,name='printf2'),
        # path('printstudentform1/<int:fno1>/',views.printform1,name='printf1'),

        path('studregis/',views.stud_regis),

        path('newappl3/',views.newappl3),
        path('newappl2/',views.newappl2),
        path('newappl1/',views.newappl1),


        path('accepted3/',views.accepted3),
        path('accepted2/',views.accepted2),
        path('accepted1/',views.accepted1),

        path('grivence3/',views.griv3),
        path('grivence2/',views.griv2),
        path('grivence1/',views.griv1),

        path('edited3/',views.edit3),
        path('edited2/',views.edit2),
        path('edited1/',views.edit1),

        #each year admin home pages
        path('1stYear_Report/',views.Year1_report,name='report1'),
        path('3rdYear_Report/',views.Year3_report,name='report3'),
        path('2ndYear_Report/',views.Year2_report,name='report2'),
       
        # appln flow
        path('1stYear_Report/newapplication/',views.newapplication,name="newapplication"),
        path('2ndYear_Report/newapplication/',views.newapplication2,name="newapplication2"),
        path('3rdYear_Report/newapplication/',views.newapplication3,name="newapplication3"),
 
        path('Admin_Preview/<str:fno>/',views.admin_Preview3,name='admin_preview3'),
        path('Admin_Preview2/<str:fno>/',views.admin_Preview2,name='admin_preview2'),
        path('Admin_Preview1/<str:fno>/',views.admin_Preview1,name='admin_preview1'),


 
        path('1stYear_Report/grivence/',views.grivence_render,name="grivence"),
        path('2ndYear_Report/grivence/',views.grivence_render2,name="grivence2"),
        path('3rdYear_Report/grivence/',views.grivence_render3,name="grivence3"),

        path('1stYear_Report/accepted/',views.accepted,name="accepted"),
        path('2ndYear_Report/accepted/',views.accepted2,name="accepted2"),
        path('3rdYear_Report/accepted/',views.accepted3,name="accepted3"),

        path('1stYear_Report/editedapplications/',views.edited,name="editedapplications"),
        path('2ndYear_Report/editedapplications/',views.edited2,name="editedapplications2"),
        path('3rdYear_Report/editedapplications/',views.edited3,name="editedapplications3"),

        path('form_preview/<str:fno>',views.form_preview,name="form_preview"),
        path('form_preview2/<str:fno>',views.form_preview2,name="form_preview2"),
        path('form_preview3/<str:fno>',views.form_preview3,name='form_preview3'),


        path('1stYear_Report/',views.Year1_report,name='report1'),
        path('3rdYear_Report/',views.Year3_report,name='report3'),
        path('2ndYear_Report/',views.Year2_report,name='report2'),
        path('Provisional_list3/',views.Provisional_list3,name='Provisional_list3'),
        path('Provisional_list2/',views.Provisional_list2,name='Provisional_list2'),
        path('Provisional_list1/',views.Provisional_list1,name='Provisional_list1'),


        # path('3rdYear_Report/newapplication/form_preview/<int:fno>',views.form_preview3,name="form_preview3"),
 
] 