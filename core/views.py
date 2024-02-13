from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile,Post
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='signin')
def index(request):
    user=User.objects.get(username=request.user.username)
    userPro=Profile.objects.get(user=user)

    posts=Post.objects.all()
    return render(request,"index.html",{'user_profile':userPro,'posts':posts})

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
def liked_post(request):
    pass

@login_required(login_url='signin')
def upload(request):
    if request.method=='POST':
       if request.FILES.get('post_upload'):
            image=request.FILES.get('post_upload')
            caption=request.POST['caption']
            username=request.user.username
            post_object=Post.objects.create(user=username,image=image,caption=caption)
            post_object.save()
            return redirect('/')
          
    else: 
        return redirect('/')


@login_required(login_url='signin')
def setting(request):
    user = Profile.objects.get(user=request.user)
    if request.method=='POST':
        image = request.FILES.get('profile_pic') if request.FILES.get('profile_pic') else user.profPic
        bio = request.POST['bio']
        location = request.POST['location']
        user.profPic=image
        user.bio=bio
        user.location=location
        user.save()

            
    return render(request,'setting.html',{"user":user})    

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