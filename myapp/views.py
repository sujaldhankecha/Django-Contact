from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from myapp.forms import RegisterForm, ContactForm
from .models import Contact, User, Request


# Create your views here.


def register(request):
    if request.method == 'POST':
        fm = RegisterForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        fm = RegisterForm()
    return render(request, 'registration.html', {'form': fm})


def login(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'You are now logged in!')
                return redirect('dashboard')
    else:
        fm = AuthenticationForm()
    return render(request, "login.html", {'form': fm})


def dashboard(request):
    if request.user.is_authenticated:
        list = Contact.objects.filter(user=request.user)
        return render(request, 'dashboard.html', {'list': list})
    else:
        return redirect('login')


def addcontact(request):
    if request.method == 'POST':
        fm = ContactForm(request.POST)
        if fm.is_valid():
            # data = fm.save()
            # ct = Contact.objects.get(id=data.id)
            # ct.user = request.user
            # ct.save()

            # Contact.objects.create(
            #     user=request.user,
            #     firstname=fm.cleaned_data['firstname'],
            #     lastname=fm.cleaned_data['lastname'],
            #     mobile=fm.cleaned_data['mobile'],
            #     email=fm.cleaned_data['email'],
            #     address=fm.cleaned_data['address'],
            # )

            contact = Contact(
                user=request.user,
                firstname=fm.cleaned_data['firstname'],
                lastname=fm.cleaned_data['lastname'],
                mobile=fm.cleaned_data['mobile'],
                email=fm.cleaned_data['email'],
                address=fm.cleaned_data['address'],
            )
            contact.save()

            messages.success(request, 'Contact added!')
            return redirect('dashboard')
    else:
        fm = ContactForm()
        return render(request, 'addcontact.html', {'form': fm})


def editcontact(request, id):
    if request.user.is_authenticated:
        contact = Contact.objects.get(pk=id)
        if request.method == 'POST':
            fm = ContactForm(request.POST, instance=contact)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Your information save successfully')
                return redirect('dashboard')
        else:
            fm = ContactForm(instance=contact)
        return render(request, 'editcontact.html', {'form': fm})
    else:
        messages.success(request, 'Your login is required for editing.')
        return redirect('login')


def deletecontact(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            contact = Contact.objects.get(pk=id)
            contact.delete()
            messages.success(request, 'Your contact deleted successfully')
        return redirect('dashboard')
    else:
        messages.success(request, 'login required for deleting')
        return redirect('login')


def logout(request):
    auth_logout(request)
    return redirect('dashboard')


def request_user(request):
    user = User.objects.exclude(id=request.user.id)
    user_request = Request.objects.all()
    return render(request, 'request.html', {'user': user,'user_request': user_request})


def sendrequest(request, id):
        sender = request.user
        receiver = User.objects.get(id=id)
        Request.objects.create(request_sender=sender, request_receiver=receiver)
        messages.success(request, 'Your request sent successfully')
        return redirect('request_user')

def acceptrequest(request, id):
    request = Request.objects.get(id=id)
    request.accept_request = 'true'
    request.save()
    user = User.objects.exclude(id=request.user.id)
    return render(request, 'request.html', {'user': user})
