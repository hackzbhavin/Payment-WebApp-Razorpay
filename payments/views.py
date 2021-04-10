from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User, auth

# login logout and required login
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required

# imports 
from .models import *
from .forms import StudentFeeDetailsForm, CreateUserForm
from django.contrib import messages

# from django.contrib.auth.decorators import user_passes_test
from django.db.models import Max
from django.db import connection
import json
import requests



#razorpay 
import razorpay

#=====================================================================================
# razorpay api
#=====================================================================================

client = razorpay.Client(auth=("rzp_test_3rwBYBLYRPHJWd", "YEJHecBxRaXbusMTPxuykTZ4"))


#=====================================================================================
# Error View Page
#=====================================================================================


def View_Error(request):
    return render(request, 'error.html')



#=====================================================================================
# Registration View 
#=====================================================================================

def View_Student_Register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            print('else:::::::::')
            # print(form)
            if form.is_valid():
                print('inside if register form is valid')
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
                
        context = {'form':form}
        return render(request, 'register.html', context)


#=====================================================================================
# Login View 
#=====================================================================================

def View_Student_Login(request):
    # student_fees_details = StudentFeesDetail.objects.all()
    is_admin = request.user.is_superuser

    if not is_admin and request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            print('post method---->', username, password)
            if user is not None:
                login(request, user)
                print('--------> user is not none =====> ',user.id)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
        


    # print('else------> of f  * T = F')        
    context = {}
    return render(request, 'login.html', context)


#=====================================================================================
# for home page
#=====================================================================================


def View_Home_Page(request):
    current_user = request.user.id
    is_admin = request.user.is_superuser

    cursor = connection.cursor()
    cursor.execute("SELECT * from auth_user INNER JOIN studentfeesdetail ON auth_user.id = studentfeesdetail.id ")
    user_and_fees_inner_join = cursor.fetchall()


    # print(is_admin)
    if not is_admin:
        if  current_user :
            student_fees_details = StudentFeesDetail.objects.get(id=current_user)
    
            for results in user_and_fees_inner_join:
            # print(results[0])
                if current_user == results[0]:
                    context = {'student_fees_details':student_fees_details, 'result':results}
                    return render(request, 'home.html', context)
    logout(request) 
    return render(request,'home.html')

    # if student_fees_details.fees_amount == 0:
    #     messages.info(request, 'Paid Already')


#=====================================================================================
# Dashboard for student
#=====================================================================================

@login_required(login_url='login')
def View_Student_Dashboard_Details(request):
    current_user = request.user.id
    is_admin = request.user.is_superuser
    
    print('id========================================> ',current_user)

    print('===== Gender Detection Start ==========')
    store_name_for_gender= request.user.first_name
    response = requests.get('https://api.genderize.io?name='+ store_name_for_gender)
    data_of_gender = response.json()
    print('----->gender---->', data_of_gender['gender'])
    print('----->name---->', data_of_gender['name'])
    print()
    print('===== Gender Detection End ==========')

    if data_of_gender['gender'] == 'male':
        print('Male')
        gender_loop = 'MALE'

    elif data_of_gender['gender']== 'female':
        print('Female')
        gender_loop = 'FEMALE'

    else:
        print("Can't Detect")  
        gender_loop = 'NO'
  


    if not request.user.is_authenticated and is_admin:
        return redirect('login')
    

    #inner join query to view details
    cursor = connection.cursor()
    cursor.execute("SELECT * from auth_user INNER JOIN studentfeesdetail ON auth_user.id = studentfeesdetail.id ")
    user_and_fees_inner_join = cursor.fetchall()
    for results in user_and_fees_inner_join:
        # print(results[0])
        if current_user == results[0]:
            # print('Yes')
            # print(results) 
            context = {'result':results, 'gender_loop':gender_loop}
    
    return render(request, 'student_dashboard.html', context)


#=====================================================================================
# for changing password
#=====================================================================================

@login_required(login_url='login')
def View_Change_Password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})



#=====================================================================================
# order confirmation page
#=====================================================================================

@login_required(login_url='login')
def View_Order_Page(request):
    
    current_user = request.user.id
    if not request.user.is_authenticated:
        return redirect('login')
    
    results_studentdetails = StudentFeesDetail.objects.get(id=current_user)
    return render(request, 'order.html', {'data': results_studentdetails})



#=====================================================================================
# For Login
#=====================================================================================
# @login_required(login_url='login')
def View_Student_Logout(request):
    logout(request) 
    return redirect('home')        



#=====================================================================================
# Create order page comes after order.html page
#=====================================================================================

def View_Create_Order(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    current_user = request.user.id

    context = {}
    if request.method == 'POST':
        print("INSIDE Create Order!!!")
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        product = request.POST.get('product')

        results_studentdetails = StudentFeesDetail.objects.get(id=current_user)
 
        order_amount = 0
        if product == 'p1':
            order_amount = float(results_studentdetails.fees_amount * 100) 
        elif product == 'p4':
            order_amount = 10000

    
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {
            'Shipping address': 'Pune, Maharashtra'}

        # CREAING ORDER
        response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        order_id = response['id']
        order_status = response['status']
        print('order_Status ====> ', order_status)

        if order_status=='created':

            # Server data for user convinience
            context['product_id'] = product
            context['price'] = order_amount / 100
            context['name'] = name
            context['phone'] = phone
            context['email'] = email

            # data that'll be send to the razorpay for
            context['order_id'] = order_id

            print('order_Status ====> ', order_id)
            return render(request, 'confirm_order.html', context, {'data': results_studentdetails})


        # print('\n\n\nresponse: ',response, type(response))
    return HttpResponse('<h1>Error in  create order function</h1>')


#=====================================================================================
# Payment Page Summary 
#=====================================================================================
def View_Payment_Status(request):

    response = request.POST
    print('response======>', response['razorpay_payment_id'])
    print('response======>', response['razorpay_order_id'])
    print('response======>', response['razorpay_signature'])
    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature']
    }


    # VERIFYING SIGNATURE
    try:
        print(' **success** ')
        status = client.utility.verify_payment_signature(params_dict)
        print(status)
        #invoice_create = client.invoice.create(data=params_dict)        
        return render(request, 'order_summary.html', {'status': 'Payment Successful'})
    except:
        return render(request, 'order_summary.html', {'status': 'Payment Faliure!!!'})




#============================================================
#======================= For admin ==========================

#=====================================================================================
#======================= For admin login ==========================
#=====================================================================================

def View_Admin_Login(request):
    # student_fees_details = StudentFeesDetail.objects.all()
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('./show')
            else:
                messages.info(request, 'Username OR password is incorrect')
                
        context = {}
        return render(request, './admin/admin_login.html', context)


#=====================================================================================
#======================= For admin logout ==========================
#=====================================================================================

def View_Admin_Logout(request):
    logout(request) 
    return redirect('admin_login')        


#=====================================================================================
#======================= For Adding Students Data ==========================
#=====================================================================================

@permission_required('is_superuser',  login_url='admin_login')
def students(request):
    users_all = User.objects.all()
    students = StudentFeesDetail.objects.all().order_by('-id')[0]

    #inner join query
    cursor = connection.cursor()
    # cursor.execute("select * from auth_user join studentfeesdetail on auth_user.id=studentfeesdetail.id")
    cursor.execute("SELECT * from auth_user INNER JOIN studentfeesdetail ON auth_user.id = studentfeesdetail.id ")
    user_and_fees_inner_join = cursor.fetchall()
    # print(results)

    if request.method == 'POST':
        form = StudentFeeDetailsForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                return redirect('../show')
            except:
                # print('====== Except')
                pass
    else:
        form = StudentFeeDetailsForm()
        # print('else========?')
    
    return render(request, 'admin/add_students.html', {'form': form, 'students':students,'users_all':users_all, 'results':user_and_fees_inner_join })


#=====================================================================================
#======================= For Admin Show Detail of Students ==========================
#=====================================================================================


@permission_required('is_superuser',  login_url='admin_login')
def show_students(request):  
    students = StudentFeesDetail.objects.all()  

    #inner join query
    cursor = connection.cursor()
    # cursor.execute("select * from auth_user join studentfeesdetail on auth_user.id=studentfeesdetail.id")
    cursor.execute("SELECT * from auth_user INNER JOIN studentfeesdetail ON auth_user.id = studentfeesdetail.id ")
    user_and_fees_inner_join = cursor.fetchall()



    return render(request,"admin/show.html",{'students':students, 'results':user_and_fees_inner_join})  


#=====================================================================================
#======================= For Admin Edit Student Details ==========================
#=====================================================================================

@permission_required('is_superuser',  login_url='admin_login')
def edit_students(request, id):
    print('=====>edit===>', id)

  
    students = StudentFeesDetail.objects.get(id=id)  
    return render(request,'./admin/edit.html', {'students':students})  

#=====================================================================================
#======================= For admin To Update Student Details==========================
#=====================================================================================

@permission_required('is_superuser',  login_url='admin_login')
# def update_students(request, id):
#     print('=====>', id)  
#     students = StudentFeesDetail.objects.get(id=id)  
#     print('=========>students <=========',students.id)
#     print()
#     form = StudentFeeDetailsForm(request.POST, instance = students)  


#     print(form)
#     if form.is_valid():  
#         form.save()
#         print('=======> valif form ')  
#         return redirect("show")  
#     return render(request, 'admin/edit.html', {'students': students})  


def update_students(request, id):  
    students = StudentFeesDetail.objects.get(id=id)  
    form = StudentFeeDetailsForm(request.POST, instance = students) 
    for i in form:
        print(i)

    if form.is_valid(): 
        print('form is valid --------=========') 
        form.save()  
        return redirect("show")
    else:
        print('nothing')      
    return render(request, './admin/edit.html', {'students': students})  



#=====================================================================================
#======================= For admin to delete the students ==========================
#=====================================================================================

@permission_required('is_superuser',  login_url='admin_login')
def delete_students(request, id):  
    students = StudentFeesDetail.objects.get(id=id)  
    students.delete()  
    return redirect("../show")  

