from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from shopping.models import *
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
def all_category():
    all_cat = Category.objects.all()
    return all_cat

def total(u):
    data = Add_to_cart.objects.filter(usr = u)
    total = 0
    for i in data:
        total += int(i.product.price)
    return total

def Home(request):
    products = Product.objects.all().order_by('-id')
    last_five = products[:5]
    sub_cat = Sub_category.objects.all().order_by('-id')
    subcat = sub_cat[:4]
    if request.user.is_authenticated():
     d = {"subcat":subcat,"last_five":last_five,'allcat' : all_category(), 'total': total(request.user)}

    else:
        d = {"subcat":subcat,"last_five":last_five,'allcat': all_category(),}
    return render(request, 'index.html',d)

def About(request):
    if request.user.is_authenticated():
         d = {'allcat': all_category(), 'total': total(request.user)}

    else:
        d = {'allcat': all_category()}

    return render(request, 'about.html', d)


def Contact(request):
    if request.user.is_authenticated():
        d = {'allcat': all_category(), 'total': total(request.user)}

    else:
        d = {'allcat': all_category()}
    return render(request, 'contact.html', d)

def products(request, sub_id):
    data = Sub_category.objects.filter(id = sub_id).first()
    if request.user.is_authenticated():
         d = {'allcat': all_category(),'subcat':data, 'total': total(request.user)}

    else:
        d = {'allcat': all_category(),'subcat':data,}
    return render(request,'products.html',d)

def Product_Details(request,p_id):
    pdata = Product.objects.filter(id = p_id).first()
    if request.user.is_authenticated():
      d = {'allcat': all_category(),"product":pdata, 'total': total(request.user)}
    else:
        d = {'allcat': all_category(), "product": pdata}

    return render(request,'product_details.html',d)


def Login(request):
    error = False

    if request.method == 'POST':
        u = request.POST['user']
        p = request.POST['pwd']
        us = authenticate(username = u, password = p)
        if us:
            login(request,us)
            if request.user.is_staff:
              return redirect('admin_panel')
            else:
                return redirect('home')
        else:

            error = True
    d = {'allcat': all_category, 'error':error}
    return render(request,'login.html',d)

def AddToCart(request,pid):
    data = Product.objects.filter(id=pid).first()
    dd = Add_to_cart.objects.filter(product =data,usr = request.user)
    if dd:
        return redirect('mycart')
    else:
        Add_to_cart.objects.create(usr = request.user,product=data)
        return redirect('mycart')

def MyCart(request):
    mycart = Add_to_cart.objects.filter(usr=request.user)
    total = 0
    for i in mycart:
        total += int(i.product.price)
    d = {'allcat': all_category(), 'mycart': mycart, 'total': total}
    return render(request,'cart.html',d)

def Delete_product_from_cart(request,cid):
    data = Add_to_cart.objects.filter(id = cid).first()
    data.delete()
    return redirect('mycart')

def Signup(request):
    error = False
    if request.method=='POST':
        u = request.POST['user']
        p = request.POST['pwd']
        n = request.POST['name']
        m = request.POST['mob']
        e = request.POST['email']
        a = request.POST['add']
        user_data = User.objects.filter(username = u)
        if user_data:
            error = True
        else:
            user = User.objects.create_user(username = u, password= p)
            User_detail.objects.create(user = user,name = n, mobile = m,
                                       email = e,address= a)
            return redirect('login')
    d = {'allcat': all_category(),'error':error}
    return render(request,'signup.html',d)


def Order(request,pid):
    data = User_detail.objects.filter(user = request.user).first()
    address = data.address
    d = {'allcat': all_category(),'address': address, 'total':total(request.user)}
    if request.method == "POST":
        add = request.POST['add']
        product = Product.objects.filter(id = pid).first()
        data2 = Add_to_cart.objects.filter(product = product,usr=request.user)
        data2.delete()
        Order_placed.objects.create(user = request.user,product = product,address=add)
        sub = "Order Placed"
        from_email = settings.EMAIL_HOST_USER
        d = {"name":data.name,"product":product.name,
             "price":product.price,"des":product.discription}
        html = get_template('mail.html').render(d)
        msg = EmailMultiAlternatives(sub,' ',from_email,[data.email])
        msg.attach_alternative(html,'text/html')
        #msg.send()

        return redirect('payment',pid)
    return render(request,'order.html',d)

def Clear_Cart(request):
    data = Add_to_cart.objects.filter(usr=request.user)
    data.delete()
    return redirect('home')

import requests
import json


headers = {"X-Api-Key": "36fedc81de23f05b7044ababd27d0555",
           "X-Auth-Token": "6fb6c5ad36a9baa8a7c734141a9535f3"}

def Payment(request,pid):
    product = Product.objects.filter(id = pid).first()
    user = User_detail.objects.filter(user = request.user).first()
    payload = {
        "purpose":"Product Payment",
        "amount":product.price,
        "buyer_name":user.name,
        "email":user.email,
        "phone":user.mobile,
        "send_email":True,
        "send_sms":True,
        "redirect_url":"http://127.0.0.1:8000/payment_check/"
    }
    response = requests.post("https://www.instamojo.com/api/1.1/payment-requests/",
                            data=payload,headers=headers)
    print(response)
    y = response.text
    d = json.loads(y)
    a = d['payment_request']['longurl']
    i = d['payment_request']['id']
    Payment_ids.objects.create(ids = i,user = request.user)
    return redirect(a)

def Payment_check(request):
    i = Payment_ids.objects.filter(user = request.user).first()
    ii = i.ids
    response = requests.get("https://www.instamojo.com/api/1.1/payment-requests/"+str(ii)+'/',
                            headers=headers)
    y = response.text
    b = json.loads(y)
    print(b)
    status = b['payment_request']['status']
    if status=="Completed":
        return HttpResponse('Done')
    else:
        return HttpResponse("Fail")


def Admin_home(request):
    return render(request,'admin_home.html')

def AllCategory(request):
    data = Category.objects.all()
    d = {"allcat":data}
    return render(request,'allcat.html',d)

def Add_category(request):
    if request.method == "POST":
        n = request.POST['cat']
        Category.objects.create(name = n)
        return redirect('all_cat')
    return render(request,'add_category.html')

def All_subcategory(request):
    data = Sub_category.objects.all()
    d = {"allsubcat":data}
    return render(request,'all_subcat.html',d)


def Add_sub_cat(request):
    all_cat = Category.objects.all()
    d = {"allcat":all_cat}
    if request.method == "POST":
        c = request.POST['cid']
        cat = Category.objects.get(id = c)
        n = request.POST['subcat']
        Sub_category.objects.create(category = cat,name = n)
        return redirect('all_subcat')
    return render(request,'add_subcat.html',d)


def All_product(request):
    all_product = Product.objects.all()
    d = {"all_product":all_product}
    return render(request,'all_product.html',d)

def Add_product(request):
    all_subcat = Sub_category.objects.all()
    d = {"allsubcat":all_subcat}
    if request.method == "POST":
        s = request.POST['sid']
        subcat = Sub_category.objects.get(id = s)
        n = request.POST['name']
        p = request.POST['price']
        d = request.POST['dis']
        i1 = request.FILES['img1']
        i2 = request.FILES['img2']
        i3 = request.FILES['img3']
        Product.objects.create(subcategory = subcat,name = n,price = p,discription = d,
                               img1 = i1,img2=i2,img3 = i3)
        return redirect('all_product')
    return render(request,'add_product.html',d)

def Delete_cat(request,cid):
    data = Category.objects.get(id = cid)
    data.delete()
    return redirect('all_cat')

def Delete_subcat(request,sid):
    data = Sub_category.objects.get(id = sid)
    data.delete()
    return redirect('all_subcat')
def Delete_product(request,pid):
    data = Product.objects.get(id = pid)
    data.delete()
    return redirect('all_product')


def All_order(request):
    all_ordered_product = []
    for i in Product.objects.all():
        data = Order_placed.objects.filter(product = i)
        if data:
            all_ordered_product.append(i)
    d = {"all_ordered_product":all_ordered_product}
    return render(request,'all_order.html',d)


def Buyer_details(request,pid):
   pro = Product.objects.get(id = pid)
   user_list = []
   number = []
   for i in User_detail.objects.all():
       data = Order_placed.objects.filter(user=i.user,product=pro)

       if data:
           number.append(data.count())
           user_list.append(i)
   z = zip(user_list,number)

   d = {"product":pro,"z":z}
   return render(request,'user_list.html',d)

