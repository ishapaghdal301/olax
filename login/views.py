from django.shortcuts import redirect, render,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password,make_password
from django.contrib.auth.decorators import login_required
from store.models import Customer,Category,Products,Order
# from django.views import View


def homepage(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    
    if request.method == 'POST':
        product_quantity(request)
        return redirect('homepage')

    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products()
    
    id = request.session.get('customer')
    if not id:
        request.session['customer'] = {}
    
    customer = Customer.get_customer_by_id(id)

    data = {}
    data['products'] = products
    data['categories'] = categories
    data['customer'] = customer
  
    print('you are : ', request.session.get('username'))
    return render(request, 'navbar.html', data)

def pro_desc(request):

    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        if product_id is not None:
            print(product_id)
            print('----------------------------------------------------------------------------------------')
            p = Products.get_product_by_id(product_id)
        else:
            product_id = request.session['product_id']
            print(product_id)
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            p = Products.get_product_by_id(product_id)

    id = request.session['customer']
    customer = Customer.get_customer_by_id(id)
    return render(request,"pro_desc.html",{'product':p,'customer':customer})

def product_quantity(request):
    if request.method == 'POST':
       product = request.POST.get('product')
       remove = request.POST.get('remove')
       cart = request.session.get('cart')
       request.session['product_id'] = product
       if cart:
           quantity = cart.get(product)
           if quantity:
               if remove:
                   if quantity<=1:
                       cart.pop(product)
                   else:
                       cart[product]  = quantity-1
               else:
                   cart[product]  = quantity+1
           else:
               cart[product] = 1
       else:
           cart = {}
           cart[product] = 1
       request.session['cart'] = cart
       print('cart' , request.session['cart'])
       
    return redirect('pro_desc')
def updateprofile(request):
    
    id = request.session['customer']
    customer = Customer.get_customer_by_id(id)
    if request.method == "POST":
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        nationality = request.POST.get('nationality')
        upload1=request.FILES['upload']
        
        customer.upload = upload1
        customer.first_name = first_name
        customer.last_name = last_name
        customer.email = email
        customer.phone = phone
        customer.gender = gender
        customer.nationality = nationality 
        Customer.register(customer)
    return render(request,'update_profile.html',{'customer':customer})

def sell(request):
    cust_id = request.session['customer']

    categories = Category.get_all_categories()
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        customer = Customer.objects.get(id=cust_id)
        description = request.POST.get('description')
        image1=request.FILES['image']
        
        product= Products.objects.create(name = name,price = price,category = category,description = description,
                          customer = customer,image= image1 )
        Products.register(product)

    id = request.session.get('customer')
    if not id:
        request.session['customer'] = {}
    
    customer = Customer.get_customer_by_id(id)
    return render(request,'sell.html',{'categories':categories,'customer':customer})

def orderdetail(request):
    id = request.session['customer']
    customer = Customer.get_customer_by_id(id)
    if request.method == "POST":
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        customer.email = email
        customer.phone = phone
        customer.address = address
        Customer.register(customer)
        CheckOut(request)
        id = request.session.get('customer')
        if not id:
            request.session['customer'] = {}
            customer = Customer.get_customer_by_id(id)
        return redirect('orders')
    else:
        return render(request, 'order_detail.html',{'customer':customer})
    
def CheckOut(request):
    id = request.session['customer']
    customer = Customer.get_customer_by_id(id)
    address = customer.address
    phone = customer.phone
    cart = request.session.get('cart')
    products = Products.get_products_by_id(list(cart.keys()))
    print(address, phone, customer, cart, products)

    for product in products:
        print(cart.get(str(product.id)))
        order = Order(customer=Customer(id=id),
                      product=product,
                      price=product.price,
                      address=address,
                      phone=phone,
                      quantity=cart.get(str(product.id)))
        order.save()
    request.session['cart'] = {}

    return redirect('cart')


def orders(request):
    print("ORDERRRRRR IS CALLED>>>>>")
    customer = request.session.get('customer')
    order = Order.get_orders_by_customer(customer)
    print(order)
    id = request.session.get('customer')
    if not id:
        request.session['customer'] = {}
    customer = Customer.get_customer_by_id(id)
    return render(request, 'orders.html', {'orders': order,'customer':customer})

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products()
  
    data = {}
    data['products'] = products
    data['categories'] = categories
  
    print('you are : ', request.session.get('username'))
    return render(request, 'navbar.html', data)

def cart(request):

    if request.method == 'GET':
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}

        ids = list(request.session.get('cart').keys())
        products = Products.get_products_by_id(ids)
        print(products)
        id = request.session.get('customer')
        if not id:
            request.session['customer'] = {}
        customer = Customer.get_customer_by_id(id)
        return render(request , 'cart.html' , {'products' : products,'customer':customer} )

def sellproductlist(request):
    ids = request.session['customer']
    # customer = Customer.get_customer_by_id(id)
    products = Products.get_products_by_customer(ids)
    if request.method == 'POST':
        pro_id = request.POST.get('product')
        Products.objects.filter(id=pro_id).delete()
        return redirect('sellproductlist')
    id = request.session.get('customer')
    if not id:
        request.session['customer'] = {}
    customer = Customer.get_customer_by_id(id)
    return render(request , 'showsellproduct.html',{'products':products,'customer':customer})

def signup(request):
    postData = request.POST
    first_name = postData.get('firstname')
    last_name = postData.get('lastname')
    username = postData.get('username')
    email = postData.get('email')
    pass1 = postData.get('pass1')
    pass2 = postData.get('pass2')
    # validation
    value = {
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'email': email
    }
    error_message = None

    customer = Customer(first_name=first_name,
                        last_name=last_name,
                        username = username,
                        email=email,
                        pass1=pass1,
                        pass2=pass2)
    error_message = validateCustomer(customer)

    if not error_message:
        print(first_name, last_name, username, email, pass1)
        customer.pass1 = make_password(customer.pass1)
        customer.register()
        return redirect('login')
    else:
        data = {
            'error': error_message,
            'values': value
        }
        return render(request, 'signup.html', data)

def validateCustomer(customer):
    error_message = None
    if (not customer.first_name):
        error_message = "Please Enter your First Name !!"
    elif len(customer.first_name) < 3:
        error_message = 'First Name must be 3 char long or more'
    elif not customer.last_name:
        error_message = 'Please Enter your Last Name'
    elif len(customer.last_name) < 3:
        error_message = 'Last Name must be 3 char long or more'
    # elif not customer.phone:
    #     error_message = 'Enter your Phone Number'
    # elif len(customer.phone) < 10:
    #     error_message = 'Phone Number must be 10 char Long'
    elif len(customer.pass1) < 5:
        error_message = 'Password must be 5 char long'
    elif len(customer.email) < 5:
        error_message = 'Email must be 5 char long'
    elif customer.isExists():
        error_message = 'Email Address Already Registered..'
    # saving

    return error_message
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     pass1 = request.POST.get('pass1')
    #     pass2 = request.POST.get('pass2')
    #     firstname = request.POST.get('firstname')
    #     lastname = request.POST.get('lastname')
    #     email = request.POST.get('email')

    #     if User.objects.filter(username = username):
    #         return render(request,"signup.html",{'error':"Username already exist."})
        
    #     if User.objects.filter(email = email):
    #         return render(request,"signup.html",{'error':"Email is already registered."})

    #     if pass1 != pass2 :
    #         return render(request,"signup.html",{'error':"Password do not match."})
        
    #     myuser = User.objects.create_user(username,email,pass1)
    #     myuser.firstname = firstname
    #     myuser.lastname = lastname

    #     myuser.save()
    #     return render(request,"navbar.html")
    # return render(request,"signup.html")

def login(request):
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     pass1 = request.POST.get('pass1')

    #     user = authenticate(username=username, password =pass1)

    #     if user is not None:
    #         auth_login(request , user)
    #         return render(request,"navbar.html")
        
    #     else:
    #         return render(request,"login.html")
    # return render(request,"login.html")
    return_url = None
    username = request.POST.get('username')
    pass1 = request.POST.get('pass1')
    customer = Customer.get_customer_by_username(username)
    error_message = None
    if customer:
        flag = check_password(pass1, customer.pass1)
        if flag:
            request.session['customer'] = customer.id

            if return_url:
                return HttpResponseRedirect(return_url)
            else:
                return_url = None
                return redirect('homepage')
        else:
            # request.session['customer'] = None
            error_message = 'Invalid Password!!'
    else:
        error_message = 'Invalid user!!'

    print(username, pass1)
    return render(request, 'login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('homepage')
    # auth_logout(request)
    # response = render(request,"navbar.html")
    # response.delete_cookie('user_location')
    # return response
    