from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm, RegisterForm, ResetPWDForm, ProfileForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.shortcuts import render
from django.views import View
from .models import Staff
import requests
import random
import string
import re

# Create your views here.

# Login
class LoginView(View):
    def get(self, request):
        # If session has value
        if request.session.get('login'):
            # If session has role seller so if condition true otherwise else.
            if request.session.get('role') == 'Seller':
                return HttpResponseRedirect('seller/dashboard/')
            else:
                return HttpResponseRedirect('owner/dashboard/')

        # Create form.
        login_form = LoginForm(auto_id=True)
        return render(request, 'staff/login.html', {'loginForm':login_form})

    def post(self, request):
        try:
            # attach form from post method
            login_form = LoginForm(request.POST, auto_id=True)

            # Validate form
            if login_form.is_valid():
                # Get data from form.
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']

                # User login check
                table_password = Staff.objects.get(username=username, deleted_at=True)
                user = check_password(password, table_password.password)

                # Login attempt
                if user == False:
                    if table_password.login_attempt < 5:
                        increaseAttempt = table_password.login_attempt + 1
                        attemptUpdate = Staff.objects.filter(username=username).update(login_attempt = increaseAttempt)
                        msg_info = f"Your attempt is remains {4 - table_password.login_attempt}"
                        messages.error(request, msg_info)

                    else:
                        resetPassword = Staff.objects.filter(username=username).update(pwd_reset = 0, password='')
                        messages.error(request, 'You are blocked now! Please contact owner for new password.')

                # If user is exist render the password reset form
                if user: 
                    request.session['name']      =  table_password.first_name
                    request.session['email']     =  table_password.email
                    request.session['role']      =  table_password.user_role
                    request.session['login']     =  True
                    # If user under 5 attempts use write username password so reset login_attempt from 0
                    if table_password.login_attempt > 0:
                        attemptUpdate = Staff.objects.filter(username=username).update(login_attempt = 0)

                    if table_password.pwd_reset == False:
                        # Create url for redirecting page with data                        
                        url = f'/reset/?email={table_password.email}'

                        # url = '/reset/?email={}'.format(table_password.email)
                        return HttpResponseRedirect(url)
                    
                    elif table_password.user_role == 'Owner':
                        request.session['last_name'] =  table_password.last_name
                        request.session['img']       =  table_password.profile_img.url
                        return HttpResponseRedirect('owner/dashboard/')

                    else:
                        request.session['last_name'] =  table_password.last_name
                        request.session['img']       =  table_password.profile_img.url
                        return HttpResponseRedirect('seller/workbench/')
                else:
                    messages.error(request, 'Staff removed doesn\'t exit.')
                    return HttpResponseRedirect('/')
                              
        except Exception as e:
            print(e)
            messages.error(request, e)
            return HttpResponseRedirect('/')
        
        return render(request, 'staff/login.html', {'loginForm': login_form})
    
# User registration using default django system
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm(auto_id=True)
        return render(request, 'staff/register.html', {'register_form':register_form})
    
    def post(self, request):
        try:
            register_form = RegisterForm(request.POST, auto_id=True)
            if register_form.is_valid():
                name = register_form.cleaned_data['first_name']
                email = register_form.cleaned_data['email']
                user_role = register_form.cleaned_data['user_role']
                
                # Create Username and Password
                underscoreName = re.sub(' ', '_', name)
                username = underscoreName.lower() + '_' +str(random.randint(0, 999))
                password = '' . join(random.sample((string.ascii_uppercase + string.digits), 8))

                # Convert password in hash (sha1)
                hash_password = make_password(password)

                # Save all data in database
                new_user = Staff.objects.create(first_name = name, email = email, username=username, password = hash_password, user_role = user_role)

                # Send email
                subject = 'Username and Password here...'
                msg = f'''
                    <table border='2'>
                        <tr>
                            <th>Username</th>
                            <td>{username}</td>
                        </tr>
                        <tr>
                            <th>Password</th><td>{password}</td>
                        </tr>
                    </table>
                '''
                email_from = 'mohitmishra.falna850@yahoo.com'
                to = email

                user_msg = EmailMultiAlternatives(subject, msg, email_from, [to])
                user_msg.content_subtype = 'html'
                user_msg.send()
                return HttpResponseRedirect('/owner/dashboard/')

        except Exception as e:
            print(e)
            messages.error(request, e)
            return HttpResponseRedirect('/register/')
        
        return render(request, 'staff/register.html', {'register_form':register_form})

# Reset Password
class ResetPassword(View):
    def get(self, request):
        # It get value from url bar
        email = request.GET.get('email')

        # Set input fields value tag using initial method it takes dictionary
        resetForm = ResetPWDForm(auto_id=True, initial={'email':email})
        return render(request, 'staff/reset_password.html', {'resetForm':resetForm})

    def post(self, request):        
        try:
            resetForm = ResetPWDForm(request.POST, auto_id=True)
        
            if resetForm.is_valid():
                email = resetForm.cleaned_data['email']
                newPassword = resetForm.cleaned_data['password']

                hash_password = make_password(newPassword)
                
                updatePassword = Staff.objects.filter(email=email).update(password=hash_password, pwd_reset=1)
                
                if updatePassword:
                    userData = Staff.objects.get(email=email)
                    print(userData.last_name)
                    if not userData.last_name:
                        url = '/profile/?email={}'.format(email)
                        return HttpResponseRedirect(url)
                    
                    if request.session.get('login') == True:
                        del request.session['name']
                        del request.session['email']
                        del request.session['role']
                        del request.session['login']
                        return HttpResponseRedirect('/')
        except Exception as e:
            print(e)
            messages.error(request, e)
            return HttpResponseRedirect('/reset/')
        return render(request, 'staff/reset_password.html', {'resetForm':resetForm})
    

# Profile details
class ProfileView(View):
    def get(self, request, eml=None):

        # If user coming from completed login process so email value set by the request.GET.get method
        # and If user coming from the clicking link so email value set by eml variable.
        if eml is None:
            email = request.GET.get('email')
        else:
            email = eml

        userData = Staff.objects.get(email=email)
        profileForm = ProfileForm(auto_id=True, 
        initial={
        'first_name':userData.first_name,
        'last_name':userData.last_name,
        'email':userData.email,
        'username':userData.username,
        'about_user':userData.about_user,
        # 'dob':userData.dob,
        'mobile':userData.mobile,
        'gender':userData.gender,
        'profile_img':userData.profile_img,
        'pincode':userData.pincode,
        'dist':userData.dist,
        'state':userData.state,
        'country':userData.country
    })
        profileForm.fields['city'].choices = [userData.city]
       
        return render(request, 'staff/profile.html', {'profileForm':profileForm, 'userData':userData})

    def post(self, request, eml=None):

        if eml is None:
            email = request.GET.get('email')
        else:
            email = eml

        updateUser = Staff.objects.get(email=email)
        profileForm = ProfileForm(request.POST, request.FILES, auto_id=True)
        try:
            if profileForm.is_valid():
                updateUser.first_name = profileForm.cleaned_data['first_name']
                updateUser.last_name = profileForm.cleaned_data['last_name']
                updateUser.about_user = profileForm.cleaned_data['about_user']
                updateUser.dob = profileForm.cleaned_data['dob']
                updateUser.profile_img = profileForm.files['profile_img']
                updateUser.mobile = profileForm.cleaned_data['mobile']
                updateUser.gender = profileForm.cleaned_data['gender']
                updateUser.pincode = profileForm.cleaned_data['pincode']
                updateUser.city = profileForm.cleaned_data['city']
                updateUser.dist = profileForm.cleaned_data['dist']
                updateUser.state = profileForm.cleaned_data['state']
                updateUser.country = profileForm.cleaned_data['country']

                # If we want to update image so its compulsory to use save() method
                updateUser.save()

                # After profile data uploaded session delete.
                if request.session.get('login') == True:
                    del request.session['name']
                    del request.session['email']
                    del request.session['role']
                    del request.session['login']
                    return HttpResponseRedirect('/')

                # updateUser = Staff.objects.filter(email=email).update(
                #     first_name = first_name, last_name = last_name, about_user = about_user, dob = dob, mobile = mobile, gender = gender, profile_img = profile_img, pincode = pincode, city = city, dist = dist, state = state, country = country 
                # )

        except Exception as e:
            print(e)
            return render(request, 'staff/profile.html', {'profileForm':profileForm})
        return render(request, 'staff/profile.html', {'profileForm':profileForm})
        
# Get address usig postal api
def getAddress(request):
    pincode = request.POST.get('pincode')
    try:
        sendData = "http://postalpincode.in/api/pincode/" + pincode
        postalAddress = requests.get(sendData)
    except Exception as e:
        print(e)
        return HttpResponse(e)
    return HttpResponse(postalAddress)

# Logout
def logout(request):
    try:
        if request.session.get('login') == True:
           del request.session['name']
           del request.session['last_name']
           del request.session['email']
           del request.session['role']
           del request.session['img']
           del request.session['login']
        messages.success(request, "Logout Successfully.")
    except Exception as e:
        print(e)
    return HttpResponseRedirect('/')