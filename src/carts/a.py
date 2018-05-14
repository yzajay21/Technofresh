
Python - Django
Expert , professional,personal and affordable web Development framework is one and only DJANGO ( Python web development framework )

Saturday, April 4, 2015
Payu payment gateway integration with Django

                                  Payu Payment  Gateway Integration With Django 



  Introduction  

       
        This Blog is describes the steps for technical integration process between merchant 
website and PayU Payment Gateway for enabling online transactions. This Blog is covered payment gateway integration with Django Framework.



PayU Payment Gateway




PayU offers electronic payment services to merchant website through its partnerships with various banks and payment instrument companies. Through PayU, the customers would be able to make  




Electronic payments through a variety of modes which are mentioned below:


Credit cards
Debit cards
Online net banking accounts
EMI payments
Cash Cards
Email Invoicing
IVR
Cash on Delivery (COD)


PayU also offers an online interface (known as PayU Dashboard) where the merchant has access to various features like viewing all the transaction details, settlement reports, analytical reports etc.Through this interface, the merchant can also execute actions like capturing, cancelling andrefunding the transactions. This online interface can be accessed through Payu using the username and password provided to you.




Payment Gateway Process Flow 




      








PayU payment Gateway Process Flow


 



Steps for Integration Process


The steps for integrating with PayU can technically be described as below:




1) To start off the integration process, you would be provided a test setup by PayU where you

would be given a test merchant account and test credit card credentials to have a first-hand
experience of the overall transaction flow. Here, you need to make the transaction request
on our test server (and not the production server). Once your testing is complete, then only
you will be ready to move to the PayU production server.



2) To initiate a transaction, the merchant needs to generate a POST REQUEST - which must

consist of mandatory and optional parameters mentioned in the later section. This POST
REQUEST needs to be hit on the below mentioned PayU URLs:



For PayU Test Server:

     POST URL: https://test.payu.in/_payment


For PayU Production (LIVE) Server:

     POST URL: https://secure.payu.in/_payment



3) In the merchant initiated POST REQUEST, one of the mandatory parameters is named as

hash. The details of this hash parameter have been covered in the later section. But it is
absolutely critical for the merchant to calculate the hash correctly and post to us in the
request.



4) When the transaction POST REQUEST hits the PayU server, a new transaction entry is

created in the PayU Database. To identify each new transaction in the PayU Database, a
unique identifier is created every time at PayU’s end. This identifier is known as the PayU ID
(or MihPayID).



5) With the POST REQUEST, customer would be re-directed to PayU’s payment page. Customer now selects the particular payment option on PayU’s page (Credit Card/Debit Card/NetBanking etc) and clicks on ‘Pay Now’. PayU re-directs the customer to the chosen bank. Thecustomer goes through the necessary authorization/authentication process at bank’s login page, and the bank gives the success/failure response back to PayU.




6) PayU marks the transaction status on the basis of response received from Bank. PayU

provides the final transaction response string to the merchant through a POST RESPONSE.
The parameters in this response are covered in the subsequent sections.



7) In the POST RESPONSE sent by PayU, you would receive the final status of the transaction.

You will receive the hash parameter here also. Similar to step 3, it is absolutely crucial to
verify this hash value at your end and then only accept/reject the invoice order. This is done
to strictly avoid any tampering attempt by the user.


Note : 


Test URL: The Test URL is provided to PayU merchants to test the integration of their  server with that of PayU or Bank. It is understood that since this is merely a Test URL, the Merchant should not treat any transactions done on this Test server as live and should not deliver the products/services with respect to any such test transactions even in the case your server receive a successful transaction confirmation from PayU/Bank.

Merchants are herein forth requested to set up required control checks on their               (merchant) systems/servers to ensure that only those transactions should get routed to the  PayU test server which are initiated with sole intention of test the environment.





PayU payment Gateway Integration with DJANGO





Onces you create the account With Payu they will provide SALT and KEY we need this two

credentials for the integration. 



Parameters to be posted by Merchant to PayU in Transaction Request:

 key (Mandatory)
txnid (Mandatory)
amount(Mandatory)
productinfo(Mandatory)
firstname(Mandatory)
email (Mandatory)
phone (Mandatory)
lastname
Udf1-Udf5
address1
city
state
country
zipcode
surl(Mandatory)
furl(Mandatory)
curl(Mandatory)
hash(Checksum)Mandatory)     :sha512(key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5||||||SALT)

Udf : user defind field
Surl : Sucess URL ( Success redirection URLs ) 
Furl : Failure URL ( Failure redirectio URLs )
Curl : Cancelation URL( cancelation URLs)

Integration Steps 

Settings.py in your project

Add this Section.

####### Pay yu payment integration information###################





PAYU_INFO = {
              'merchant_key': "test merchant key",

             'merchant_salt': "test merchant salt",
             # for production environment use 'https://secure.payu.in/_payment'
             'payment_url': 'https://test.payu.in/_payment',
             'surl':'http://example.com/pay-success/',
             'furl':'http://example.com/failure/',
             'curl':'http://example.com/cancel/',
            }

###################End payment info ###############################


models.py 

from django.db import models
from uuid import uuid4

from uuid import UUID
import uuid
from django_extensions.db.fields import UUIDField


class MyOrder(models.Model):

    items = models.ManyToManyField(OrderItem, null=True, blank=True)
    order_date = models.DateField(auto_now=True)
    buyer = models.ForeignKey(Buyer)

    txnid = models.CharField(max_length=36, primary_key=True)
    amount = models.FloatField(null=True, blank=True,default=0.0)
    hash = models.CharField(max_length=500, null=True, blank=True)
    billing_name = models.CharField(max_length=500, null=True, blank=True)
    billing_street_address = models.CharField(max_length=500, null=True, blank=True)
    billing_country = models.CharField(max_length=500, null=True, blank=True)
    billing_state = models.CharField(max_length=500, null=True, blank=True)
    billing_city = models.CharField(max_length=500, null=True, blank=True)
    billing_pincode = models.CharField(max_length=500, null=True, blank=True)
    billing_mobile = models.CharField(max_length=500, null=True, blank=True)
    billing_email = models.CharField(max_length=500, null=True, blank=True)

    shipping_name = models.CharField(max_length=500, null=True, blank=True)
    shipping_street_address = models.CharField(max_length=500, null=True, blank=True)
    shipping_country = models.CharField(max_length=500, null=True, blank=True)
    shipping_state = models.CharField(max_length=500, null=True, blank=True)
    shipping_city = models.CharField(max_length=500, null=True, blank=True)
    shipping_pincode = models.CharField(max_length=500, null=True, blank=True)
    shipping_mobile = models.CharField(max_length=500, null=True, blank=True)
    shipping_rate = models.FloatField(null=False, blank=False, default=0.0)
    status = models.CharField(max_length=500, null=True, blank=True)
    shipping_email = models.CharField(max_length=500, null=True, blank=True)

    payment_method = models.CharField(max_length=1000,verbose_name='Payment-method')
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)



Views.py 

When the user click on the checkout button in your online shop,add this code add in to the that views.py


from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
import hashlib
from django.conf import settings
from .util import generate_hash

@login_required

def buy_order(request):
    """ funtion for save all orders and genarate order id"""
    items = None
    orderitem = None
    extra = False
    if request.user.is_authenticated() and not request.user.is_staff:
        user = Buyer.objects.get(id=request.user.id)
        try:
            cart = Cart.objects.get(buyer=request.user)
        except ObjectDoesNotExist:
            extra = "You dont have any item in your cart"
            variables = RequestContext(request, {'extra': extra})
            return render_to_response('home.html', variables)
            total_amount = OrderItem.objects.filter(buyer=request.user)
            item_list = []
            rg = request.POST.get
            if cart:
                if request.POST:
                    rg('shippingnme')and rg('shippingaddress') and rg('shippingemail') and                                                   rg('shippingpostel') and rg('shippingcity') and rg('shippingcountry') and                                                 rg('shippingcountry') rg('shippingphone'):
                    try:
                        """store all products to myorder model and genarate order id for the order"""
                        myorder = MyOrder(buyer=user)
                        # billing User
                        myorder.buyer = user
                        # myorder of Billing  Address
                        myorder.billing_name = request.POST.get('billingname')
                        myorder.billing_street_address = request.POST.get(
                            'billingaddress')
                        myorder.billing_pincode = request.POST.get('billingpostel')
                        myorder.billing_city = request.POST.get('billingcity')
                        myorder.billing_country = request.POST.get('billingcountry')
                        myorder.billing_state = request.POST.get('billingstate')
                        myorder.billing_mobile = request.POST.get('billingphone')
                        myorder.billing_email = request.POST.get('billingemail')

                        # myorder of shipping Address
                        myorder.shipping_pincode = request.POST.get('shippingpostel')
                        myorder.shipping_name = request.POST.get('shippingnme')
                        myorder.shipping_street_address = request.POST.get(
                            'shippingaddress')
                        myorder.shipping_city = request.POST.get('shippingcity')
                        myorder.shipping_state = request.POST.get('shippingstate')
                        myorder.shipping_mobile = request.POST.get('shippingphone')
                        myorder.shipping_country = request.POST.get('shippingcountry')
                        myorder.shipping_email = request.POST.get('shippingemail')
                        if request.POST.get('paymentmethod'):
                            myorder.payment_method = request.POST.get('paymentmethod')
                        else:
                            myorder.payment_method = 'ON'
                        myorder.comment =  request.POST.get('prodcutmessage')

                        print "my messages "
                        print myorder.comment

                      # payment_method
                      # comment
                        myorder.txnid = str(uuid.uuid1().int >> 64)
                        myorder.save()
                        """genarate an oredr id, the below loop will add all orderd product to the                                               order"""

                        for order in cart.items.all():
                            orderitem = OrderItem()
                            orderitem.buyer = order.buyer
                            orderitem.product_id = order.product.id
                            orderitem.product_title = order.product.name
                            orderitem.weight = order.product.weight
                            orderitem.product_price = order.product.gross_pay()[0]
                            orderitem.total_amount = order.total
                            orderitem.quantity = order.quantity
                            orderitem.save()
                            myorder.items.add(orderitem)
                        total_details = total_price_fu(myorder)

                        """ After adding products to order assigning a
                        transaction amount and shipping charge to the order"""
                        myorder = MyOrder.objects.get(pk=myorder.txnid)

                        myorder.amount = total_details['grand_total']
                        myorder.shipping_rate = total_details['shipping_rate']

                        """Assigning all values for hash funtion for payu"""

                        cleaned_data = {'key': settings.PAYU_INFO['merchant_key'], 'txnid':                                                                   myorder.txnid, 'amount': myorder.amount, 'productinfo':                                                                   orderitem.product_title,'firstname': myorder.billing_name, 'email':                                                            myorder.billing_email, 'udf1': ' '', 'udf2': '', 'udf3': '', 'udf4': '', 'udf5': '', 'udf6': '',                                   'udf7': '',  'udf8': '', 'udf9': '', 'udf10': ''}

                        """ the generate_hash funtion is use for genarating hash
                         value from cleaned_data"""
                        hash_o = generate_hash(cleaned_data)
                        myorder.hash =hash_o
                        myorder.save()

                            return HttpResponse(
                                         """
                                              <html>
                                                  <head><title>Redirecting...</title></head>
                                                  <body>
                                                  <form action='%s' method='post' name="payu">
                                                      <input type="hidden" name="firstname" value="%s" />
                                                      <input type="hidden" name="surl" value="%s" />
                                                      <input type="hidden" name="phone" value="%s" />
                                                      <input type="hidden" name="key" value="%s" />
                                                      <input type="hidden" name="hash" value =
                                                      "%s" />
                                                      <input type="hidden" name="curl" value="%s" />
                                                      <input type="hidden" name="furl" value="%s" />
                                                      <input type="hidden" name="txnid" value="%s" />
                                                      <input type="hidden" name="productinfo" value="%s" />
                                                      <input type="hidden" name="amount" value="%s" />
                                                      <input type="hidden" name="email" value="%s" />
                                                      <input type="hidden" value="submit">
                                                  </form>
                                                  </body>
                                                  <script language='javascript'>
                                                  window.onload = function(){
                                                   document.forms['payu'].submit()
                                                  }
                                                  </script>
                                              </html>

                                          """ % (settings.PAYU_INFO['payment_url'],
                                                 myorder.billing_name, settings.PAYU_INFO[
                                                     'surl'],
                                                 myorder.billing_mobile,
                                                 settings.PAYU_INFO['merchant_key'],
                                                 hash_o,
                                                 settings.PAYU_INFO['curl'],
                                                 settings.PAYU_INFO['furl'],
                                                 myorder.txnid,
                                                 orderitem.product_title,
                                                 myorder.amount,
                                                 myorder.billing_email
                                                 )
                                        )



util.py 


from hashlib import sha512
from django.conf import settings
KEYS = ('key', 'txnid', 'amount', 'productinfo', 'firstname', 'email',
        'udf1', 'udf2', 'udf3', 'udf4', 'udf5',  'udf6',  'udf7', 'udf8',
        'udf9',  'udf10')

def generate_hash(data):
    keys = ('key', 'txnid', 'amount', 'productinfo', 'firstname', 'email',
            'udf1', 'udf2', 'udf3', 'udf4', 'udf5',  'udf6',  'udf7', 'udf8',
            'udf9',  'udf10')
    hash = sha512('')
    for key in KEYS:
        hash.update("%s%s" % (str(data.get(key, '')), '|'))
    hash.update(settings.PAYU_INFO.get('merchant_salt'))
    return hash.hexdigest().lower()

def verify_hash(data, SALT):
    keys.reverse()
    hash = sha512(settings.PAYU_INFO.get('merchant_salt'))
    hash.update("%s%s" % ('|', str(data.get('status', ''))))
    for key in KEYS:
        hash.update("%s%s" % ('|', str(data.get(key, ''))))
    return (hash.hexdigest().lower() == data.get('hash'))

Once the transaction comple we will get a set of query set in the form of Json Dictionary 

eg :

<QueryDict: {u'name_on_card': [u'sda'], u'net_amount_debit': [u'10'], u'payment_source': [u'payu'], u'udf10': [u''], u'issuing_bank': [u'AXIS'], u'field7': [u''], u'udf3': [u''], u'unmappedstatus': [u'captured'], u'card_type': [u'VISA'], u'PG_TYPE': [u'HDFC'], u'addedon': [u'2014-10-20 18:50:38'], u'city': [u''], u'field8': [u''], u'field9': [u'SUCCESS'], u'field2': [u'999999'], u'field3': [u'2819211501842931'], u'field1': [u'429367481506'], u'field6': [u''], u'zipcode': [u''], u'field4': [u'-1'], u'field5': [u''], u'productinfo': [u'adsdsd'], u'address1': [u''], u'discount': [u'0.00'], u'email': [u'arungopi.online@gmail.com'], u'cardhash': [u'This field is no longer supported in postback params.'], u'udf4': [u''], u'status': [u'success'], u'bank_ref_num': [u'2819211501842931'], u'error_Message': [u'No Error'], u'hash': [u'2f274b1f5ca4004db6eac28f317f9e1bff0105b7c14039ac663b9fcf50dc5910f20eaae33a938ef7989d0ecd28c6557d41f396229c21f18f4fb6f01a562ba667'], u'firstname': [u'Arun'], u'state': [u''], u'lastname': [u''], u'address2': [u''], u'error': [u'E000'], u'phone': [u'8113943843'], u'cardnum': [u'512345XXXXXX2346'], u'key': [u'gtKFFx'], u'bankcode': [u'CC'], u'mihpayid': [u'403993715510265476'], u'country': [u''], u'txnid': [u'9470041433304666596'], u'udf1': [u''], u'amount': [u'10.00'], u'udf2': [u''], u'udf5': [u''], u'mode': [u'CC'], u'udf7': [u''], u'udf6': [u''], u'udf9': [u''], u'udf8': [u'']}>

According to status in the callback queryset from the Payu. The url automaticaly redirect to the appropriate views( we mentioned this urls in settings.py and we pass the urls in the buyorder views )  



# order sucess mail views
@csrf_exempt
def success(request):
       ========================
       do what functionality you need 
     =========================



@csrf_exempt

def failure(request):
       ========================

       do what functionality you need 

     =========================



@csrf_exempt

def cancel(request):
       ========================

       do what functionality you need 

     =========================

    

I hope you all understood the payu payment gateway integration. this is working fine for me you can check the working with this link Electrotrendz online shop


                        <===============THANK YOU ============>














Posted by renjith s raj at 12:41 PM 
Email This
BlogThis!
Share to Twitter
Share to Facebook
Share to Pinterest

27 comments:

Shawn DenyAugust 21, 2015 at 3:15 AM
This Blog is covered payment gateway integration with Django Framework.
payment gateway

Reply
Replies

RENJITH S RAJSeptember 8, 2015 at 8:17 PM
yes off course @Shawn Deny


Renjith S RajMarch 30, 2017 at 9:51 AM
please follow this package.

https://pypi.python.org/pypi/payu_biz/1.2.1


Renjith S RajApril 23, 2017 at 6:50 AM
https://github.com/renjithsraj/django_payubiz

Reply

Amir ShahOctober 16, 2015 at 12:36 AM
Hello raj, thanks for the logic. I used it but i m getting transaction failed,
i checked it, it is because the hash sent by payu and the one which we computed in verify hash method using reversed keys is not matching, please suggest the solution soon

Reply
Replies

renjith s rajOctober 16, 2015 at 8:14 AM
Hi Amir,
Have you added all the required field , for hashing


renjith s rajOctober 16, 2015 at 8:15 AM
if you need more help , just come to the skype , i will help you to sort it out.


renjith s rajOctober 16, 2015 at 8:27 AM
djangorenjith

Reply

Vadivel GunasekarenFebruary 3, 2016 at 11:40 PM
Hello Renjith, Myself also getting same transaction error.While integrating web page into production payumoney payment gateway.But it works fine in test environment
Error Reason
You seem to be using an incorrect key or salt value.

Reply
Replies

Renjith S RajMarch 30, 2017 at 9:51 AM
please follow https://pypi.python.org/pypi/payu_biz/1.2.1

Reply

oaulakhMarch 17, 2016 at 8:55 PM
hi, i would love if you can check this indentation and alot of stuff you make me confused about, like multiple imports, i wish payu official django kit would work but it's also thrwoing error because of some module resource which still occur if you do install that module. so i think maybe you can make this tutorial alot better and help alot of people. maybe not alot of people use django in india and payment gateway like payu but still we can make it much more available to other too. but please help me understand like why you importing useless stuff like uuid which you no teven using in model and also why you are importing objectnotexist which you can also use straing exception. can you help me i want to make this tutorial avaible to everyone out there who looking django integration with payu gateway.

thanks by the way
have a nice day :)

Reply
Replies

Renjith RajApril 5, 2016 at 3:46 AM
you can connect me in skype : djangorenjith


Renjith RajApril 5, 2016 at 3:51 AM
i will make perfect

Reply

Priya BhadkeSeptember 9, 2016 at 12:27 AM
Hi, need help in payumoney integration as it is giving me error like this..

Error Reason
Transaction failed due to incorrectly calculated hash parameter.

Corrective Action
Please ensure that the hash used in transaction request is calculated using the correct formula. Please note the correct formula for calculating the value of hash:
sha512(key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5||||||SALT)

Based on above formula and applying for this transaction, hash should be calculated as mentioned below :
hash = sha512(gtKFFx|77430fe3cf66ecb2650b|399|this is product|vikash|vikash.g@vsynergize.com|||||||||||eCwWELxi) = Array
As seen above, correct hash value should have been - Array

But the hash posted in the transaction request from your end was - d58556d31a83a0aa90ebcd08d27c20c5dcc1f30d31e9ca71d9b206fef34762a36f25167445596e9e98ee713516ea00dd317793647bdc78522bad3be94bf51aa9

Please re-initiate a transaction with correctly calculated hash value

Reply

Abiya CarolDecember 13, 2016 at 10:37 PM
Django is an excellent framework for Python. While it may not get as much ink as other popular frameworks like Rails, it is just as much a polished framework as any of the rest. It puts plenty of emphasis on the DRY principle (Don't Repeat Yourself) in clean coding by automating many of the processes in programming.

aws training in chennai

Reply
Replies

Renjith S RajMarch 30, 2017 at 9:52 AM
please follow https://pypi.python.org/pypi/payu_biz/1.2.1

Reply

Shailesh GehlotJanuary 14, 2017 at 9:19 PM
hi, am getting the same error as priya bhdake mentioned in above comment like
Hi, need help in payumoney integration as it is giving me error like this..

Error Reason
Transaction failed due to incorrectly calculated hash parameter.

Corrective Action
Please ensure that the hash used in transaction request is calculated using the correct formula. Please note the correct formula for calculating the value of hash:
sha512(key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5||||||SALT)

Based on above formula and applying for this transaction, hash should be calculated as mentioned below :
hash = sha512(gtKFFx|77430fe3cf66ecb2650b|399|this is product|vikash|vikash.g@vsynergize.com|||||||||||eCwWELxi) = Array
As seen above, correct hash value should have been - Array

But the hash posted in the transaction request from your end was - d58556d31a83a0aa90ebcd08d27c20c5dcc1f30d31e9ca71d9b206fef34762a36f25167445596e9e98ee713516ea00dd317793647bdc78522bad3be94bf51aa9

Please re-initiate a transaction with correctly calculated hash value

please Help me

Reply
Replies

Renjith S RajMarch 30, 2017 at 9:52 AM
please follow https://pypi.python.org/pypi/payu_biz/1.2.1

Reply

Shailesh GehlotJanuary 14, 2017 at 10:14 PM
am stuck in generating Hash please help me out

Reply

Shailesh GehlotFebruary 10, 2017 at 9:40 AM
No one is here to help

Reply
Replies

Renjith S RajMarch 28, 2017 at 7:23 PM
Hi Shailesh, I have forget the credentials so only I didnt noticed .


Shailesh GehlotApril 24, 2017 at 11:28 AM
ITS OK :) THNKS FOR REPLY

Reply

Renjith S RajMarch 28, 2017 at 7:24 PM
Hi Every one, The blog account password i got forgeted , so please you can go forward with recently created package for payu.

https://github.com/renjithsraj/django_payubiz

Reply

Renjith S RajMarch 30, 2017 at 9:53 AM
please follow https://pypi.python.org/pypi/payu_biz/1.2.1

Reply

Somnath DasApril 10, 2017 at 6:41 PM
How to get test setup by PayU where you would be given a test merchant account and test credit card credentials????????

Reply
Replies

Renjith S RajApril 23, 2017 at 6:49 AM
please reffer : https://github.com/renjithsraj/django_payubiz

Reply

sunitha vishnuNovember 26, 2017 at 9:39 PM
Really it was an awesome article...very interesting to read..You have provided an nice article....Thanks for sharing..
Android Training in Chennai
Ios Training in Chennai

Reply

Newer Post Older Post Home
Subscribe to: Post Comments (Atom)

 
About Me
My photo
renjith s raj  

I am a python developer passionate to become a dedicated python django developer and open source promoter. I am having 4 plus years of experience in python.

I have well experience in almost all python frameworks like django, flask,bottle,scrapy and successfully completed more than 180 plus projects.

Worked on projects in e-commerce, web-portals, API integration and Scrapping data from different websites.

I have contributed a couple of packages to django.

I am also having a good team specialized in :

ColdFusion frameworks(Coldbox, Railo,FW1), Phonegap, AngularJS, Nodejs, WordPress, php and etc. Expertise in Front end design and creation using HTML5 , CSS3, Bootstrap, Topcoat, Angular Js, HTML, CSS, JavaScript, jQuery, Ajax.

Database Development: PostgreSQL, MySQL, sqlite, MongoDB File Management expert includes Github, SVN.

My github url :https://github.com/renjithsraj/

My blog: my-django-python.blogspot.in

My skype : djangorenjith

View my complete profile
Blog Archive
▼  2015 (26)
►  December (1)
►  November (2)
►  October (4)
►  September (7)
►  July (1)
►  June (1)
►  May (2)
▼  April (4)
Host your Django Website In Ubuntu Server With Ngn...
Django Custom User Authentication Backend
Payu payment gateway integration with Django
How to Export Your Data as CSV, XLS, or XLSX in Dj...
►  March (4)
Follow by Email

Email address...
Renjith S Raj. Simple theme. Powered by Blogger.
