from django.shortcuts import render,redirect
from . models import *
from django.http import JsonResponse
import json
from .forms import register,LoginForm,Search
from django.contrib.auth import authenticate,login,logout  
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache, cache_control 
from django.contrib import messages     


   

# # @login_required
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def store(request):
        products = Product.objects.all()
    
        form=Search(request.GET)
        query=request.GET.get('query','').strip()
        
        if query:
           products = Product.objects.filter(name__icontains=query)
      
        
           return render(request,'store/store.html',{'products':products,'form':form})

                                                 
    
      
        sort_by = request.GET.get('sort_by', '')  
        
        if sort_by == 'price_lowest':
            products = Product.objects.all().order_by('price')
            # return render(request, 'store/store.html',  {'products':products})
        elif sort_by == 'price_highest':
            products =Product.objects.all().order_by('-price')
            # return render(request, 'store/store.html',  {'products':products})
        else:
            products = Product.objects.all()
             
        try:
             customer = request.user.customer 
        except:
            customer=None
     
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
       
        context = { 'order':order,'products': products,'form':form}
        

        return render(request, 'store/store.html', context)
    
    
# @login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart(request):
    
    if  request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        
        
       
    else:
        items=[]  
        order={'order.get_cart_items':0, 'get_cart_total':0}
    context = {'items': items,'order':order}
            
    return render(request, 'store/cart.html',  context )
@never_cache
def checkout(request):
	  
    if  request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        
       
    else:
        return redirect('store')
    #     items=[]  
    #     order={'order.get_cart_items':0, 'get_cart_total':0}
    context = {'items': items,'order':order}
            
    

    return render(request, 'store/checkout.html', context)
  



 
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def RegisterForm(request):
     if  request.user.is_authenticated:
          return redirect('store')
     else:
        
        form=register()
        if request.method=='POST':
            form=register(request.POST)
            if form.is_valid():
                user=form.save()
                instance=Customer(user=user,name=form.data['username'],email=form.data['email'])
                instance.save()
                login(request,user)
            return redirect('store')
        
                 
     return render(request,'store/registration.html',{'form':form})
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
 
# @login_required
@never_cache
def loginf(request):
     if  request.user.is_authenticated:
          return redirect('store')
     else:
        form=LoginForm( )
        if request.method=="POST":
            form=LoginForm(request.POST)
            if form.is_valid():
                # form.save()
                username=request.POST.get('username')
                password=request.POST.get('password')
                user=authenticate(username=username,password=password)
                if user is not None:
            
                    login(request,user)
                    return redirect('store')
                else:
                    messages.error(request,'Invalid Login Credentials')
                    return redirect('login')
            
     return render(request,'login.html',{'form':form})
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# # @never_cache
# @login_required
def logoutf(request):
    logout(request)
    # request.session.clear()
    # request.session.flush()
    # if hasattr(request, 'user'):
    #   from django.contrib.auth.models import AnonymousUser
    #   request.user = AnonymousUser()
    return redirect('login')
    
        
        
        
        
    

