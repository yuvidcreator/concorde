from multiprocessing import context
from django.shortcuts import render, redirect,reverse,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from email import message

from .models import User, Investor, Investment
from .forms import *
from django.views.generic import CreateView
from django.contrib.auth import login
from django import template
from django.contrib.auth.models import Group

from django.core.mail import send_mail, send_mass_mail
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse


class AdminSignupView(CreateView):
    model = User
    form_class = AdminSigupForm
    template_name = 'back/admin/admin-signup.html'

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f'Account created for {user.username}!, now you can Login')
        # email_template = render_to_string('back/email_templates/accouncreation_email.html',{'name':user.username})
        # usrEmailmsg = EmailMessage(
        #     'Thanks for Creating an Account',
        #     email_template,
        #     settings.EMAIL_HOST_USER,
        #     [user.email],
        # )
        # usrEmailmsg.send(fail_silently=False)
        login(self.request, user)
        return redirect('Admin-Login')



class CustomerSignupView(CreateView):
    model = User
    form_class = CustomerSignupForm
    template_name = 'back/customer/customer-signup.html'

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f'Customer Account created for {user.username}! Your Account is in Review. Once Admin approves, then you can Login')
        # email_template = render_to_string('back/email_templates/customer_accouncreation_email.html',{'name':user.first_name,'username':user.username})
        # usrEmailmsg = EmailMessage(
        #     'Thanks for Creating an Account',
        #     email_template,
        #     settings.EMAIL_HOST_USER,
        #     # [user.email,'angryavin167@gmail.com'],
        #     [user.email,'yuvra@neurosoftech.org'],
        # )
        # usrEmailmsg.send(fail_silently=False)
        login(self.request, user)
        return redirect('afterlogin')
    


#-----------for checking user is Admin or Customer ---------------
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()




#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('Admin-Dahsboard')
    elif is_customer(request.user):
        accountapproval=Investor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('Customer-Dahsboard')
        else:
            return render(request,'back/customer/customer_wait_for_approval.html')




#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='Admin-Login')
@user_passes_test(is_admin)
def AdminDash(request):
    #for both table in admin dashboard
    customers=Investor.objects.all().order_by('-id')
    #for four cards
    customercount=Investor.objects.all().filter(status=True).count()
    pendingcustomercount=Investor.objects.all().filter(status=False).count()
    mydict={
    'customers':customers,
    'customercount':customercount,
    'pendingcustomercount':pendingcustomercount,
    }
    return render(request, 'back/admin/admin-index.html',context=mydict)



    
#------------------FOR APPROVING INVESTORS BY ADMIN----------------------
@login_required(login_url='Admin-Login')
@user_passes_test(is_admin)
def admin_approve_customer_view(request):
    #those whose approval are needed
    #for four cards
    customercount=Investor.objects.all().filter(status=True).count()
    pendingcustomercount=Investor.objects.all().filter(status=False).count()
    customers=Investor.objects.all().filter(status=False)
    mydict = {
        'customercount':customercount,
        'pendingcustomercount':pendingcustomercount,
        'customers':customers,
    }
    return render(request,'back/admin/admin_approve_customer.html',context=mydict)




@login_required(login_url='Admin-Login')
@user_passes_test(is_admin)
def approve_customer_view(request,pk):
    #approve customers
    customer=Investor.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    customer.status=True
    customer.save()
    # email_template = render_to_string('back/email_templates/admin_custmr_approved_email.html',{'name':user.first_name,'username':user.username})
    # usrEmailmsg = EmailMessage(
    #     'Success - Account has been Approved',
    #     email_template,
    #     settings.EMAIL_HOST_USER,
    #     # [user.email,'angryavin167@gmail.com'],
    #     [user.email,'yuvraj@neurosoftech.org']
    # )
    # usrEmailmsg.send(fail_silently=False)
    return redirect(reverse('admin-approve-customer'))



@login_required(login_url='Admin-Login')
@user_passes_test(is_admin)
def reject_customer_view(request,pk):
    #reject customers
    customer=Investor.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    # email_template = render_to_string('back/email_templates/admin_custmr_rejected_email.html',{'name':user.first_name})
    # usrEmailmsg = EmailMessage(
    #     'Sorry, Account has been Rejected',
    #     email_template,
    #     settings.EMAIL_HOST_USER,
    #     # [user.email,'angryavin167@gmail.com'],
    #     [user.email,'yuvraj@neurosoftech.org']
    # )
    # usrEmailmsg.send(fail_silently=False)
    return redirect(reverse('admin-approve-customer'))

#--------------------------------------------------------------------------------
















#---------------------------------------------------------------------------------
#------------------------ Investors/Customers RELATED VIEWS START ----------------
#---------------------------------------------------------------------------------
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def CustomerDash(request):
    context = {}
    if is_customer(request.user):
        accountapproval=Investor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            customer=Investor.objects.get(user_id=request.user.id)
            investment = Investment.objects.get(customer=customer)
            context={
                'customer':customer,
                'investment':investment
            }
            return render(request, 'back/customer/customer-index.html',context)
        else:
            return render(request,'back/customer/customer_wait_for_approval.html')