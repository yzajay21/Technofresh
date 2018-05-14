from django.http import JsonResponse
from django.shortcuts import render, redirect
from orders.models import Order
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from addresses.models import Address
from billing.models import BillingProfile
from products.models import Product
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from accounts.forms import LoginForm,GuestForm
from .models import Cart
from billing.views import payment
from django.conf import settings
from .utils import generate_hash
import hashlib
# Create your views here.
def cart_detail_api_view(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	products = [{
				"id":x.id,
				"url":x.get_absolute_url(),
				"name":x.title,
				"price":x.price,
				}
				 for x in cart_obj.products.all()]
	cart_data = {"products":products,"subtotal":cart_obj.subtotal,"total":cart_obj.total}
	return JsonResponse(cart_data)
def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = {
    	'cart' : cart_obj
    }
    return render(request, "carts/home.html",context)


def cart_update(request):
	product_id = request.POST.get('product_id')

	if product_id is not None:
		try :
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("Product Is Gone")
			return redirect("cart:home")
		
		cart_obj,new_obj= Cart.objects.new_or_get(request)
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
			added = False
		else:
			cart_obj.products.add(product_obj)
			added = True
		request.session['cart_items'] = cart_obj.products.count()
		if request.is_ajax():
			print("Ajax request")
			json_data = {
				"added" : added,
				"removed" : not added,
				"cartItemCount":cart_obj.products.count()
			}
			return JsonResponse(json_data,status=200)
			#return JsonResponse({"message" : "Error 400"},status_code=400)
	return redirect("cart:home")

def checkout_home(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	order_obj = None
	if cart_created or cart_obj.products.count() == 0:
		return redirect("cart:home")


	login_form =LoginForm(request=request)
	guest_form	= GuestForm(request=request)
	address_form = AddressForm()
	billing_address_id = request.session.get("billing_address_id",None)
	shipping_address_id = request.session.get("shipping_address_id",None)

	
	billing_profile ,billing_profile_created = BillingProfile.objects.new_or_get(request)
	address_qs = None
	if billing_profile is not None :
		if request.user.is_authenticated() :
			address_qs 			= Address.objects.filter(billing_profile=billing_profile)
		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)
		if shipping_address_id:
			order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
			del request.session["shipping_address_id"]
		if billing_address_id :
			order_obj.billing_address = Address.objects.get(id=billing_address_id)
			del request.session["billing_address_id"]
		if billing_address_id or shipping_address_id :
			order_obj.save()
	txnid  = order_obj
	amount = order_obj.total
	User   = request.user
	Name   = request.user.full_name
	Mobile = billing_profile.mobile_no
	product =cart_obj.products.all()
	cleaned_data = {'key': settings.PAYU_INFO['merchant_key'], 
                        'txnid':order_obj, 'amount': order_obj.total,
                        'productinfo': product,
                        'firstname': request.user.full_name,
                        'email': request.user,'phone':Mobile, 'udf1':'',
                        'udf2': '', 'udf3': '', 'udf4': '', 
                        'udf5': '', 'udf6': '','udf7': '','udf8': '',
                        'udf9': '', 'udf10': '',
                                                
                        }
	hash_o = generate_hash(cleaned_data)
	#Address = order_obj.billing_address
	print(Mobile)	
	if request.method == "POST" :
		#"check that order is done"
		is_done = order_obj.check_done()
		if is_done:
			order_obj.mark_paid()
			request.session['cart_items'] = 0
			del request.session['cart_id']
		txnid = order_obj
		print(txnid)
		print(request.user)
		print(request.user.full_name)
		
		#products=cart_obj.products.values_list('title', flat=True)


		#print(products)
		#product =cart_obj.products.all()
		#for product in cart_obj.products.all():
		#	print(product)
		#print(order_obj.total)
		#print(order_obj.cart_id)
		#print(product)
		
		return redirect("cart:success")

	context = {
		"object": order_obj,
		"billing_profile" :billing_profile,
		"login_form": login_form,
		"guest_form" : guest_form,
		"address_form": address_form,
 		"address_qs":address_qs,
 		"amount": amount,
 		"User" : User,
 		"Name"  : Name,
 		"Mobile" : Mobile,
 		"txnid" :txnid,
 		'key': settings.PAYU_INFO['merchant_key'],
 		'product' :product,
 		"hash_o" :hash_o,
 		#"Address":Address,
}
	#print(object)
	return render(request,"carts/checkout.html", context)


def checkout_done_view(request):
	return render(request,"carts/checkout-done.html",{})