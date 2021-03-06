
<h1 align='center'> Screenshots of UI </h1>


### Student Home Page UI

<img src='https://github.com/hackzbhavin/Payment-WebApp-Razorpay/blob/main/static/assets/images/homepage.jpeg' />

----

### Student Dashboard Page UI

<img src='https://github.com/hackzbhavin/Payment-WebApp-Razorpay/blob/main/static/assets/images/dashboardpage.jpeg' />

----

### Modes of Payment

![Image of Payments Mode](static/assets/images/left-image.png)

-----
#### Screenshots and Images/UI of Project

![Image of UI](static/assets/images/dash.png)

----
----


### To run the project

Makemigrations for migration of settings.py file and to check installed libraries/module
- python3 manage.py makemigrations

Migrate Settings for database
- python3 manage.py migrate

To Runserver
- python3 manage.py runserver

### Git Commands

Push project to existing repositary without changing existing code with new branch

- git init

- git add .

- git commit -m '`your custom commit name`'

- git checkout -b `yourname/branch_name`

- git config --global user.email `your github emailid`

- git config --global user.name `your github username`

- git config --global --list
  > _CHECK USERNAME AND EMAIL_

- git remote set-url origin `url`

- git remote -v
  > _CHECK URL FETCHED_

- git branch
  > _CHECK BRANCH_

- git push --set-upstream origin `yourname/branch_name`
  
  
  
  -----
  -----
  
  #### CONFIGURATION in  razor/settings.py 
```
  DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'student_pay',                   
    'USER': 'root',
    'PASSWORD': 'root',
    'HOST': '127.0.0.1',                    
    'PORT': '8889',
    # 'OPTIONS':{
    #     'init_command':'SET sql_mode = "STRICT_TRANS_TABLES"'
    # }               
  }
}
```




