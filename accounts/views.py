from cmath import e
from multiprocessing import context
from telnetlib import STATUS
from django.shortcuts import render, redirect,reverse,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from email import message

from .models import *
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
        # accountapproval=Investor.objects.all().filter(id=request.user.id,status=True)
        accountapproval=Investor.objects.get(user_id=request.user.id)
        if accountapproval.status==True:
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
    context={
    'customers':customers,
    'customercount':customercount,
    'pendingcustomercount':pendingcustomercount,
    }
    return render(request, 'back/admin/admin-index.html',context)



@login_required(login_url='Admin-Login')
@user_passes_test(is_admin)
def AdminProfile(request):
    auser = User.objects.get(id=request.user.id)
    context = {'auser':auser}
    if request.method == "POST":
        try:
            auser.username = request.POST['username']
            auser.first_name = request.POST['first_name']
            auser.last_name = request.POST['last_name']
            auser.mobile = request.POST['mobile']
            auser.email = request.POST['email']
            auser.save()
            message.success(request, "Profile Updated Successfully.")
        except:
            pass
    return render(request, 'back/admin/admin_profile.html', context)


    
#------------------FOR APPROVING INVESTORS BY ADMIN----------------------
@login_required(login_url='Admin-Login')
@user_passes_test(is_admin)
def admin_approve_customer_view(request):
    #those whose approval are needed
    #for four cards
    customercount=Investor.objects.all().filter(status=True).count()
    pendingcustomercount=Investor.objects.all().filter(status=False).count()
    customers=Investor.objects.all().filter(status=False)
    context = {
        'customercount':customercount,
        'pendingcustomercount':pendingcustomercount,
        'customers':customers,
    }
    return render(request,'back/admin/admin_approve_customer.html',context)




@login_required(login_url='Admin-Login')
@user_passes_test(is_admin)
def approve_customer_view(request,pk):
    #approve customers
    customer=Investor.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    customer.status=True
    customer.save()
    user.save()
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
    customer.delete()
    user.delete()
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



#------------------FOR APPROVING INVESTORS BY ADMIN----------------------
@login_required(login_url='Admin-Login')
@user_passes_test(is_admin)
def admin_customer_invest_list(request):
    #those whose approval are needed
    #for four cards
    # customers=Investor.objects.all().order_by('-id')
    customercount=Investor.objects.all().filter(status=True).count()
    pendingcustomercount=Investor.objects.all().filter(status=False).count()
    customers=Investor.objects.all()
    upadte = Update.objects.all()
    context = {
        'customercount':customercount,
        'pendingcustomercount':pendingcustomercount,
        'customers':customers,
        'upadte':upadte,
    }
    return render(request,'back/admin/admin_customer_invest_list.html',context)



@login_required(login_url='Admin-Login')
@user_passes_test(is_admin)
def admin_view_customers_investment(request, pk):
    customer=Investor.objects.get(id=pk)
    investment = Investment.objects.all().filter(user=customer, status=True)
    context= {'customer':customer, 'investment':investment}
    return redirect(request, 'back/admin/admin_invest_view.html', context)



@login_required(login_url='Admin-Login')
@user_passes_test(is_admin)
def admin_customer_invest_update(request, pk):
    customer=Investor.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    investUpdate = InvestUpdateForm(request.POST or None, instance=customer)
    context = {'customer':customer, 'investUpdate':investUpdate}
    if request.method == "POST":
        if investUpdate.is_valid() and customer.status==True:
            update = investUpdate.save(commit=False)
            investor=request.POST['investor']
            investment = request.POST['investment']
            next_payment_note = request.POST['next_payment_note']
            next_payment_date=request.POST['next_payment_date']
            payment_mode=request.POST['payment_mode']
            transaction_id=request.POST['transaction_id']
            print(investment,next_payment_note,next_payment_date)
            Update.objects.create(investor=investor,investment=investment,next_payment_note=next_payment_note,next_payment_date=next_payment_date,payment_mode=payment_mode,transaction_id=transaction_id,payment_status=True)
            messages.success(request, "Investment Status Updated Successfully.")
            return redirect('admin-customer-invest-list')
    else:
        return render(request, 'back/admin/admin_customer_invest_update.html', context)












#---------------------------------------------------------------------------------
#------------------------ Investors/Customers RELATED VIEWS START ----------------
#---------------------------------------------------------------------------------
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def CustomerDash(request):
    accountapproval=Investor.objects.get(user_id=request.user.id)
    # print(accountapproval.status==True)
    if accountapproval.status==True:
        try:
            customer=User.objects.get(id=request.user.id)
            nvstr = Investor.objects.get(user_id=request.user.id)
            # investment = Investment.objects.get(user_id=request.user.id)
            updates = Update.objects.all()
            context={
                'nvstr':nvstr,
                'customer':customer,
                'accountapproval':accountapproval,
                'updates':updates,
            }
            return render(request, 'back/customer/customer-index.html',context)
        except Exception as e:
            return HttpResponse(e)
    else:
        return redirect('afterlogin')




@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def CustomerProfile(request):
    cuser = User.objects.get(id=request.user.id)
    iuser = Investor.objects.get(user=cuser)
    nvstr = Investor.objects.get(user_id=request.user.id)
    userForm = InvestorProfileForm(request.POST or None, request.FILES or None, instance=iuser)
    context = {'userForm':userForm,'iuser':iuser,'nvstr':nvstr}
    if request.method == "POST":
        userForm = InvestorProfileForm(request.POST or None, request.FILES or None, instance=iuser)
        if userForm.is_valid():
            userForm.save()
            cuser.username = request.POST['username']
            cuser.first_name = request.POST['first_name']
            cuser.last_name = request.POST['last_name']
            cuser.mobile = request.POST['mobile']
            cuser.email = request.POST['email']
            cuser.save()
            print(cuser.mobile)
            messages.success(request, "Profile Updated Successfully.")
            return redirect('Customer-Profile')
    return render(request, 'back/customer/customer-profile.html', context)



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_invest(request):
    cuser=User.objects.get(id=request.user.id)
    iuser = Investor.objects.get(user=cuser)
    investForm = InvestmentForm(request.POST or None, request.FILES or None, instance=iuser)
    context={
        'iuser':iuser,
        'cuser':cuser,
        'investForm':investForm
    }
    return render(request, 'back/customer/customer-invest-view.html', context)



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_invest_updates(request):
    cuser=User.objects.get(id=request.user.id)
    iuser = Investor.objects.get(user=cuser)
    updates = Update.objects.all().filter(id=request.user.id)
    context = {'iuser':iuser,'updates':updates}
    return render(request, 'back/customer/customer-invest-updates-view.html', context)