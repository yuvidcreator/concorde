from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('afterlogin/', afterlogin_view, name='afterlogin'),
    path('logout/', LogoutView.as_view(template_name='back/index1.html'),name='logout'),

    #----------------------SIGNUP URLS------------------------------------
    path('adminsignup/', AdminSignupView.as_view()),
    path('customersignup/', CustomerSignupView.as_view(), name="Customer-Signup"),

    #----------------------LOGIN URLS------------------------------------
    path('adminlogin/', LoginView.as_view(template_name='back/admin/admin-login.html'), name="Admin-Login"),
    # path('adminlogin/', AdminLoginView, name="Admin-Login"),
    path('customerlogin/', LoginView.as_view(template_name='back/customer/customer-login.html'), name="customerlogin"),
    # path('customerlogin/', CustomerLoginView, name="customerlogin"),

    #----------------------DASHBOARDS URLS------------------------------------
    path('admindash/', AdminDash, name="Admin-Dahsboard"),
    path('adminprofile/', AdminProfile, name="Admin-Profile"),
    path('customerdash/', CustomerDash, name="Customer-Dahsboard"),


    #----------------------ADMIN-CUSTOMERS APPROVALS URLS--------------------------------
    path('admin-approve-customer/', admin_approve_customer_view, name='admin-approve-customer'),
    path('approve-customer/<int:pk>/', approve_customer_view, name='approve-customer'),
    path('reject-customer/<int:pk>/', reject_customer_view, name='reject-customer'),
]