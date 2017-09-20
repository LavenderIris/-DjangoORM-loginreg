from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime, localtime
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'index.html')

def add_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        print "Fail!"
    else: 
        myrequest = request.POST

        # need to Bcrypt our password
        hash1 = bcrypt.hashpw( myrequest['pw'].encode('utf8') , bcrypt.gensalt())
        user = User.objects.create(first_name=myrequest['first_name'], last_name=myrequest['last_name'], email=myrequest['email'], pw=hash1 )
        user.save()
        return redirect('/success')

    return redirect('/')

def success(request):
    return render(request, 'success.html')

def login(request):
    if request.method == 'POST':
        myrequest = request.POST
        user = User.objects.filter(email=myrequest['email'])
        # if record not found
        if len(user) == 0:
            errors = {}
            errors['email_not_found'] = 'Email not found in our records'
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            # password on file
            hashed_pw = user[0].pw
            if bcrypt.checkpw( myrequest['pw'].encode('utf8'), hashed_pw.encode('utf8') )  :
                return redirect('/success')
            else:
                errors = {}
                errors['password_no_match'] = "Password doesn't match our records. Incorrect password."
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)

    return redirect('/')