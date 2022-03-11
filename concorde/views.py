from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponseRedirect
from django.core.mail import message, send_mail, EmailMessage

# Create your views here.


def HomePage(request):
    return render(request, 'front/index.html')


def AboutPage(request):
    return render(request, 'front/about.html')


def ContactPage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        message = request.POST.get('message')

        context = {
            'name' : name,
            'email' : email,
            'mobile' : mobile,
            'message' : message
        }
        print(context)
        eml_message = '''
            Customer Enquiry from Concorde Investment's Contact Page. 

            Customer Name: {}
            Customer Email: {}
            Customer Mobile: {}
            Message: {}

        '''.format(context['name'], context['email'], context['mobile'], context['message'])
        send_mail(context['email'], eml_message, '', ['angryavin167@gmail.com'])        
        return redirect('Thanks-Page')
    return render(request, 'front/contact.html')


def ComingsoonPage(request):
    return render(request, 'front/comingsoon.html')


def ThanksPage(request):
    return render(request, 'front/thanks.html')