from django.shortcuts import render, HttpResponse, redirect
from home.models import Convocation
from home.models import Contact
from home.models import eventlike
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from events.models import Post
from datetime import datetime
from django.http import JsonResponse
import json
import base64

# Create your views here.
def home(request):
    return render(request, 'home/home.html') 

def about(request): 
    return render(request, 'home/about.html') 

def contact(request): 
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
        
    return render(request, 'home/contact.html') 

def convocation(request): 
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        batchcourse = request.POST['batchcourse']
        phone = request.POST['phone']
        attendstatus = request.POST['attendstatus']
        currentwork = request.POST['currentwork']
        print(name, email, phone, currentwork, batchcourse, attendstatus)

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(currentwork)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            convocation = Convocation(name=name, email=email, phone=phone, currentwork=currentwork, batchcourse=batchcourse, attendstatus=attendstatus)
            convocation.save()
            messages.success(request, "Your update has been successfully sent")
        
    return render(request, 'home/convocation.html') 


def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = Post.objects.none() 
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    
    if allPosts.count() == 0:
         messages.warning(request, "No search results found. Please refine your query")
    params = {'allPosts': allPosts, 'query':query}
    return render(request, 'home/search.html', params) 

def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        print(fname)
        # Check for errorneous inputs
        # username should be under 10 characters
        if len(username) > 15:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')
        
        # username should be alphanumeric
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('home')

        # passwords should match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')

        # Create the user 
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your Academic director account has been successfully created")
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home') 
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')
            
    return HttpResponse('404 - Not Found')

def CreateNewPost(request):
    if request.method == "POST":
        image =request.FILES['imagefile']
        convertedimage = base64.b64encode(image.read())
        title=request.POST.get('title')
        tools=request.POST.get('tools')
        eventtype=request.POST.get('eventtype')
        content=request.POST.get('content')
        user=request.user
        #print(title)
        print(eventtype)
        convertedimage="data:image/jpeg;base64,"+ str(convertedimage.decode("utf-8"))

        entry = Post(eventtype=eventtype, tools=tools,title=title,content=content,eventimage=convertedimage,author=request.user,slug=title,timeStamp=datetime.now())
        entry.save()
        messages.success(request, "Your Artwork has been posted successfully")
        return redirect('/events')
        


def handleLogout(request): 
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home') 

def MyProfile(request,username): 
    user=username
    userdetail=User.objects.filter(username=user).first()
    print(userdetail.username)
    allPosts = Post.objects.filter(author=user).all()
    if userdetail.username==request.user:
        is_myprofile=True
    else:
        is_myprofile=False
    #allPosts= Post.objects.all()
    #is_home_page=True
    context={'allPosts': allPosts, "userdetail":userdetail, "is_myprofile":is_myprofile }
    return render(request, 'home/myprofile.html', context) 

def LikePost(request): 
    received_json_data=json.loads(request.body)
    
    validate=eventlike.objects.filter(srno=received_json_data["srno"],user=request.user).count()
    print("total count is ",validate)
    
    if validate==0:
        #allow to like
        post=Post.objects.filter(sno=received_json_data["srno"]).first()
        post.totallikes= post.totallikes +1
        post.save()
        add=eventlike(srno=received_json_data["srno"],user=request.user)
        add.save()
        print(received_json_data["srno"],request.user)
        return JsonResponse({'totallikes':post.totallikes})    
    else :
        #deacrease the like and remove user from artlike table
        post=Post.objects.filter(sno=received_json_data["srno"]).first()
        post.totallikes= post.totallikes -1
        post.save()
        add=eventlike.objects.filter(srno=received_json_data["srno"],user=request.user).delete()
       
        return JsonResponse({'totallikes':post.totallikes})    
   

def deletepost(request): 
    received_json_data=json.loads(request.body)  
    delete=Post.objects.filter(sno=received_json_data["srno"], author=request.user).delete()
    print("deleting post " , received_json_data["srno"])
    return JsonResponse({'msg':"deleted "})    

def typeprofile(request, type): 
    eventtype=request.POST.get('eventtype')
    return type
    allPosts = Post.objects.filter(arttype=request.a).all()
    #allPosts= Post.objects.all()
    #is_home_page=True
    context={'allPosts': allPosts }
    return render(request, 'home/myprofile.html', context) 
    