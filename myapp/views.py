from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
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
    if request.user.is_authenticated:
        return redirect('dashboard')

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
                messages.error(request, 'Invalid username or password.')
    else:
        fm = AuthenticationForm()

    return render(request, "login.html", {'form': fm})


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    show_contact = ""
    list = Contact.objects.filter(user=request.user)
    if Request.objects.filter(accept_request=True, request_sender=request.user.id).exists():
        request_data = Request.objects.filter(accept_request=True, request_sender=request.user.id).values_list(
            "request_receiver", flat=True)
        show_contact = Contact.objects.filter(user__in=request_data)

    return render(request, 'dashboard.html', {'list': list, 'show_contact': show_contact})


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


def user_logout(request):
        if request.user.is_authenticated:
            auth_logout(request)
            messages.success(request, 'You have been logged out successfully.')
        return redirect('login')


def request_user(request):
    user = User.objects.exclude(id=request.user.id)
    user_request = Request.objects.filter(request_receiver=request.user.id)
    return render(request, 'request.html', {'user': user, 'user_request': user_request})


def sendrequest(request, id):
    sender = request.user
    receiver = User.objects.get(id=id)
    if Request.objects.filter(request_sender=sender, request_receiver=receiver):
        messages.success(request, 'Your request was already sent')
        print(request.user.id)
    else:
        Request.objects.create(request_sender=sender, request_receiver=receiver)
        messages.success(request, 'Your request sent successfully')
    return redirect('request_user')


def acceptrequest(request, id):
    r = Request.objects.get(id=id)
    if r.request_receiver == request.user:
        r.accept_request = True
        r.save()
        messages.success(request, 'Your request has been accepted')
    else:
        messages.success(request, 'You cannot accept request')
    return redirect('request_user')


def declinerequest(request, id):
    r = Request.objects.get(id=id)
    if r.request_receiver == request.user:
        r.accept_request = False
        r.save()
        messages.success(request, 'Your request has been declined')
    else:
        messages.success(request, 'You cannot decline request')
    return redirect('request_user')
