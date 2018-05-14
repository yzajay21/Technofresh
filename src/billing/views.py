from django.shortcuts import render, render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
import datetime
import hashlib
import logging, traceback
from random import randint
from billing.constants import constants
from billing.config import config
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf
from django.utils.http import is_safe_url
from .models import BillingProfile
from carts.models import Cart
from orders.models import Order

def payment__(request):
	MERCHANT_KEY = "cPRE9tvJ"
	key="cPRE9tvJ"
	SALT = "Bo6ZChBPDS"
	PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
	action = ''
	posted={}
	# Merchant Key and Salt provided y the PayU.
	for i in request.POST:
		posted[i]=request.POST[i]
	hash_object = hashlib.sha256(b'randint(0,20)')
	txnid=order_obj
	hashh = ''
	posted['txnid']=txnid
	hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
	posted['key']=key
	hash_string=''
	hashVarsSeq=hashSequence.split('|')
	for i in hashVarsSeq:
		try:
			hash_string+=str(posted[i])
		except Exception:
			hash_string+=''			
		hash_string+='|'
	hash_string+=SALT    
	hashh=hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
	action =PAYU_BASE_URL
	if(posted.get("key")!=None and posted.get("txnid")!=None and posted.get("productinfo")!=None and posted.get("firstname")!=None and posted.get("email")!=None):
		return render(request,'billing/payment-method-form.html',{"posted":posted,"hashh":hashh,"MERCHANT_KEY":MERCHANT_KEY,"txnid":txnid,"hash_string":hash_string,"action":"https://test.payu.in/_payment" })
	else:
		return render(request,'billing/payment-method-form.html',{"posted":posted,"hashh":hashh,"MERCHANT_KEY":MERCHANT_KEY,"txnid":txnid,"hash_string":hash_string,})

def payment_(request):
	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
	if not billing_profile:
		return redirect("/cart")
	next_url = None
	next_ = request.GET.get('next')
	if is_safe_url(next_,request.get_host()):
		next_url =next_
	data = {}
	txnid = get_transaction_id()
	hash_ = generate_hash(request,txnid)
	hash_string = get_hash_string
	return render(request,'billing/payment-method-form.html',)




def payment(request):
	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
	if not billing_profile:
		return redirect("/cart") 

	cart_obj = None
	order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)
	data = {}
	txnid = order_obj
	#hash_ = generate_hash(request, txnid)
	#hash_string = get_hash_string(request, txnid)
    # use constants file to store constant values.
    # use test URL for testing
	#data["action"] = constants.PAYMENT_URL_LIVE 
	#data["amount"] = float(constants.PAID_FEE_AMOUNT)
	#data["productinfo"]  = constants.PAID_FEE_PRODUCT_INFO
	#data["key"] = config.KEY
	#data["txnid"] = order_obj
	#txnid = order_obj
	#
	print(txnid)
	#data["hash"] = hash_
	#data["hash_string"] = hash_string
	#data["firstname"] = request.session["billing_profile"]["name"]
	#data["email"] = request.session["billing_profile"]["email"]
	#data["phone"] = request.session["billing_profile"]["mobile"]
	#data["service_provider"] = constants.SERVICE_PROVIDER
	#data["furl"] = request.build_absolute_uri(reverse("students:payment_failure"))
	#data["surl"] = request.build_absolute_uri(reverse("students:payment_success"))
    
	return render(request, 'billing/payment-method-form.html', data)   
# generate the hash
def generate_hash(request, txnid):
    try:
        # get keys and SALT from dashboard once account is created.
        # hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = get_hash_string(request,txnid)
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        return generated_hash
    except Exception as e:
        # log the error here.
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None
 
# create hash string using all the fields
#def get_hash_string(request, txnid):
 #   hash_string = config.KEY+"|"+txnid+"|"+str(float(constants.PAID_FEE_AMOUNT))+"|"+constants.PAID_FEE_PRODUCT_INFO+"|"
 #   hash_string += request.session[""]["name"]+"|"+request.session["billing_profile"]["email"]+"|"
  #  hash_string += "||||||||||"+config.SALT
 
  #  return hash_string
 
# generate a random transaction Id.
def get_transaction_id():
    hash_object = hashlib.sha256(str(randint(0,9999)).encode("utf-8"))
    # take approprite length
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid   
def payment_method_view(request):
	MERCHANT_KEY = ""
	key=""
	SALT = ""
	PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
	action = ''
	posted={}

	if request.method =="POST":
		print(request.POST)

	return render(request,'billing/payment-method-form.html',{})
@csrf_protect
@csrf_exempt
def success(request):
	c = {}
	c.update(csrf(request))
	status=request.POST["status"]
	firstname=request.POST["firstname"]
	amount=request.POST["amount"]
	txnid=request.POST["txnid"]
	posted_hash=request.POST["hash"]
	key=request.POST["key"]
	productinfo=request.POST["productinfo"]
	email=request.POST["email"]
	salt="GQs7yium"
	try:
		additionalCharges=request.POST["additionalCharges"]
		retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	except Exception:
		retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
	if(hashh !=posted_hash):
		print ("Invalid Transaction. Please try again")
	else:
		print ("Thank You. Your order status is ", status)
		print ("Your Transaction ID for this transaction is ",txnid)
		print ("We have received a payment of Rs. ", amount ,". Your order will soon be shipped.")
	return render_to_response('sucess.html',RequestContext(request,{"txnid":txnid,"status":status,"amount":amount}))


@csrf_protect
@csrf_exempt
def failure(request):
	c = {}
	c.update(csrf(request))
	status=request.POST["status"]
	firstname=request.POST["firstname"]
	amount=request.POST["amount"]
	txnid=request.POST["txnid"]
	posted_hash=request.POST["hash"]
	key=request.POST["key"]
	productinfo=request.POST["productinfo"]
	email=request.POST["email"]
	salt=""
	try:
		additionalCharges=request.POST["additionalCharges"]
		retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	except Exception:
		retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
	if(hashh !=posted_hash):
		print ("Invalid Transaction. Please try again")
	else:
		print ("Thank You. Your order status is ", status)
		print ("Your Transaction ID for this transaction is ",txnid)
		print ("We have received a payment of Rs. ", amount ,". Your order will soon be shipped.")
	return render_to_response("Failure.html",RequestContext(request,c))