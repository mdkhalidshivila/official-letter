from django.shortcuts import render

# Create your views here.
from traceback import format_stack
from django.shortcuts import redirect, render, HttpResponse
from django.views.decorators.csrf import csrf_protect 
from .models import Bill, Rejected, Reexp
from .forms import BillForm, RejectedForm, ReexpForm
from .utils import Render
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm, LinkMail
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout #add this
from django.contrib.auth.forms import AuthenticationForm #add this
from django.core.mail import send_mail, BadHeaderError
from django.template import loader
import pandas as pd
from django.http import JsonResponse
from . import forms
from django.db.models import Q
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

@csrf_protect 
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

@csrf_protect 
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})


@csrf_protect 
def logout_request(request):
    logout(request)
    msg = messages.info(request, "You have successfully logged out.") 
    return redirect("login")

@login_required
def index(request):
    bill = Bill.objects.all().order_by('employee_id')
    return render(request, 'index.html', {'bill': bill})

@login_required
def detailView(request, id):
    bill_det = Bill.objects.get(id = id)
    bill = Bill.objects.filter(id =id)
    return render(request, 'bill.html', {'bill': bill, 'bill_det': bill_det})
@login_required
def formView(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BillForm()
    return render(request, 'bill-form.html', {'form':form})

@login_required
def deleteView(request,id):
    bill = Bill.objects.get(id = id)
    bill.delete()
    return redirect('index')

@csrf_protect 
def updatedata(request, id):
    if request.method == 'POST':
        pi = Bill.objects.get(pk=id)
        form = BillForm(request.POST, instance=pi)
        if form.is_valid():
            form.save()
    else:
        pi = Bill.objects.get(pk=id)
        form = BillForm(instance=pi)
    return render(request, 'update.html', {'form':form})
# def updateView(request,id):
#     bill = Bill.objects.filter(id = id)
#     template = loader.get_template('bill-form.html')
#     return HttpResponse(template.render(request))

    # return redirect('index')

# Html to pdf view
@csrf_protect 
def pdf(request, id):
    bill = Reexp.objects.filter(id =id)
    return Render.render('bill.html', {'bill':bill})

#Html to exp_pdf view
@csrf_protect 
def exp_pdf(request, id):
    bill = Reexp.objects.filter(id =id)
    return Render.render('exp.html', {'bill':bill})

# html to offer view
@csrf_protect 
def offer_pdf(request, id):
    bill = Bill.objects.filter(id =id)
    return Render.render('offer.html', {'bill':bill})
 
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from django.core.mail import EmailMessage

from django.conf import settings
from .forms import EmailForm, RelivingEmailForm

class EmailAttachementView(View):
    form_class = EmailForm
    template_name = 'emailattachment.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'email_form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            
            
           
            email = form.cleaned_data['email']
            files = request.FILES.getlist('attach')

            try:
                mail = EmailMessage('INTERSHIP LETTER', 'Dear ,\n Greetings from Shivila Technologies.\n Hereby attached your Internship letter. \n Please sign and sent back To:- hr@shivila.com in CC :- recruiting@shivila.com at before the joining date. \n All the best.',
                settings.EMAIL_HOST_USER, [email])
                for f in files:
                    mail.attach(f.name, f.read(), f.content_type)
                mail.send()
                return render(request, self.template_name, {'email_form': form, 'error_message': 'Sent email to %s'%email})
            except:
                return render(request, self.template_name, {'email_form': form, 'error_message': 'Either the attachment is too big or corrupt'})

        return render(request, self.template_name, {'email_form': form, 'error_message': 'Unable to send email. Please try again later'})

class GeneratePdfView(View): 
    def get(self, request):
        bill = Bill.objects.filter(id =id)
        params ={
            'bill' : bill
        }
        file_name , status = Render(params)

        if not status:
            return HttpResponse({'status' : 400})

        return HttpResponse({'status': 200 , 'path' : f'/media/{file_name}.pdf'})

def sendemaildirect(request, id):
    form_class = EmailForm
    rejected =Rejected.objects.get(id=id)
    template_name = ('sendmail.html',{'email':rejected.employee_email})
    send_mail(
        'Thank for your Interest', 
        'waiting for format', 
        settings.EMAIL_HOST_USER, 
        [rejected.employee_email]
    )
    fail_silently = False
    messages.info(request, "Mail send successfully .")
    return redirect('success')    

@csrf_protect 
def directmailView(request):
    if request.method == 'POST':
        form = RejectedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = RejectedForm()
    return render(request, 'direct-form.html', {'form':form})

def success(request):
    bill = Rejected.objects.all().order_by('-date')
    return render(request, 'success.html', {'bill': bill})

def delete(request,id):
    bill = Rejected.objects.get(id = id)
    bill.delete()
    return redirect('success')

def export_data_excel(request):
    bill = Bill.objects.all()
    data= []
    
    for bills in bill:
        data.append({
            "employee_id": bills.employee_id,
            "employee_email": bills.employee_email,
            "employee_name": bills.employee_name,
            "job_type": bills.job_type,
            "designation": bills.designation,
            "joindate": bills.joindate,
            "date": bills.date

        })

    pd.DataFrame(data).to_excel('employee_list.xlsx')
    return redirect('index')

from .forms import LinkMail

@csrf_protect  
def linkemail(request, id):
    sub = forms.LinkMail()
    bill=Bill.objects.get(id=id)
    template_name = ('msg.html', {'email':bill.employee_email})
    if request.method == 'POST':
        sub = forms.LinkMail(request.POST)
        subject = 'Team joining Link'
        recepient = str(sub['message'].value())
        [bill.employee_email]
        send_mail(subject, recepient, settings.EMAIL_HOST_USER,[bill.employee_email], fail_silently = False)
        messages.info(request, "Link send successfully .")
        # return redirect('index')
    return render(request, 'link.html', {'form':sub, 'error_message': 'Link send Successfully'})


# def attachpdf(request, id):
#     form = EmailForm
#     bill=Bill.objects.get(id=id)
#     template_name = ('offerattachmail.html',{'email_form':bill.employee_email})
    
#     if form.is_valid():
#         files = request.FILES.getlist('attach')
#     # email.attach_file("pdf/static/upload/user.pdf")
#         try:
#             email = EmailMessage('Intership Letter', 'Dear ,\n Greetings from Shivila Technologies.\n Hereby attached your Internship letter. \n Please sign and sent back To:- hr@shivila.com in CC :- recruiting@shivila.com at before the joining date. \n All the best.', 
#                 settings.EMAIL_HOST_USER, 
#                 [bill.employee_email]
#             )
#             fail_silently = False
#             for f in files:
#                 email.attach_file(f.name, f.read(), f.content_type)
#             email.send()
#             return render(request, template_name, {'email_form':form, 'error_message': 'Sent email succesfully'})
#         except:
#             return render(request, template_name, {'email_form': form, 'error_message': 'Either the attachment is too big or corrupt'})

class RelivingEmailAttachementView(View):
    form_class = RelivingEmailForm
    template_name = 'relivingemailattachment.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'relivingemail_form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            
           
           
            email = form.cleaned_data['email']
            files = request.FILES.getlist('attach')

            try:
                mail = EmailMessage('RELIVING LETTER', 'Greetings from Shivila Technologies.\n Hereby attached your Internship letter. \n Please sign and sent back To:- hr@shivila.com in CC :- recruiting@shivila.com at before the joining date. \n All the best.',
                settings.EMAIL_HOST_USER, [email])
                for f in files:
                    mail.attach(f.name, f.read(), f.content_type)
                mail.send()
                return render(request, self.template_name, {'relivingemail_form': form, 'error_message': 'Sent email to %s'%email})
            except:
                return render(request, self.template_name, {'relivingemail_form': form, 'error_message': 'Either the attachment is too big or corrupt'})

        return render(request, self.template_name, {'relivingemail_form': form, 'error_message': 'Unable to send email. Please try again later'})

def SearchView(request):
    if request.method == 'GET':
        query= request.GET.get('q')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups= Q(id__icontains=query) |  Q(employee_name__icontains=query) | Q(employee_email__icontains=query)| Q(date__icontains=query)| Q(designation__icontains=query)| Q(job_type__icontains=query)| Q(joindate__icontains=query)
            results= Bill.objects.filter(lookups).distinct()
            context={'results': results,
                     'submitbutton': submitbutton}
            return render(request, 'base.html', context)
        else:
            return render(request, 'base.html')
    else:
        return render(request, 'base.html')
    
@csrf_protect 
def reexpView(request):
    if request.method == 'POST':
        form = ReexpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reexp')
    else:
        form = ReexpForm()
    return render(request, 'reexp_form.html', {'form':form})

def reexp(request):
    bill = Reexp.objects.all().order_by('-date')
    return render(request, 'reexp.html', {'bill': bill})


def employeeSearchView(request):
    if request.method == 'GET':
        querys= request.GET.get('q')
        submitbuttons= request.GET.get('submit')
        if querys is not None:
            lookup= Q(id__icontains=querys) |  Q(employee_name__icontains=querys) | Q(employee_email__icontains=querys)| Q(date__icontains=querys)| Q(designation__icontains=querys)| Q(job_type__icontains=querys)| Q(resignationdate__icontains=querys)| Q(job_type__icontains=querys)| Q(joindate__icontains=querys)
            result= Reexp.objects.filter(lookup).distinct()
            contexts={'result': result,
                     'submitbuttons': submitbuttons}
            return render(request, 'login.html', contexts)
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


# Password Reset 

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'official_letter',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})