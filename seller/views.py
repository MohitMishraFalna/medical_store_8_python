from seller.create_update.product_order_create_update import ProductOrderCreate
from seller.create_update.order_create_update import OrderCreateUpdate
from .create_update.customer_create_update import CustomerCreateUpdate
from django.http import HttpResponse, HttpResponseRedirect
from owner.get_record.get_all_type import GetWholeTypeData
from .payment_gateway.razorpay import RazorpayGateway
from seller.models import Customer, Order
from django.contrib import messages
from django.shortcuts import render
from product.models import Product
from doctor.models import Doctor
from django.views import View
import json



# Create your views here.
class NewBill(View):
    def get(self, request):
        return render(request, 'seller/new_bill.html')
    
    def post(self, request):
        try:                       
            customer_result = CustomerCreateUpdate.customer_create_or_update(request)
            if customer_result:
                order_result = OrderCreateUpdate.order_create(request, customer_result)
                if order_result:
                    product_order = ProductOrderCreate.create_product_order(request, order_result)
                    if product_order:
                        product_update = ProductOrderCreate.update_product_order(request)
                        if product_update:
                            res = RazorpayGateway.razorpay_payment(request, order_result)
                            print(res)
                            if res:
                                return render(request, 'seller/new_bill.html', res)                       


        except Exception as e:
            print(e)
            messages.error(request, e)
        return HttpResponseRedirect('/seller/workbench/')

    # Payment Gateway status save
    def save_payemnt_status(request):
        try:
            json_obj = ''
            status = ''
            if request.GET.get('error_code'):                
                json_obj = [dict(order_id=request.GET.get('my_order_id'), error_code=request.GET.get('error_code'), error_description=request.GET.get('error_description'), error_source=request.GET.get('error_source'), error_step=request.GET.get('error_step'), error_reason=request.GET.get('error_reason'), error_order_id=request.GET.get('error_order_id'), error_payment_id=request.GET.get('error_payment_id'))]
                status = 'error'
                # dictionary insert ---- when we want to fetch data from dict so use json.loads() this decode the json string in normal obj.
                json_obj = json.dumps(json_obj)
            else:
                json_obj = dict(order_id=request.GET.get('my_order_id'), payment_id=request.GET.get('payment_id'), payment_order_id=request.GET.get('payment_order_id'), payment_signature=request.GET.get('payment_signature'))
                status = 'success'
            update_payment_status = Order.objects.get(id =request.GET.get('my_order_id'))
            update_payment_status.payment_status = status
            update_payment_status.payment_data = json_obj
            update_status = update_payment_status.save()
            
            # call function for printing bill
            result = GetWholeTypeData.order_product(request)

        except Exception as e:
            print(e)
            messages.error(request, e)
        return HttpResponse(result)

    def customer_exists(request):
        try:
            search_item = request.GET.get('search_Item')
            customer_list = Customer.objects.filter(name__icontains = search_item)

            response = []
            if customer_list:
                for customer in customer_list:
                    response.append({'id': customer.id, 'name': customer.name, 'mobile': customer.mobile, 'due_amt':customer.due_amt})             
                response = json.dumps({'response':response}, default=str)
            else:
                response = customer_list
            
        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong.')

        return HttpResponse(response)   
        
    def doctor_exists(request):
        try:
            search_item = request.GET.get('search_Item')
            doctor_list = Doctor.objects.filter(name__icontains = search_item)
            response = []
            if doctor_list:
                for doctor in doctor_list:
                    response.append({'id': doctor.id, 'name': doctor.name})             
                response = json.dumps({'response':response}, default=str)
        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong.')   
        return HttpResponse(response)   
                
    def product_list(request):
        try:
            search_item = request.GET.get('search_Item')
            product_list = Product.objects.filter(name__icontains = search_item)
            response = []
            if product_list:
                for product in product_list:
                    response.append({'id': product.id, 'name': product.name, 'manufacturing': product.manufacturing.strftime('%m/%d/%Y'), 'expiry': product.expiry.strftime('%m/%d/%Y'), 'department': product.department, 'amt': product.amt})
                response = json.dumps({'response':response}, default=str)
        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong.')   
        return HttpResponse(response)   
        
         