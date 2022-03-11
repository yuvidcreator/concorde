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