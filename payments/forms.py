
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



from .models import StudentFeesDetail


class StudentFeeDetailsForm(ModelForm):
	class Meta:
		model = StudentFeesDetail
		fields = '__all__'

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']








# from django import forms
# from datetime import date
# from django.db.models import IntegerField
# from django.core.validators import MaxLengthValidator, MinLengthValidator

# # choices field
# gender_choose = (
#     ('male','Male'),
#     ('female','Female'),
# )

# branch_choose = (
#     ('me', 'Mechanical Engg'),
#     ('cs', 'Computer Engg'),
#     ('it', 'Information Technology Engg'),
#     ('civil', 'Civil Engg'),
#     ('aerospace', 'Aerospace Engg'),
#     ('chemical', 'Chemical Engg'),
# ) 

# batch_course_year=(
#     ('fy', 'First Year'),
#     ('sy', 'Second Year'),
#     ('ty', 'Third Year'),
#     ('by', 'Final Bachelor Year'),

# )




# # forms
# class StudentLoginDetails(forms.Form):
#     id_card_unique_number = IntegerField(default=101, validators=[MaxLengthValidator(10), MinLengthValidator(3)])
#     name = forms.CharField(max_length=50, required=True)
#     email =  forms.EmailField(max_length=40, required=True,)  
#     password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput)
#     date_of_birth = forms.DateField()

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

#     home_address = forms.CharField(widget=forms.Textarea, max_length=100)
#     home_address_pin_code = forms.IntegerField(validators=[MaxLengthValidator(6), MinLengthValidator(6)], required=False)
#     gender = forms.ChoiceField(choices=gender_choose, required=True)
#     phone_number = forms.IntegerField(validators=[MaxLengthValidator(10), MinLengthValidator(10)], required=False)
#     batch_course_year = forms.ChoiceField(choices=batch_course_year, required=False)
#     branch = forms.ChoiceField(choices=branch_choose, required=True)
#     linkedin_profile_url =  forms.URLField(initial='https://')

    