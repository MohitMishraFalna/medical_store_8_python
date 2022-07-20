from django.http import HttpResponse, HttpResponseRedirect
from .forms import AddDoctorForm, EditDoctorForm
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib import messages
from django.views import View
from .models import Doctor
import json

# Create your views here.
class DoctorView(View):
    # Get all deparment data and decorate by the pagination.
    def get(self, request):
        
        add_form = AddDoctorForm(auto_id=True)

        # pagination
        per_page = request.GET.get('selectPerPage')

        # If per_page value not coming so assign manualy
        if not per_page:
            per_page = 5

        # get data from the table
        doctors = Doctor.objects.all().order_by('id')

        # apply pagination
        paginator = Paginator(doctors, per_page)

        # get page number from url bar
        page_number = request.GET.get('page')

        # convert all doctor data to pagination object
        page_obj = paginator.get_page(page_number)

        # get all pages from pagination object
        total_pages = page_obj.paginator.num_pages

        # create compaharance list
        total_page_list = [n+1 for n in range(total_pages)]
        return render(request, 'doctor/new_doctor.html', {'add_form':add_form, 'doctors':page_obj, 'perPage':per_page, 'totalPages':total_pages, 'totalPageList':total_page_list})
    
    # Create doctor
    def post(self, request):
        add_form = AddDoctorForm(request.POST, auto_id=True)
        try:
            if add_form.is_valid():
                add_form.save()
                messages.success(request, 'Doctor create successfully.')
        except Exception as e:
            print(e)
            messages.error(request, e)
        return HttpResponseRedirect('/doctor/add/')

    # Get data and send django forms as ajax response
    def get_doctor_Data(request):
        get_doctor = Doctor.objects.get(id=request.GET.get('doc_id'))

        # Set initial value of django forms input and send as ajax respons
        # If you getting any type of error so use form_name.as_p() method.
        edit_form = EditDoctorForm(initial={'name':get_doctor.name, 'id':get_doctor.id, 'email':get_doctor.email, 'mobile':get_doctor.mobile, 'department':get_doctor.department}, auto_id=True)
        return HttpResponse(edit_form.as_p())

    # Edit method
    def edit(request):
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            department = request.POST.get('department')
            Doctor.objects.filter(id=request.POST.get('doc_id')).update(name=name, email=email, mobile=mobile, department=int(department))
            messages.success(request, "Doctor updated succussfully.")

        except Exception as e:
            print(e)
            messages.error(request, e)
        return HttpResponseRedirect('/doctor/add/')

    # Delete Method
    def delete(request):
        try:
            updateStaff = Doctor.objects.filter(id=request.GET.get('d_id')).update(deleted_at = 0)
            if updateStaff:
                messages.success(request, "Doctor deleted succussfully.")
        except Exception as e:
            print(e)
            messages.error(request, e)
        return HttpResponseRedirect('/doctor/add/')

    # doctor search
    def doctor_search(request):
        try:
            search_item = request.GET.get('search_Item')
            doctor_list = Doctor.objects.filter(name__icontains = search_item)
            response = []
            if doctor_list:
                for doctor in doctor_list:
                    response.append({'id':doctor.id, 'name': doctor.name, 'deleted_at': doctor.deleted_at})             
                response = json.dumps({'response':response}, default=str)
        except Exception as e:
            print(e)
            messages.error(request, e)
        return HttpResponse(response)

    