from django.shortcuts import render
from myapp.forms import UserForm,UserProfileInfoForm

#This is for login
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request,'myapp/index.html')

def special(request):
    return render(request,'myapp/special.html')

@login_required #This decorators used for who logged in only are logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered =False

    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user #this is for onetoone relationship bw User model and UserProfileInfo model

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered =True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'myapp/register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('special'))

            else:
                return HttpResponse('Account not active!!')

        else:
            print('Someone tried to login and failed')
            print("Username : {} and Password {}".format(username,password))
            return HttpResponse("<center><h1>You are not user!!</h1></center>")

    else:
        return render(request,'myapp/user_login.html')
