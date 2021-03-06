from django.http import HttpResponse, HttpResponseRedirect
from carts.apitest import apitest
from django.urls import reverse
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
from instamojo_wrapper import Instamojo
from django.contrib.auth.decorators import login_required
# Create your views here.


api = Instamojo(api_key=apitest.API_KEY, auth_token=apitest.AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')
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
	
	context = {
		"object": order_obj,
		"billing_profile" :billing_profile,
		"login_form": login_form,
		"guest_form" : guest_form,
		"address_form": address_form,
 		"address_qs":address_qs
		
	}
	return render(request,"carts/checkout.html", context )


def checkout_done_view(request):
	return render(request,"carts/checkout-done.html",{})


def list_payments(request):
    # Create a new Payment Request
    response = api.payment_requests_list()

    # Loop over all of the payment requests
    h = "<div><table><tr><th>ID</th><th>amount</th><th>Purpose</th><th>status</th></tr>"
    for payment_request in response['payment_requests']:
        h += "<tr>"
        h += "<td>" + payment_request['id'] + "</td>"
        h += "<td>" + payment_request['amount'] + "</td>"
        h += "<td>" + payment_request['purpose'] + "</td>"
        h += "<td>" + payment_request['status'] + "</td>"
        h += "</tr>"

    h += "</table></div>"

    return HttpResponse(h)