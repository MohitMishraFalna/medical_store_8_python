from product.models import Product
from seller.models import ProductOrder
from django.contrib import messages
from django.views import View

class ProductOrderCreate(View):
    def create_product_order(request, order_id):
        try:
            prod_id_str = request.POST.get('prod_id')
            prod_qty_str = request.POST.get('prod_qty')

            prod_id_arr = [int(p.strip()) for p in prod_id_str.split(',') if p]
            prod_qty_arr = [int(q.strip()) for q in prod_qty_str.split(',') if q]

            for x in range(len(prod_id_arr)):
                product_order_create = ProductOrder.objects.create(order_id=order_id, product_id=prod_id_arr[x], order_qty=prod_qty_arr[x])
            return product_order_create.id
        except Exception as e:
            print(e)
            messages.error(request, e)
    
    def update_product_order(request):
        try:
            prod_id_str = request.POST.get('prod_id')
            prod_qty_str = request.POST.get('prod_qty')

            prod_id_arr = [int(p.strip()) for p in prod_id_str.split(',') if p]
            prod_qty_arr = [int(q.strip()) for q in prod_qty_str.split(',') if q]

            for x in range(len(prod_id_arr)):
                product_order_get = Product.objects.get(id=prod_id_arr[x])
                get_product_qty = product_order_get.quantity
                calculate_product_qty = float(get_product_qty) - prod_qty_arr[x]
                product_order_get.quantity = calculate_product_qty
                product_order_get.save()
            return 1
        except Exception as e:
            print(e)
            messages.error(request, e)