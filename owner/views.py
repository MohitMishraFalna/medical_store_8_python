from django.http import HttpResponse, HttpResponseRedirect
from .get_record.get_all_type import GetWholeTypeData
from .sed.sed_activity import AllSearchEditDelete
from department.models import Department
from django.shortcuts import render
from product.models import Product
from doctor.models import Doctor
from staff.models import Staff
from django.views import View

# Create your views here.

class DashboardView(View):
    def get(self, request):
        # all staff here
        all_staff = GetWholeTypeData.get_staffs(request)
        
        # all department here
        all_department = GetWholeTypeData.get_departments(request)
        
        # all doctor here
        all_doctor = GetWholeTypeData.get_doctor(request)
        
        # all product here
        all_product = GetWholeTypeData.get_products(request)
        
        # all customer here
        all_customer = GetWholeTypeData.get_customers(request)

        # all order here
        all_orders = GetWholeTypeData.get_orders(request)       

        return render(request, 'owner/dashboard.html', {'staffs':all_staff, 'departments':all_department, 'doctors':all_doctor, 'products':all_product, 'customers':all_customer, 'orders':all_orders})

    # Department
    def department_edit(request) :
        result = GetWholeTypeData.get_department_Data(request)
        return render(request,'owner/department_edit.html', {'edit_form':result})
    
    def department_update(request) :
        AllSearchEditDelete.edit(request, Department)
        return HttpResponseRedirect('/owner/dashboard/')
    
    def department_delete(request) :
        response = AllSearchEditDelete.delete(request, Department)
        print(response)
        return HttpResponseRedirect('/owner/dashboard/')
    
    # Doctor
    def doctor_edit(request) :
        result = GetWholeTypeData.get_doctor_Data(request)
        # print(result)
        doc_id = request.GET.get('id')
        return render(request,'owner/doctor_edit.html', {'edit_form':result, 'id':doc_id})
    
    def doctor_update(request) :
        result = AllSearchEditDelete.doctor_update(request, Doctor)
        return HttpResponseRedirect('/owner/dashboard/')
    
    def doctor_delete(request) :
        response = AllSearchEditDelete.delete(request, Doctor)
        print(response)
        return HttpResponseRedirect('/owner/dashboard/')
   
    # Product
    def product_edit(request) :
        result = GetWholeTypeData.get_product_Data(request)
        pro_id = request.GET.get('id')
        return render(request,'owner/product_edit.html', {'edit_form':result, 'id':pro_id})
    
    def product_update(request) :
        result = AllSearchEditDelete.product_update(request, Product)
        return HttpResponseRedirect('/owner/dashboard/')
    
    def product_delete(request) :
        response = AllSearchEditDelete.delete(request, Product)
        return HttpResponseRedirect('/owner/dashboard/')
   
    # Staff
    def staff_delete(request) :
        response = AllSearchEditDelete.delete(request, Staff)
        return HttpResponseRedirect('/owner/dashboard/')

    def staff_search(request) :
        response = AllSearchEditDelete.search(request, Staff)
        return HttpResponse(response)

    def new_password(request) :
        response = AllSearchEditDelete.new_password(request, Staff)
        return HttpResponseRedirect('/owner/dashboard/')

    # All Order Product table
    def order_product_table(request) :
        result = GetWholeTypeData.order_product(request)  
        return HttpResponse(result)

    
