from medical_store.settings import RAZORPAY_API_KEY, RAZORPAY_SECRET_KEY
from medical_store.razorpay.razorpay import Client
from django.contrib import messages
from django.views import View

class RazorpayGateway(View):
    def razorpay_payment(request, order_id):
        try:
            paid_amt = request.POST.get('paid_amt')
            amount = 100 * float(paid_amt)
            client = Client(auth=(RAZORPAY_API_KEY, RAZORPAY_SECRET_KEY))
            order_payment = client.order.create(dict(amount=amount, currency= 'INR', payment_capture=1))
            data = {'key':RAZORPAY_API_KEY, 'amount':amount, 'razorpay_order_id':order_payment['id'], 'my_order_id':order_id}
            return data
        except Exception as e:
            print(e)
            messages.error(request, e)