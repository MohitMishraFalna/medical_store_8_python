# SED means Search, Edit, Delete activity is here.
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.views import View
import random
import string
import json

class AllSearchEditDelete(View):

    # Delete search
    def delete(request, model_name = None):
        try:            
            updateStaff = model_name.objects.filter(id=request.GET.get('id')).update(deleted_at = 0)
            if updateStaff:
                result = messages.success(request, "Item deleted succussfully.")
        except Exception as e:
            print(e)
            result = messages.error(request, e)
        return result
        
    # Edit method
    def edit(request, model_name = None):
        try:
            updateStaff = model_name.objects.filter(id=request.POST.get('dep_id')).update(name=request.POST.get('name'))
            if updateStaff:
                messages.success(request, "Item updated succussfully.")
        except Exception as e:
            print(e)
            messages.error(request, e)

    # Staff search
    def search(request, model_name = None):
        try:
            search_item = request.GET.get('search_Item')
            staff_list = model_name.objects.filter(first_name__icontains = search_item) | model_name.objects.filter(email__icontains=search_item) | model_name.objects.filter(mobile__contains=search_item)
            response = []
            if staff_list:
                for staff in staff_list:
                    response.append({'id': staff.id, 'first_name': staff.first_name,'email': staff.email,'username': staff.username,'mobile': staff.mobile,'user_role': staff.user_role,'pwd_reset': staff.pwd_reset,'login_attempt': staff.login_attempt,'deleted_at': staff.deleted_at,  })             
                response = json.dumps({'response':response}, default=str)
        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong.')   
        return response     

    # Set new password and send email
    def new_password(request, model_name=None):
        try:
            eml = request.GET.get('eml')
            username = request.GET.get('username')
            password = '' . join(random.sample((string.ascii_uppercase + string.digits), 8))

            # Convert password in hash (sha1)
            hash_password = make_password(password)

            # Save all data in database
            new_user = model_name.objects.filter(email = eml).update(password = hash_password, login_attempt=0)

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
            to = eml

            user_msg = EmailMultiAlternatives(subject, msg, email_from, [to])
            user_msg.content_subtype = 'html'
            user_msg.send()
            messages.success(request, 'Password generate. Please check email.')
        except Exception as e:
            print(e)
            messages.error(request, e)

    # Doctor Update
    def doctor_update(request, model_name=None):
        updateDoctor = model_name.objects.filter(id=request.POST.get('hid_id'))
        update = updateDoctor.update(name = request.POST.get('name'), email =request.POST.get('email'), mobile = request.POST.get('mobile'), department = request.POST.get('department'))
        if update:
            messages.success(request, 'Doctor update successfully.')

    # Product Update
    def product_update(request, model_name=None):
        update_product = model_name.objects.filter(id=request.POST.get('pro_id'))
        update = update_product.update(name = request.POST.get('name'), amt =request.POST.get('amt'), quantity = request.POST.get('quantity'), manufacturing = request.POST.get('manufacturing'), expiry = request.POST.get('expiry'), department = request.POST.get('department'))
        if update:
            messages.success(request, 'Product update successfully.')

