from django.contrib import messages
from seller.models import Order
from django.views import View


class OrderCreateUpdate(View):
    def order_create(request, customer_id):
        try:            
            payable = request.POST.get('payable')
            paid_amt = request.POST.get('paid_amt')
            due = float(payable) - float(paid_amt)

            create_order = Order.objects.create(customer_id=customer_id, doctor_id=request.POST.get('doc_id'), gst=request.POST.get('gst'),  bill_amt=request.POST.get('amount'), due_amt=due, total_amt=request.POST.get('total_amt'), paid_amt=paid_amt, payable_amt=payable)

            if create_order:
                return create_order.id
        except Exception as e:
            print(e)
            messages.error(request, e)

