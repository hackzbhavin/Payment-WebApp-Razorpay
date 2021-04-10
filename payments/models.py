from django.db import models
from datetime import date
from django.db.models import IntegerField

engineering_year_choose = [
    ('FIRST YEAR','FIRST YEAR'),
    ('SECOND YEAR','SECOND YEAR'),
    ('THIRD YEAR','THIRD YEAR'),
    ('BACHELOR YEAR','BACHELOR YEAR')
    ]


branch_choose = [
    ('Information Technology', 'Information Technology'),
    ('Mechanical Engineering', 'Mechanical Engineering'),
    ('Computer Engineering', 'Computer Engineering'),
    ('Electronics Engineering', 'Electronics Engineering'),
    ('Aerospace Engineering', 'Aerospace Engineering'),
    ('Chemical Engineering', 'Chemical Engineering'),
    ('Civil Engineeing', 'Civil Engineeing')
    ]


# Create your models here.
class StudentFeesDetail(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    reference_id_card_unique_number =models.PositiveIntegerField()
    name= models.CharField(max_length=50)
    email = models.CharField(max_length=80)
    engineering_year = models.CharField(max_length=30,default='FIRST YEAR', choices = engineering_year_choose)
    batch = models.PositiveIntegerField(default=2020)
    branch = models.CharField(max_length=50,default='Computer Engineering', choices= branch_choose)

    fees_amount = models.IntegerField(default=0)

    class Meta:
        db_table = 'studentfeesdetail'



# # choices field
# gender_choose = [
#     ('male','Male'),
#     ('female','Female'),
# ]

# branch_choose = [
#     ('me', 'Mechanical Engg'),
#     ('cs', 'Computer Engg'),
#     ('it', 'Information Technology Engg'),
#     ('civil', 'Civil Engg'),
#     ('aerospace', 'Aerospace Engg'),
#     ('chemical', 'Chemical Engg'),
# ]

# batch_course_year=[
#     ('fy', 'First Year'),
#     ('sy', 'Second Year'),
#     ('ty', 'Third Year'),
#     ('by', 'Final Bachelor Year'),

# ]


# forms
# class StudentLoginDetails(models.Model):
#     id_card_unique_number = IntegerField(default=101, validators=[MaxLengthValidator(10), MinLengthValidator(3)])
#     name = models.CharField(max_length=50)
#     email =  models.EmailField(max_length=40,)  
#     password = models.CharField(max_length=200)
#     date_of_birth = models.DateField()

#     def calculate_age(self):
#         today = date.today()
#         try:
#             birthday = self.date_of_birth(year=today.year)
#         except ValueError:
#             birthday = self.date_of_birth.replace(year=today.year, day=born.day-1)

#         if birthday > today:
#             return today.year - born.year - 1
#         else:
#             return today.year - born.year        

#     home_address = models.CharField(max_length=100)
#     home_address_pin_code = models.IntegerField(validators=[MaxLengthValidator(6), MinLengthValidator(6)])
#     gender = models.CharField(max_length=10,choices=gender_choose)
#     phone_number = models.IntegerField(validators=[MaxLengthValidator(10), MinLengthValidator(10)])
#     batch_course_year = models.CharField(max_length=20,choices=batch_course_year)
#     branch = models.CharField(max_length=20,choices=branch_choose)
#     linkedin_profile_url =  models.URLField()
#     last_login = models.DateTimeField()
