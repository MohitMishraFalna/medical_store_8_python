from django.contrib import messages
from seller.models import Customer
from django.views import View


class CustomerCreateUpdate(View):
    def customer_create_or_update(request):
        try:
            # Customer process            
            name = request.POST.get('customerList')
            cust_id = request.POST.get('cust_id')
            mobile = request.POST.get('mobile')
            doc_id = request.POST.get('doc_id')
            payable = request.POST.get('payable')
            paid_amt = request.POST.get('paid_amt')
            due = float(payable) - float(paid_amt)
            
            if not cust_id:
                customer = Customer.objects.create(name=name, mobile=mobile, doctor_id=doc_id, due_amt=due)
                return customer.id

            customer = Customer.objects.filter(id = cust_id).update(due_amt=due)
            if customer:
                return cust_id

        except Exception as e:
            print(e)
            messages.error(request, e)
