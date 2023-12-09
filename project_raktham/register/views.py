from django.shortcuts import render,redirect,HttpResponse
from .forms import regist_form
from .models import user_registration,acceptor,donor
import random
from django.views.decorators.cache import cache_control
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from datetime import datetime, timedelta

is_logged_in=False
seek1_completed=False

    
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def home(request): 
    return render(request, 'register/home.html',{'is_logged_in':is_logged_in})

def update(request):
    pass       
def donate(request):
    if is_logged_in:
        if request.method=="POST":
            name=request.POST['name']
            age=request.POST['age']
            sex=request.POST['sex']
            mobile=request.POST['mobile']
            blood_grp=request.POST['blood_type']
            email=request.POST['email']
            address=request.POST['address']
            health=request.POST['health_status']
            date=request.POST['date']
            if request.POST['consent'] is not None:
                consent=True

            user_profile =donor.objects.create(name=name,age=age,sex=sex,email=email,mobile=mobile,
                                                  address=address,blood_group=blood_grp,health_status=health,last_donated=date,agree=consent)
            return HttpResponse('Tnx mowa donation form fill chesinanduku ....')
        
        else:
            return render(request,'register/donor.html',{'is_logged_in':is_logged_in})
    else:
        return redirect('home')

def logout(request):
    global is_logged_in
    is_logged_in=False
    return redirect('home')

def seek1(request): 
    if is_logged_in:
        if request.method=="POST":
            request.session['name']=request.POST['name']
            request.session['age']=request.POST['age']
            request.session['sex']=request.POST['sex']
            request.session['email']=request.POST['email']
            request.session['mobile']=request.POST['mobile']
            global seek1_completed
            seek1_completed=True
            return redirect('seek2')
        else:
            return render(request,'register/acceptor1.html',{'is_logged_in':is_logged_in})
    else:
        return redirect('home')
    
def seek2(request):
    if is_logged_in and seek1_completed:
        if request.method=="POST":
            hospital=request.POST['hospital']
            address=request.POST['address']
            emerg=request.POST['emergency']
            blood_grp=request.POST['blood_type']
            component=request.POST['component']
            units=request.POST['units']
            date=request.POST['date']
            if request.POST['consent'] is not None:
                consent=True
            name=request.session.get('name')
            age=request.session.get('age')
            sex=request.session.get('sex')
            mail=request.session.get('email')
            mobile=request.session.get('mobile')

            user_profile =acceptor.objects.create(name=name,age=age,sex=sex,email=mail,mobile=mobile,
                                                  hospital_name=hospital,hospital_address=address,emergency=emerg,
                                                  blood_group=blood_grp,blood_type=component,required_by=date,units=units,agree=consent)
            
            date_50_days_ago = datetime.now() - timedelta(days=50)


            today = datetime.now().date()

            
            records=donor.objects.filter(blood_group=blood_grp,last_donated__lt=date_50_days_ago)
           
            global recipient_list
            recipient_list = [] 
            
            for don in records: 
                print(don.last_donated)
                recipient_list.append(don.email)
                
            global message
            message = f'''patient name : {name}
                            Hospital name :{hospital}
                            Hospital address : {address}
                            blood Group: {blood_grp}
                            type :{component}
                            units : {units}
                            required_on:{date}
                            email : {mail}
                            contact number : {mobile}'''
            return redirect('seek_submit')
        else:
            return render(request,'register/acceptor2.html',{'is_logged_in':is_logged_in})
    else:
        return redirect('home')


    
def seek_submit(request):  
    if request.method=="POST":
        subject = 'Request for blood donation'
        from_email = 'lingareddydanda098@gmail.com' 
        send_mail(subject, message, from_email, recipient_list)
        return redirect('home')
    else:
        return render(request,'register/seek_submit.html')


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def verify(request):
    if request.method == 'POST':
        otp_entered=request.POST['otp']
        mail=request.session.get('email')
        user_profile = user_registration.objects.get(email=mail)
        print(otp_entered , user_profile.otp)
        if str(otp_entered) == str(user_profile.otp):
            print("Verified Sucessfully") 
            user_registration.objects.filter(email=mail).update(isVerified=True)
            return redirect('login')
        else:
            print("Invalid OTP")
            
    return render(request, 'register/verify.html')

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def login(request):
    if request.method == 'POST':
        mail=request.POST['email']
        passw=request.POST['password']
        user = authenticate(request, email=mail, password=passw)
        if user is not None:
            print("sucessful")
        if request.user.is_authenticated:
            print("user login ayyadu ra")
        if user_registration.objects.filter(email=mail).exists() and (user_registration.objects.get(email=mail).isVerified==True):
            hash_pass=user_registration.objects.get(email=mail).password   
            if check_password(passw,hash_pass):
                print("Login succesful")
                messages.success(request, 'Login Successful')  
                global is_logged_in
                is_logged_in=True
                return redirect('home')
            else:
                messages.success(request, 'Invalid Password')
        else:
            print('Email not registered')
            return redirect('login')
    return render(request,'register/login.html')

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def regist(request):
    if request.method == 'POST':
        form = regist_form(request.POST)
        if form.is_valid():
            cleaned_data=form.cleaned_data
            username=cleaned_data['username']
            mail=cleaned_data['email']
            passw = make_password(cleaned_data['password'])
            print("mail : ",mail)  
            if user_registration.objects.filter(email=mail).exists() and (user_registration.objects.get(email=mail).isVerified==True):
                print("Email already registered please Login")
                return render(request,'register/login.html')
            
            elif user_registration.objects.filter(email=mail).exists(): 
                print(f" Dear {username} Email already registered please verify the access code")
                request.session['email'] =mail 
           
            else:    
                ot=random.randint(1000,10000)
                user_profile =user_registration.objects.create(username=username, email=mail,password=passw, otp=ot)
                sender="lingareddydanda098@gmail.com"
                receiver=[mail]
                send_mail("Verification Mail",f" Dear {username}/nAccess code for Email Verification : {ot}",sender,receiver)
                print("New user saved successfully") 
                request.session['email'] =mail 
            return redirect('verify')

    else:
        form = regist_form()

    return render(request, 'register/register.html', {'form': form})
