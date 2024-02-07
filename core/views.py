from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='signin')
def index(request):
    return render(request,"index.html")

def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info("User with this Email already exists..")
                return redirect('signup')
            elif(User.objects.filter(username=username)):
                messages.info("Username already exists..")
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                
                user_login = auth.authenticate(username = username,password=password)
                auth.login(request,user_login)
                
                user_model=User.objects.get(username=username)
                new_profile=Profile(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('setting')
                 
        else:
            messages.info("Password Mismatch")
            return redirect('signup')
            
        
    else:
        return render(request,'signup.html')


@login_required(login_url='signin')
def setting(request):
    return render(request,'setting.html')    

def signin(request):
    
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Credentials Invalid")
            return redirect('signin')
            
    else:
        return render(request,"signin.html")
    
@login_required(login_url='signin')    
def logout(request):
    auth.logout(request)
    return redirect('signin')