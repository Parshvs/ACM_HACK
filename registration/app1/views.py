from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
import pyrebase
from twilio.rest import Client
import os


firebaseConfig = {
  "apiKey": "AIzaSyB-YlDEnwxFcRQy1ZQXTW0SnMis1SAPkoI",
  "authDomain": "line-free-c2f74.firebaseapp.com",
  "databaseURL": "https://line-free-c2f74-default-rtdb.firebaseio.com",
  "projectId": "line-free-c2f74",
  "storageBucket": "line-free-c2f74.appspot.com",
  "messagingSenderId": "608412692251",
  "appId": "1:608412692251:web:affdb3d208b921c2532dbe",
  "measurementId": "G-F8J0WQV9CT"
};

firebase=pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
database=firebase.database()

account_sid = "ACf95cdc07f743776becee6c4b1e84c0a1"
auth_token = "45ea1712c709c5fec13f4e4f2f8fb787"
client = Client(account_sid, auth_token)

queue = database.child("queue").get()

if not queue.val():
    database.child("queue").set({"Enteries": []})

# Create your views here.
# @login_required(login_url='login')
def HomePage(request):

    return render(request,'home.html')

def SignUpPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        if pass1!=pass2:
            return HttpResponse("Pass1 and Pass2 are Not Same please enter correct password")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    else:
        return render (request,'signup.html') 

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            HttpResponse("UserName or password is Incorrect")
    return render(request,'login.html')

def LogOut(request):
    # logout(request)
    return redirect('login')


def user_login(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        mob=request.POST.get('mobile')
        reason=request.POST.get('reason')
        token = database.child("token").get().val()
        token += 1
        database.child("token").set(token)

        current_time = datetime.now().strftime("%H:%M:%S")
        data = {
            'username': uname,
            'mobile': mob,
            'reason': reason,
            'token': token,
            'Register_time': current_time,
        }
        no='+91'+mob
        # tt="token = "+token
        new_node_ref = database.child('queue').child('Enteries').child(str(token))
        new_node_ref.set(data)
        message = client.messages.create(body='Track your queue status here:\nUsername:'+mob+'\nPassword:'+str(token)+'\nWebsite: https://linefree.com',to=no, from_='+15076235870')
        print(message.sid)
        #display all elements
        # queue = database.child("queue").child("Enteries").get()
        # if queue.val():
        #     print(queue.val())

        return redirect('index')
    else:
        
        return render(request,'user_register.html')