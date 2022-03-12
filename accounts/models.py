from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


gender=[('Male','Male'),
('Female','Female'),
('Other','Other'),
]


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    email = models.EmailField(unique=True, null=True)
    mobile = models.CharField(max_length=13, unique=True, null=True)


class Investor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    profile_pic = models.ImageField(default="avatar.png", upload_to='assets/customerprofiles/', blank=True, null=True)
    full_address = models.CharField(max_length=100,null=True, blank=True,)
    bank_details = models.CharField(max_length=300,null=True, blank=True,)
    upi_no = models.CharField(max_length=300,null=True, blank=True,)
    date_of_birth = models.CharField(max_length=100,null=True, blank=True,)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

    @property
    def get_email(self):
        return self.user.email

    @property
    def get_mobile(self):
        return self.user.mobile

    @property
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return str(self.user.first_name)



class Investment(models.Model):
    user = models.ForeignKey(Investor, on_delete=models.CASCADE, null=True, blank=True)
    invested_amount = models.CharField(max_length=100,null=True, blank=True,)
    investment_date = models.DateTimeField(auto_now=False)
    investment_period = models.CharField(max_length=100,null=True, blank=True,)
    investment_note = models.CharField(max_length=100,null=True, blank=True,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def _str_(self):
        return str(self.user.first_name+"has invested Rs."+self.invested_amount+" on "+self.investment_date)
    


class Update(models.Model):
    investor = models.PositiveIntegerField(null=True, blank=True)
    investment = models.PositiveIntegerField(null=True, blank=True)
    next_payment_note = models.CharField(max_length=100,null=True, blank=True,)
    next_payment_date = models.CharField(max_length=100,null=True, blank=True,)
    profit = models.CharField(max_length=50, null=True, blank=True)
    payment_mode = models.CharField(max_length=100,null=True, blank=True,)
    transaction_id = models.CharField(max_length=100,null=True, blank=True,)
    payment_date = models.CharField(max_length=100,null=True, blank=True,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payment_status = models.BooleanField(default=False) 

    def __str__(self):
        return str(self.user+" = "+self.next_payment_date)