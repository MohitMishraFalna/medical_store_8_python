from django.http import HttpResponse, HttpResponseRedirect
from .forms import DepartmentAddForm, DepartmentEditForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render
from .models import Department
from django.views import View
import json

# Create your views here.
class DepartmentView(View):
    # Get all deparment data and decorate by the pagination.
    def get(self, request):
        
        add_form = DepartmentAddForm(auto_id=True)

        # pagination
        per_page = request.GET.get('selectPerPage')

        # If per_page value not coming so assign manualy
        if not per_page:
            per_page = 5

        # get data from the table
        departments = Department.objects.all().order_by('id')

        # apply pagination
        paginator = Paginator(departments, per_page)

        # get page number from url bar
        page_number = request.GET.get('page')

        # convert all department data to pagination object
        page_obj = paginator.get_page(page_number)

        # get all pages from pagination object
        total_pages = page_obj.paginator.num_pages

        # create compaharance list
        total_page_list = [n+1 for n in range(total_pages)]
        return render(request, 'department/new_department.html', {'add_form':add_form, 'departments':page_obj, 'perPage':per_page, 'totalPages':total_pages, 'totalPageList':total_page_list})
    
    # Create department
    def post(self, request):
        add_form = DepartmentAddForm(request.POST, auto_id=True)
        try:
            if add_form.is_valid():
                name = add_form.cleaned_data['name']
                new = Department.objects.create(name = name)
                print('res', new)
                if new:
                    messages.success(request, 'Department create successfully.')
                    return HttpResponseRedirect('/department/all_department/')
        except Exception as e:
            print(e)
            messages.error(request, e)
            return HttpResponseRedirect('/department/new_department/')
        return render(request, 'department/new_department.html', {'add_form':add_form})

    # Get data and send django forms as ajax response
    def get_department_Data(request):
        get_department = Department.objects.get(id=request.GET.get('dept_id'))
        
        # Set initial value of django forms input and send as ajax respons
        # If you getting any type of error so use form_name.as_p() method.
        edit_form = DepartmentEditForm(initial={'name':get_department.name, 'dep_id':get_department.id})

        return HttpResponse(edit_form)

    # Edit method
    def edit(request):
        try:
            updateStaff = Department.objects.filter(id=request.POST.get('dep_id')).update(name=request.POST.get('name'))
            if updateStaff:
                messages.success(request, "Department updated succussfully.")
        except Exception as e:
            print(e)
            messages.error(request, e)
        return HttpResponseRedirect('/department/new_department/')

    # Delete Method
    def delete(request):
        print(request.GET.get('d_id'))
        try:
            updateStaff = Department.objects.filter(id=request.GET.get('d_id')).update(deleted_at = 0)
            if updateStaff:
                messages.success(request, "Department deleted succussfully.")
        except Exception as e:
            print(e)
            messages.error(request, e)
        return HttpResponseRedirect('/department/new_department/')

    # Department search
    def department_search(request):
        try:
            search_item = request.GET.get('search_Item')
            department_list = Department.objects.filter(name__icontains = search_item)
            response = []
            if department_list:
                for department in department_list:
                    response.append({'id':department.id, 'name': department.name, 'deleted_at': department.deleted_at})             
                response = json.dumps({'response':response}, default=str)
        except Exception as e:
            print(e)
            messages.error(request, e)
        return HttpResponse(response)