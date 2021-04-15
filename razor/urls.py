"""razor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include


# normal views
# from payments.views import View_Home_Page, View_Student_Register, View_Student_Login, View_Student_Dashboard_Details, View_Student_Logout

#admin
#from payments.views import View_Error,View_dummy_dashboard, View_Admin_Login, View_Change_Password, View_Admin_Logout, students, show_students, edit_students, update_students, delete_students, View_All_Transaction

from payments.views import *

urlpatterns = [
    path('', View_Home_Page, name='home'),
    path('news/',View_News, name='news'),
    path('register/', View_Student_Register, name='register'),
    path('login/', View_Student_Login, name='login'),
    path('student_dashboard/', View_Student_Dashboard_Details, name='student_dashboard'),
    path('change_password/', View_Change_Password, name='change_password'),
    path('payments/', include('payments.urls'), name='payments'),
    path('dummy_dashboard/',View_dummy_dashboard,name='dummy_dashboard'),
    path('logout/',View_Student_Logout, name='logout'),
    
    #admin views
    path('admin/', View_Admin_Login, name='admin_login'),
    path('admin/transactions', View_All_Transactions, name='transactions'),
    path('admin/add_students/', View_Add_Students, name='add_students'),
    path('admin/show/', View_Show_Students, name='show'),
    path('admin/edit/<int:id>', View_Edit_Students, name='edit'),
    path('admin/update/<int:id>', View_Update_Students, name='update' ),
    path('admin/allorder', View_All_Orders, name='allorders'),
    path('admin/delete/<int:id>', View_Delete_Students, name='delete'),
    path('admin/logout/',View_Admin_Logout, name='admin_logout'),
 ]
