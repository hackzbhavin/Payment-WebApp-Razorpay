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
import datetime


from django.views.decorators.csrf import csrf_exempt
import random
import string
import base64
from django.http import JsonResponse


#razorpay 
import razorpay

#=====================================================================================
#====> razorpay api
#=====================================================================================

razorpay_key_id = 'your key id'
razorpay_key_secret = 'your key secret'


client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))


#=====================================================================================
#====> Error View Page
#=====================================================================================

def View_Error(request):
    return render(request, 'error.html')

#=====================================================================================
#====> Registration View 
#=====================================================================================

def View_Student_Register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            # print('else:::::::::')
            # print(form)
            if form.is_valid():
                # print('inside if register form is valid')
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
                
        context = {'form':form}
        return render(request, 'register.html', context)


#=====================================================================================
#====> Login View 
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
            # print('post method---->', username, password)
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
#====> for Dummy Dashboard page
#=====================================================================================
def View_dummy_dashboard(request):

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

    context = {'gender_loop':gender_loop }
    return render(request, 'dummy_dashboard.html', context)


#=====================================================================================
#====> for Home page
#=====================================================================================

def View_Home_Page(request):
    current_user = request.user.id
    student_check = StudentFeesDetail.objects.all()
    is_admin = request.user.is_superuser

    # print(is_admin)
    if not is_admin:
        if  current_user :
            for i in student_check :
                if not StudentFeesDetail.objects.filter(id=current_user):
                    return redirect('dummy_dashboard')
                student_fees_details = StudentFeesDetail.objects.filter(id=current_user)
                print('heyyyyyyyy')
                cursor = connection.cursor()
                cursor.execute("SELECT * from auth_user INNER JOIN studentfeesdetail ON auth_user.id = studentfeesdetail.id ")
                user_and_fees_inner_join = cursor.fetchall()
                for results in user_and_fees_inner_join:
                    if current_user == results[0]:
                        context = {'student_fees_details':student_fees_details, 'result':results}
                        return render(request, 'home.html', context)
    logout(request) 
    return render(request,'home.html')



#=====================================================================================
#====> Dashboard for student
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
#====> for changing password
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
#====> Order confirmation page
#=====================================================================================

@login_required(login_url='login')
def View_Order_Page(request):
    
    current_user = request.user.id
    if not request.user.is_authenticated:
        return redirect('login')
    
    results_studentdetails = StudentFeesDetail.objects.get(id=current_user)
    return render(request, 'order.html', {'data': results_studentdetails})



#=====================================================================================
#====> For Logout
#=====================================================================================
# @login_required(login_url='login')
def View_Student_Logout(request):
    logout(request) 
    return redirect('home')        


#=====================================================================================
#====> Create order page comes after order.html page
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

            context['razorpay_key_id'] = razorpay_key_id

            # data that'll be send to the razorpay for
            context['order_id'] = order_id

            print('order_Status ====> ', order_id)
            return render(request, 'confirm_order.html', context)
            #return render(request, 'confirm_order.html', context, {'data': results_studentdetails})


        # print('\n\n\nresponse: ',response, type(response))
    return HttpResponse('<h1>Error in  create order function</h1>')

#=====================================================================================
#====> Payment Page Summary 
#=====================================================================================
def View_Payment_Status(request):
    print('===> Inside Payment Status <====')
    response = request.POST
    print('response======>', response['razorpay_payment_id'])
    print('response======>', response['razorpay_order_id'])
    print('response======>', response['razorpay_signature'])
    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature']
    }


    payment_id = response['razorpay_payment_id']
    order_id = response['razorpay_order_id']

    # VERIFYING SIGNATURE
    try:
        print(' **success** ')
        status = client.utility.verify_payment_signature(params_dict)
        print(status)
        return render(request, 'order_summary.html', {'status': 'Payment is Successful','payment_id':payment_id,'order_id':order_id  })
    except:
        return render(request, 'order_summary.html', {'status': 'Payment is Failed!!!'})



#============================================================
#====> For admin 
#=====================================================================================
#====> For admin login 
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
#====> For admin logout 
#=====================================================================================

def View_Admin_Logout(request):
    logout(request) 
    return redirect('admin_login')        


#=====================================================================================
#====> For Adding Students Data
#=====================================================================================

@permission_required('is_superuser',  login_url='admin_login')
def View_Add_Students(request):
    print('===View All Students Details====')

    users_all = User.objects.all()
    students = StudentFeesDetail.objects.all().order_by('-id')[0]

    #inner join query
    cursor = connection.cursor()
    cursor.execute("SELECT * from auth_user INNER JOIN studentfeesdetail ON auth_user.id = studentfeesdetail.id ")
    user_and_fees_inner_join = cursor.fetchall()


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
#====> For All transaction Details of Students 
#=====================================================================================

@permission_required('is_superuser',  login_url='admin_login')
def View_All_Transactions(request):
    # print('=== View_All_Transaction ====')
    resp = client.payment.fetch_all()  
    details = resp['items']
 
    # To convert time in normal format
    # for time in details:
    #     print()    
    #     store_unix_time = datetime.datetime.fromtimestamp(int(time['created_at'])).strftime('%d-%m-%Y %H:%M:%S')
    #     # print(store_unix_time)


    context = {'response':details}
    return render(request, 'admin/transactions.html', context)

#=====================================================================================
#====> For All Orders Details of Students Payments after Captured 
#=====================================================================================

@permission_required('is_superuser',  login_url='admin_login')
def View_All_Orders(request):
    resp = client.order.fetch_all()
    orders=resp['items']
    context = {'response':orders}
    return render(request, 'admin/allorders.html',context)

#=====================================================================================
#====> For Admin Show Detail of Students 
#=====================================================================================


@permission_required('is_superuser',  login_url='admin_login')
def View_Show_Students(request):  
    students = StudentFeesDetail.objects.all()  
    
    #inner join query
    cursor = connection.cursor()
    cursor.execute("SELECT * from auth_user INNER JOIN studentfeesdetail ON auth_user.id = studentfeesdetail.id ")
    user_and_fees_inner_join = cursor.fetchall()

    return render(request,"admin/show.html",{'students':students, 'results':user_and_fees_inner_join})  


#=====================================================================================
#====> For Admin Edit Student Details 
#=====================================================================================

@permission_required('is_superuser',  login_url='admin_login')
def View_Edit_Students(request, id):
    print('=====>edit===>', id)

  
    students = StudentFeesDetail.objects.get(id=id)  
    return render(request,'./admin/edit.html', {'students':students})  



#=====================================================================================
#====> For admin To Update Student Details
#=====================================================================================

@permission_required('is_superuser',  login_url='admin_login')
def View_Update_Students(request, id):  
    students = StudentFeesDetail.objects.get(id=id)  
    form = StudentFeeDetailsForm(request.POST, instance = students) 

    if form.is_valid(): 
        print('form is valid --------=========') 
        form.save()  
        return redirect("show")
    else:
        print('nothing')      
    return render(request, './admin/edit.html', {'students': students})  



#=====================================================================================
#====> For admin to delete the students 
#=====================================================================================

@permission_required('is_superuser',  login_url='admin_login')
def View_Delete_Students(request, id):  
    students = StudentFeesDetail.objects.get(id=id)  
    students.delete()  
    return redirect("../show")  

#=====================================================================================
#====> For news
#=====================================================================================
# api key from api-news
apikey = '286645ed941444c89f7d715940a1b527'

def View_News(request):
    #headlines
    url = ('https://newsapi.org/v2/top-headlines?'
       'country=in&'
       'apiKey='+apikey)
    response = requests.get(url)
    top_headlines = response.json()
    
    # channel
    news_channels = ('https://newsapi.org/v2/sources?apiKey='+apikey)
    response = requests.get(news_channels)
    channels = response.json()
    
    #sports
    sports_ind = ('https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey='+apikey)
    response = requests.get(sports_ind)
    sports = response.json()


    #technology
    tech_ind = ('https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey='+apikey)
    response = requests.get(tech_ind)
    tech = response.json()

    #business
    business_ind = requests.get('https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey='+apikey)
    business = business_ind.json()

    #health
    health_ind = requests.get('https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey='+apikey)
    health = health_ind.json()

    #science
    science_ind = requests.get('https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey='+apikey)
    science = science_ind.json()

    #papers
    paper_times_of_india = requests.get('https://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey='+apikey)
    times_of_india = paper_times_of_india.json()

    bbc_newsp = requests.get('https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey='+apikey)
    bbc_news = bbc_newsp.json()

    context = {
        'top_headlines':top_headlines,
        'channels':channels,
        'sports':sports, 
        'technology':tech,
        'business':business,
        'health':health,
        'science':science,
        'times_of_india':times_of_india,
        'bbc_news':bbc_news,
        }
    return render(request,'news.html', context)  

#=====================================================================================
#====> For snap
#=====================================================================================
def View_Snapshot(request):
    if request.method == "POST":
        data = request.body
        data = json.loads(data[0:len(data)])
        print(data)
        c = Category.objects.get(pk=1)
        temp = len('data:image/jpeg;base64,')
        for d in data:
            d = d[temp:len(d)]
            imgdata = base64.b64decode(d)
            filename = randomString()+'.jpg'  # I assume you have a way of picking unique filenames
            with open('media/'+filename, 'wb') as f:
                f.write(imgdata)
            i = Images.objects.create(category=c, file=filename)
            i.save()
            print(i)
        return JsonResponse({'data': 'Success'})
    return render(request, 'takesnap.html')

def randomString(stringLength=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
