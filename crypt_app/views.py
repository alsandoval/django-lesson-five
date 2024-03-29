from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm

#Login libraries and decorators
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'crypt_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

def registration(request):
    
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() & profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
             
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    
    context_dict = {'user_form':user_form, 'profile_form':profile_form,'registered':registered}
    
    return render(request,'crypt_app/registration.html',context_dict)

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username') # 'username' from login.html
        password = request.POST.get('password') # 'password' from login.html

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print('Someone tried to login and failed!')
            print(f'Username: {username} and password: {password}')
            return HttpResponse('Invalid login details submitted.')
    else:
        return render(request,'crypt_app/user_login.html',{})