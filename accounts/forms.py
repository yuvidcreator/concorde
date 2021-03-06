from dataclasses import fields
from pyexpat import model
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django.contrib.auth.models import Group



#for admin signup
class AdminSigupForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','mobile','password1','password2']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = True
        user.save()
        my_admin_group = Group.objects.get_or_create(name='ADMIN')
        my_admin_group[0].user_set.add(user)
        return user



#for Customer signup
class CustomerSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email','mobile','first_name','last_name','password1','password2']
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.mobile = self.cleaned_data.get('mobile')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        customer = Investor.objects.create(user=user)
        customer.save()
        my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
        my_customer_group[0].user_set.add(user)
        return user





class InvestorProfileForm(forms.ModelForm):
    class Meta:
        model = Investor
        fields = ['profile_pic','full_address','bank_details','upi_no','date_of_birth']




class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['invested_amount','investment_date','investment_period','investment_note','status']



class InvestUpdateForm(forms.ModelForm):
    investor = forms.ModelChoiceField(queryset=Investor.objects.all().filter(status=True), empty_label="Select Investor", to_field_name="user_id")
    payment_status = forms.CheckboxInput()
    class Meta:
        model=Update
        fields=['investor','investment','next_payment_note','next_payment_date','payment_mode','transaction_id']