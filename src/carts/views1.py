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
from django.contrib import messages
import logging, traceback
from django.core.urlresolvers import reverse
from billing.views import payment
from carts.constants import constant 
from carts.config import config 
import hashlib
from django.contrib.auth.decorators import login_required
from instamojo_wrapper import Instamojo

api = Instamojo(api_key='test_1b93bfd7be47ed56125b5b0be03',
                auth_token='test_c467499f81b9c9e6ffa11c12bbe')
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

class CartView(SingleObjectMixin, View):
	model = Cart
	template_name = "carts/view.html"

	def get_object(self, *args, **kwargs):
		self.request.session.set_expiry(0) #5 minutes
		cart_id = self.request.session.get("cart_id")
		if cart_id == None:
			cart = Cart()
			cart.tax_percentage = 0.075
			cart.save()
			cart_id = cart.id
			self.request.session["cart_id"] = cart_id
		cart = Cart.objects.get(id=cart_id)
		if self.request.user.is_authenticated():
			cart.user = self.request.user
			cart.save()
		return cart

	def get(self, request, *args, **kwargs):
		cart = self.get_object()
		item_id = request.GET.get("item")
		delete_item = request.GET.get("delete", False)
		flash_message = ""
		item_added = False
		if item_id:
			item_instance = get_object_or_404(Variation, id=item_id)
			qty = request.GET.get("qty", 1)
			try:
				if int(qty) < 1:
					delete_item = True
			except:
				raise Http404
			cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
			if created:
				flash_message = "Successfully added to the cart"
				item_added = True
			if delete_item:
				flash_message = "Item removed successfully."
				cart_item.delete()
			else:
				if not created:
					flash_message = "Quantity has been updated successfully."
				cart_item.quantity = qty
				cart_item.save()
			if not request.is_ajax():
				return HttpResponseRedirect(reverse("cart"))
				#return cart_item.cart.get_absolute_url()
		
		if request.is_ajax():
			try:
				total = cart_item.line_item_total
			except:
				total = None
			try:
				subtotal = cart_item.cart.subtotal
			except:
				subtotal = None

			try:
				cart_total = cart_item.cart.total
			except:
				cart_total = None

			try:
				tax_total = cart_item.cart.tax_total
			except:
				tax_total = None

			try:
				total_items = cart_item.cart.items.count()
			except:
				total_items = 0

			data = {
					"deleted": delete_item, 
					"item_added": item_added,
					"line_total": total,
					"subtotal": subtotal,
					"cart_total": cart_total,
					"tax_total": tax_total,
					"flash_message": flash_message,
					"total_items": total_items
					}

			return JsonResponse(data) 


		context = {
			"object": self.get_object()
		}
		template = self.template_name
		return render(request, template, context)

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


@login_required
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

	if request.method == "POST" :
		#"check that order is done"
		is_done = order_obj.check_done()
		if is_done:
			order_obj.mark_paid()
			request.session['cart_items'] = 0
			del request.session['cart_id']
		return redirect("cart:success")
	productlist= []
	for product in cart_obj.products.all():
		productlist.append(product)
	print(productlist)
	#print(product)
	data = {}
	txnid = order_obj
	hash_ = generate_hash(request,txnid)
	hash_string = get_hash_string(request, txnid)
	data["action"] = constant.PAYMENT_URL_TEST
	#print(data["action"])
	data["amount"] = order_obj.total
	#print(data["amount"])
	#print(txnid)
	data["key"] = config.KEY
	#data["txnid"] = txnid
	data["hash"] = hash_
	data["hash_string"] = hash_string
	data["firstname"] = request.user.full_name
	#data["email"] = request.user
	data["phone"] = billing_profile.mobile_no
	service_provider = constant.SERVICE_PROVIDER
	furl = request.build_absolute_uri(reverse("cart:payment_failure"))
	#sucess_url = 
	surl = request.build_absolute_uri(reverse("cart:payment_success"))
	cleaned_data = {
		'key' :config.KEY,"txnid" :order_obj,"amount":order_obj.total,
		"productinfo": productlist,
	}
	context = {
		"object": order_obj,
		"billing_profile" :billing_profile,
		"login_form": login_form,
		"guest_form" : guest_form,
		"address_form": address_form,
 		"address_qs":address_qs,
 		"amount": order_obj.total,
 		"User" : request.user,
 		"Name"  : request.user.full_name,
 		"Mobile" : billing_profile.mobile_no,
 		"txnid" :txnid,
		'key': config.KEY,
 		'product' :productlist,
 		'hash_':hash_,
 		'surl':surl,
 		'furl':furl,
 		'service_provider':service_provider,
 		#"surl" : sucess_url,
		
	}
	
	return render(request,"carts/checkout1.html", context)

def generate_hash(request,txnid):
    try:
        #get keys and SALT from dashboard once account is created.
        hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = get_hash_string(request,txnid)
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        print(generated_hash)
        return generated_hash
    except Exception as e:
         #log the error here.
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None
 
# create hash string using all the fields
def get_hash_string(request,txnid):
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	product=cart_obj.products.all()
	billing_profile ,billing_profile_created = BillingProfile.objects.new_or_get(request)
	order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)

	hash_string = config.KEY+"|"+str(txnid)+"|"+str(float(order_obj.total))+"|"+str(product)+"|"
	hash_string += str(request.user.full_name)+"|"+str(request.user)+"|"
	hash_string += "||||||||||"+config.SALT
	print(hash_string)
	return hash_string



def checkout_done_view(request):
	return render(request,"carts/checkout-done.html",{})


def payment_success(request):
    data = {}
    return render(request, "students/payment/success.html", data)

#@csrf_exempt
def payment_failure(request):
    data = {}
    return render(request, "students/payment/failure.html", data)