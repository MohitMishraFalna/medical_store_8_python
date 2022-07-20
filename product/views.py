from django.http import HttpResponse, HttpResponseRedirect
from .forms import AddProduct, EditproductForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render
from django.views import View
from .models import Product
import json

# Create your views here.
class ProductView(View):
    # Get all deparment data and decorate by the pagination.
    def get(self, request):
    
        add_form = AddProduct(auto_id=True)

        # pagination
        per_page = request.GET.get('selectPerPage')

        # If per_page value not coming so assign manualy
        if not per_page:
            per_page = 5

        # get data from the table
        products = Product.objects.all().order_by('id')

        # apply pagination
        paginator = Paginator(products, per_page)

        # get page number from url bar
        page_number = request.GET.get('page')

        # convert all product data to pagination object
        page_obj = paginator.get_page(page_number)

        # get all pages from pagination object
        total_pages = page_obj.paginator.num_pages

        # create compaharance list
        total_page_list = [n+1 for n in range(total_pages)]
        return render(request, 'product/new_product.html', {'add_form':add_form, 'products':page_obj, 'perPage':per_page, 'totalPages':total_pages, 'totalPageList':total_page_list})
    
    # Save data
    def post(self, request):
        add_form = AddProduct(request.POST, auto_id=True)
        if add_form.is_valid():
            add_form = Product(
                name=request.POST.get('name'), 
                amt=request.POST.get('amount'),
                quantity=request.POST.get('quantity'),
                manufacturing=request.POST.get('manufacturing'),
                expiry=request.POST.get('expiry'),
                department_id=request.POST.get('department'),
                )
            add_form.save()
            messages.success(request, 'Product add successfull.')
        return HttpResponseRedirect('/product/add/')

    # Get data and send django forms as ajax response
    def get_product_Data(request):
        get_product = Product.objects.get(id=request.GET.get('doc_id'))

        # Set initial value of django forms input and send as ajax respons
        # If you getting any type of error so use form_name.as_p() method.
        edit_form = EditproductForm(initial={'name':get_product.name, 'pro_id':get_product.id, 'amt':get_product.amt, 'quantity':get_product.quantity, 'expiry':get_product.expiry, 'manufacturing':get_product.manufacturing, 'department':get_product.department}, auto_id=True)
        return HttpResponse(edit_form.as_p())

    # Edit method
    def edit(request):
        try:
            print(request.POST.get('pro_id'))
            name = request.POST.get('name')
            amt = request.POST.get('amt')
            quantity = request.POST.get('quantity')
            expiry = request.POST.get('expiry')
            manufacturing = request.POST.get('manufacturing')
            department = request.POST.get('department')

            product_update = Product.objects.filter(id=request.POST.get('pro_id')).update(name=name, amt=amt, quantity=quantity, expiry=expiry, manufacturing=manufacturing, department=department)
            
            if product_update:
                messages.success(request, "Product updated succussfully.")

        except Exception as e:
            print(e)
            messages.error(request, e)
        return HttpResponseRedirect('/product/add/')

    # Delete Method
    def delete(request):
        try:
            updateStaff = Product.objects.filter(id=request.GET.get('d_id')).update(deleted_at = 0)
            if updateStaff:
                messages.success(request, "product deleted succussfully.")
        except Exception as e:
            print(e)
            messages.error(request, e)
        return HttpResponseRedirect('/product/add/')

    # product search
    def product_search(request):
        try:
            search_item = request.GET.get('search_Item')
            product_list = Product.objects.filter(name__icontains = search_item)
            response = []
            if product_list:
                for product in product_list:
                    response.append({'id':product.id, 'name': product.name, 'amt': product.amt, 'quantity': product.quantity, 'expiry': product.expiry.strftime('%m/%d/%Y'), 'manufacturing': product.manufacturing.strftime('%m/%d/%Y'), 'department': product.department, 'deleted_at': product.deleted_at})             
                response = json.dumps({'response':response}, default=str)
        except Exception as e:
            print(e)
            messages.error(request, e)
        return HttpResponse(response)