# Pre define library import
from django.core.paginator import Paginator
from django.db.models import Count
from django.views import View
import json

# Project forms import
from department.forms import DepartmentEditForm
from product.forms import EditproductForm
from doctor.forms import EditDoctorForm

# Project model import
from department.models import Department
from seller.models import Customer, ProductOrder
from product.models import Product
from seller.models import Order
from doctor.models import Doctor
from staff.models import Staff

class GetWholeTypeData(View):
    def get_staffs(request):
        # pagination
        staff_per_page = request.GET.get('staffTableSelector')

        # If per_page value not coming so assign manualy
        if not staff_per_page:
            staff_per_page = 5

        # get data from the table
        all_staff = Staff.objects.all().order_by('id')

        # get active, pendig and deactive staff using aggregate function.
        staff_deactive = all_staff.filter(deleted_at = 0).aggregate(Count('first_name'))['first_name__count']
        staff_pending = all_staff.filter(pwd_reset = 0, deleted_at = 1).aggregate(Count('first_name'))['first_name__count']
        staff_active = all_staff.filter(pwd_reset = 1, deleted_at = 1).aggregate(Count('first_name'))['first_name__count']
        
        # This line takes count of total staff and add 1.
        staff_count = all_staff.aggregate(Count('first_name'))['first_name__count'] + 1
        
        # apply pagination
        paginator = Paginator(all_staff, staff_per_page)

        # get page number from url bar
        page_number = request.GET.get('page')

        # convert all staff data to pagination object
        page_obj = paginator.get_page(page_number)

        # get all pages from pagination object
        total_pages = page_obj.paginator.num_pages

        # create compaharance list
        total_page_list = [n+1 for n in range(total_pages)]
        staffs = {'all_staff':page_obj, 'staffPerPage':staff_per_page, 'totalPages':total_pages, 'totalPageList':total_page_list}
        return({'staffs':staffs, 'total_staff':staff_count, 'staff_deactive' :staff_deactive, 'staff_pending':staff_pending, 'staff_active': staff_active})

    def get_departments(request):
        # pagination
        department_per_page = request.GET.get('departmetnSelectPerPage')

        # If per_page value not coming so assign manualy
        if not department_per_page:
            department_per_page = 5

        # get data from the table
        all_department = Department.objects.all().order_by('id')

        # get active, pendig and deactive staff using aggregate function.
        department_deactive = all_department.filter(deleted_at = 0).aggregate(Count('name'))['name__count']
        department_active = all_department.filter(deleted_at = 1).aggregate(Count('name'))['name__count']
        
        # This line takes all department accourding to name fields
        department_count = all_department.aggregate(Count('name'))['name__count']
        
        # apply pagination
        paginator = Paginator(all_department, department_per_page)

        # get page number from url bar
        page_number = request.GET.get('page')

        # convert all department data to pagination object
        page_obj = paginator.get_page(page_number)

        # get all pages from pagination object
        total_pages = page_obj.paginator.num_pages

        # create compaharance list
        total_page_list = [n+1 for n in range(total_pages)]
        departments = {'all_department':page_obj, 'departmetnSelectPerPage':department_per_page, 'totalPages':total_pages, 'totalPageList':total_page_list}
        return({'departments':departments, 'total_department':department_count, 'department_active' :department_active, 'department_deactive' :department_deactive})

    # Get data and send django forms as ajax response
    def get_department_Data(request):
        get_department = Department.objects.get(id=request.GET.get('dep_id'))
        
        # Set initial value of django forms input and send as ajax respons
        # If you getting any type of error so use form_name.as_p() method.
        edit_form = DepartmentEditForm(initial={'name':get_department.name, 'dep_id':get_department.id})
        return(edit_form)

    # All Doctor
    def get_doctor(request):
        # pagination
        doctor_per_page = request.GET.get('doctorSelectPerPage')

        # If per_page value not coming so assign manualy
        if not doctor_per_page:
            doctor_per_page = 5

        # get data from the table
        all_doctor = Doctor.objects.all().order_by('id')
        
        # get active, pendig and deactive staff using aggregate function.
        doctor_deactive = all_doctor.filter(deleted_at = 0).aggregate(Count('name'))['name__count']
        doctor_active = all_doctor.filter(deleted_at = 1).aggregate(Count('name'))['name__count']
        
        # This line takes data using name field
        doctor_count = all_doctor.aggregate(Count('name'))['name__count']
        
        # apply pagination
        paginator = Paginator(all_doctor, doctor_per_page)

        # get page number from url bar
        page_number = request.GET.get('page')

        # convert all doctor data to pagination object
        page_obj = paginator.get_page(page_number)

        # get all pages from pagination object
        total_pages = page_obj.paginator.num_pages

        # create compaharance list
        total_page_list = [n+1 for n in range(total_pages)]

        # Create dictionary for data send
        doctors = {'all_doctor':page_obj, 'doctorSelectPerPage':doctor_per_page, 'totalPages':total_pages, 'totalPageList':total_page_list}

        return({'doctors':doctors, 'total_doctor':doctor_count, 'doctor_active' :doctor_active, 'doctor_deactive' :doctor_deactive})

    # Get data and send django forms as ajax response
    def get_doctor_Data(request):
        get_doctor = Doctor.objects.get(id=request.GET.get('id'))

        # Set initial value of django forms input and send as ajax respons
        # If you getting any type of error so use form_name.as_p() method.
        edit_form = EditDoctorForm(auto_id=True, initial={'name':get_doctor.name, 'email':get_doctor.email, 'mobile':get_doctor.mobile, 'department':get_doctor.department})
        return (edit_form)

    # Get data and send django forms as ajax response
    def get_product_Data(request):
        get_product = Product.objects.get(id=request.GET.get('id'))

        # Set initial value of django forms input and send as ajax respons
        # If you getting any type of error so use form_name.as_p() method.
        edit_form = EditproductForm(auto_id=True, initial={'pro_id':get_product.id, 'name':get_product.name, 'amt':get_product.amt, 'quantity':get_product.quantity, 'expiry':get_product.expiry, 'manufacturing':get_product.manufacturing, 'department':get_product.department })
        return (edit_form)

    # all Product
    def get_products(request):
        # pagination
        product_per_page = request.GET.get('productSelectPerPage')

        # If per_page value not coming so assign manualy
        if not product_per_page:
            product_per_page = 5

        # get data from the table
        all_product = Product.objects.all().order_by('id')

        # get active, pendig and deactive staff using aggregate function.
        product_deactive = all_product.filter(deleted_at = 0).aggregate(Count('name'))['name__count']
        product_active = all_product.filter(deleted_at = 1).aggregate(Count('name'))['name__count']
        
        # This line takes all product accourding to name fields
        product_count = all_product.aggregate(Count('name'))['name__count']
        
        # apply pagination
        paginator = Paginator(all_product, product_per_page)

        # get page number from url bar
        page_number = request.GET.get('page')

        # convert all product data to pagination object
        page_obj = paginator.get_page(page_number)

        # get all pages from pagination object
        total_pages = page_obj.paginator.num_pages

        # create compaharance list
        total_page_list = [n+1 for n in range(total_pages)]
        products = {'all_product':page_obj, 'productSelectPerPage':product_per_page, 'totalPages':total_pages, 'totalPageList':total_page_list}
        return({'products':products, 'total_product':product_count, 'product_active' :product_active, 'product_deactive' :product_deactive})
    
    # all Customer
    def get_customers(request):
        # pagination
        customer_per_page = request.GET.get('customerSelectPerPage')

        # If per_page value not coming so assign manualy
        if not customer_per_page:
            customer_per_page = 5

        # get data from the table
        all_customer = Customer.objects.all().order_by('id')

        # This line takes all customer accourding to name fields
        customer_count = all_customer.aggregate(Count('name'))['name__count']
            
        # apply pagination
        paginator = Paginator(all_customer, customer_per_page)

        # get page number from url bar
        page_number = request.GET.get('page')

        # convert all customer data to pagination object
        page_obj = paginator.get_page(page_number)

        # get all pages from pagination object
        total_pages = page_obj.paginator.num_pages

        # create compaharance list
        total_page_list = [n+1 for n in range(total_pages)]
        customers = {'all_customer':page_obj, 'customerSelectPerPage':customer_per_page, 'totalPages':total_pages, 'totalPageList':total_page_list}
        
        return({'customers':customers, 'total_customer':customer_count})
    
    # all Orders
    def get_orders(request):
        # pagination
        order_per_page = request.GET.get('orderSelectPerPage')

        # If per_page value not coming so assign manualy
        if not order_per_page:
            order_per_page = 5

        # get data from the table
        all_order = Order.objects.all().order_by('id')
        
        # This line takes all order accourding to name fields
        order_count = all_order.aggregate(Count('bill_amt'))['bill_amt__count']
        
        # apply pagination
        paginator = Paginator(all_order, order_per_page)

        # get page number from url bar
        page_number = request.GET.get('page')

        # convert all order data to pagination object
        page_obj = paginator.get_page(page_number)

        # get all pages from pagination object
        total_pages = page_obj.paginator.num_pages

        # create compaharance list
        total_page_list = [n+1 for n in range(total_pages)]
        orders = {'all_order':page_obj, 'orderSelectPerPage':order_per_page, 'totalPages':total_pages, 'totalPageList':total_page_list}
        return({'orders':orders, 'total_order':order_count})

    # all Order Product
    def order_product(request):
        result = ProductOrder.objects.filter(order_id=request.GET.get('my_order_id'))
        response = []
        if result:
            for order in result:
                response.append({
                    'id'            : order.id, 
                    'qty'           : order.order_qty, 
                    'name'          : order.order.customer.name, 
                    'mobile'        : order.order.customer.mobile, 
                    'doctor'        : order.order.doctor.name, 
                    'department'    : order.order.doctor.department.name, 
                    'bill_amt'      : order.order.bill_amt, 
                    'gst'           : order.order.gst, 
                    'total_amt'     : order.order.total_amt, 
                    'due_amt'       : order.order.due_amt, 
                    'payable_amt'   : order.order.payable_amt, 
                    'paid_amt'      : order.order.paid_amt, 
                    'order_date'    : order.order.order_date.strftime('%m/%d/%Y'), 
                    'prod_name'     : order.product.name,
                    'prod_amt'      : order.product.amt,
                    })             
            response = json.dumps({'response':response}, default=str)
        return response

