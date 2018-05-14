from django.conf.urls import url

from .views import (
        cart_home, 
        cart_update, 
        checkout_home,
        checkout_done_view,
       # payment_success,
       # payment_failure,
        #list_payments,
        payment
        )

urlpatterns = [

    url(r'^$', cart_home, name='home'),
    url(r'^checkout/success/$', checkout_done_view, name='success'),
    url(r'^checkout/$', checkout_home, name='checkout'),
    url(r'^update/$', cart_update, name='update'),
    #url(r'^list/', list_payments, name="list"),
    url(r'^payment/', payment, name="payment"),

	#url(r'^payment/success$', payment_success, name="payment_success"),
	#url(r'^payment/failure$',payment_failure, name="payment_failure"),
]