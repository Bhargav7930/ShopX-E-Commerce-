from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import razorpay
from django.contrib.auth.decorators import login_required
from django.conf import settings
import uuid
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from .models import *

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})
def product_detail(request,slug):
    product = Product.objects.get(slug=slug)
    return render(request,'product_detail.html',{'product':product})
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user_obj = User.objects.filter(username=username).first()

        if user_obj is None:
            messages.warning(request,"User Not Found")
            return redirect('/login')
        customer = Customer.objects.filter(user=user_obj).first()

        if not customer.is_verified:
            messages.warning(request,"Your Profie Not Verified Yet...Please Check Your Mail")
            return redirect("/login")
        user = authenticate(username=username,password=password)

        if user is None:
            messages.warning(request,"Invalid Username Or Password")
            return redirect('/login')
        login(request,user)
        return redirect('/')
        
    return render(request,'login.html')
def register_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST['phone']
        full_name = request.POST['full_name']
        image = request.POST['image']
        try:
            if User.objects.filter(username=username).first():
                messages.warning(request,'Username already Exists')
                return redirect('/register')
            elif Customer.objects.filter(email=email).first():
                messages.warning(request,'Email already Taken')
                return redirect('/register')
            elif Customer.objects.filter(phone=phone).first():
                messages.warning(request,'Phone Number already Used')
                return redirect('/register')
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()
            auth_token =str(uuid.uuid4())
            customer = Customer(user=user,image=image,full_name=full_name,email=email,phone=phone,auth_token=auth_token)
            customer.save()

            send_mail_after_register(email,auth_token)
            messages.success(request,'we sent to you mail for verification')
            return redirect('/token')
        except Exception as e:
            print(e)
    return render(request,'register.html')

def send_mail_after_register(email,token):
    subject = "YOUR ACCOUNT NEED TO BE VERIFIED"
    message =f"Hi Paste The Link in Browser http://127.0.0.1:8000/verify/{token}/"
    email_from = settings.EMAIL_HOST_USER
    send_to = [email]
    send_mail(subject,message,email_from,send_to)



def verify(request,auth_token):
    try:
        profile_obj = Customer.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                 messages.success(request,'your profile is already verified')
                 return redirect('/login')
                

            profile_obj.is_verified=True
            profile_obj.save()
            messages.success(request,'Congratulation Your Email Has Verified successfully')
            return redirect ('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)

def error_page(request):
    return render(request,'error.html')
def success(request):
    return render (request,'success.html')

def token_send(request):
    return render (request,'token_send.html')
@login_required(login_url="/login")
def add_cart(request,id):
    user = request.user
    product = Product.objects.get(id=id)
    cart,created= Cart.objects.get_or_create(user=user,ordered=False)
    price =product.price
    cart_items =CartItem(user=user,product=product,price=price,cart=cart)
    cart_items.save()
    total_price = 0
    cart_items = CartItem.objects.filter(user=user,cart=cart.id)
    for items in cart_items:
        total_price += items.price
    cart.total_price = total_price
    cart.save()
    messages.success(request,"Your Item Added ")
    return redirect ("/")

    # return render(request, 'cart.html',{'cart_items':cart_items,'cart':cart})
@login_required(login_url="/login")    
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user,ordered=False).first()
    cart_items = CartItem.objects.filter(user=user,cart=cart)
    total_price = 0
    for items in cart_items:
        total_price += items.price
    cart.total_price = total_price
    cart.save()
    return render(request, 'cart.html',{'cart_items':cart_items,'cart':cart})
@login_required(login_url="/login")    
def remove_cart(request,id):
    user=request.user
    cart = Cart.objects.filter(user=user,ordered=False).first()
    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()
    return redirect ("/show-cart")
@login_required(login_url="/login")
def ship_address(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            full_name = request.POST.get("full_name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            address = request.POST.get("address")
            city = request.POST.get("city")
            state = request.POST.get("state")
            zip_code = request.POST.get("zip")

            customer_obj = Customer.objects.filter(user=user).first()

            ship_ad = Shipping_Address(customer=customer_obj,user=user,full_name=full_name,
            email=email,address=address,zip_code=zip_code,city=city,state=state,phone=phone)
            ship_ad.save()

            return redirect("/checkout")
        
        return render(request,'address.html')
@login_required(login_url="/login")
def checkout(request):
    user = request.user
    cart = Cart.objects.filter(user=user,ordered=False).first()
    cart_item= CartItem.objects.filter(user=user,cart=cart)
    
    razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
    currency ='INR'
    amount = int(cart.total_price) * 100

    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture=1))

    razorpay_order_id = razorpay_order['id']
    callback_url ='/paymenthandler/'
    context={}
    context['razorpay_order_id'] =razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount']= amount
    context['currency']= currency
    context['callback_url']=callback_url
    context['cart']=cart
    context['cart_item']=cart_item

    return render(request,'checkout.html',context=context)
@csrf_exempt
def paymenthandler(request):
    user = request.user
    cart = Cart.objects.filter(user=user,ordered=False).first()
    cart_item= CartItem.objects.filter(user=user,cart=cart)
    amount = cart.total_price *100
    razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
    if request.method == 'POST':
        try:
            payment_id =request.POST['razorpay_payment_id'," "]
            razorpay_order_id = request.POST['razorpay_order_id'," "]
            signature = request.POST['razorpay_signature'," "]

            param_dict={
                'razorpay_order_id':razorpay_order_id,
                'razorpay_payment_id':payment_id,
                'razorpay_signature':signature,  
            }
            result = razorpay_client.utility.verify_payment_signature(param_dict)

            if result is None:
                amount = amount
                try:
                    razorpay_client.payment.capture(payment_id,amount)
                    order = Order(user=user,cart=cart,amount=amount,order_id=razorpay_order_id,
                    payment_id=payment_id,payment_signature = signature,is_paid=True)
                    order.save()
                    order_item = OrderItem(user=user, order=order,cart_item=cart_item)
                    order_item.save()
                    ship=Shipping_Address.objects.filter(user=user).first()
                    return render(request,'order.html',{'order':order,'order_item':order_item,'ship':ship})

                    
                except:
                    return HttpResponseBadRequest()
        except:
            return HttpResponseBadRequest()    
    return HttpResponseBadRequest()

def search(request):
    if request.method == "POST":
        search = request.POST.get('search')
        product = Product.objects.filter(product_name__icontains=search)
        return render(request,'search.html',{'products':product,'search':search})
    product = Product.objects.all()
    messages.warning(request,"please enter Valid Product Name")
    return render(request,'search.html',{'products':product})
def logout_page(request):
    logout(request)
    return redirect('/login')
@login_required(login_url="/login")    
def profile_page(request):
    user = request.user
    customer = Customer.objects.filter(user=user).first()
    ship = Shipping_Address.objects.filter(customer=customer).first()
    
    return render(request,'profile.html',{'user':user, 'customer':customer,'ship':ship})
from django.contrib.auth.hashers import check_password
@login_required(login_url="/login")
def change_password(request):
    user = request.user
    if request.method =="POST":
        cpassword = request.POST.get('cpassword')
        npassword = request.POST.get('npassword')
        check = authenticate(username=user.username,password=cpassword)
        if check:
            user_obj=User.objects.get(username=user.username)
            user_obj.set_password(npassword)
            user_obj.save()
            messages.success(request,'Password updated successfully') 
            return redirect('/login')
        messages.success(request,'Invalid password')
        return render(request, 'change_pass.html')
    return render(request,'change_pass.html')
@login_required(login_url="/login")
def delete_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user= authenticate(username=username, password=password)
        if user is None:
            messages.error(request,'Please Enter Valid Username Or Password')
            return render(request,'delete_user.html')
        else:
            user.delete()
            messages.success(request,'User Deleted Successfully')
            return redirect("/register")
    return render(request,'delete_user.html')
def contact(request):
    if request.method=="POST":
        name = request.POST['full_name']
        email = request.POST['email']
        message = request.POST['message']

        contact=Contact(name=name,email=email,message=message)
        contact.save()
        messages.success(request,"We Received Your Message We Will Contact you Soon")
        return redirect('/')
    return render(request,"contact.html")
    
