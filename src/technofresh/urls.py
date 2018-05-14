"""technofresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import LogoutView
from .views import home_page,about
from banner.views import photo_list
from offersimages.views import offers_list
from addresses.views import checkout_address_create_view,checkout_address_reuse_view
from analytics.views import SalesView,SalesAjaxView
from accounts.views import LoginView, RegisterView,GuestRegisterView
from products.views import product_detail_view, ProductFeaturedDetailView,ProductFeaturedListView
from carts.views import cart_detail_api_view
from billing.views import payment,success,failure
from django.views.generic import RedirectView
#from carts.views import 
urlpatterns = [

    url(r'^$',home_page,name='home'),
    url(r'^about/$',about,name='about'),
    url(r'^banners/$',photo_list,name='photo_list'),
    url(r'^offers/$',offers_list,name='offers_list'),
    #url(r'^(?P<slug>[-\w]+)$',AlbumDetail.as_view(),name='album'),
    url(r'^accounts/$', RedirectView.as_view(url='/login')),
    url(r'^account/', include("accounts.urls",namespace='account')),
    url(r'^accounts/', include("accounts.passwords.urls")),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^register/guest/$',GuestRegisterView.as_view(),name='guest_register'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^checkout/address/create/$',checkout_address_create_view,name='checkout_address_create'),
    url(r'^checkout/address/reuse/$',checkout_address_reuse_view,name='checkout_address_reuse'),
    url(r'^api/cart/$',cart_detail_api_view,name='api-cart'),
    #url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^cart/', include("carts.urls",namespace='cart')),
    url(r'^billing/payment/$',payment, name="payment"),
    url(r'^payment/success$', success, name="payment_success"),
    url(r'^payment/failure$', failure, name="payment_failure"),
    url(r'^orders/', include("orders.urls",namespace='orders')),
    url(r'^products/', include("products.urls",namespace='products')),
    url(r'^products-fbv/(?P<pk>\d+)/$',product_detail_view),
    url(r'^search/', include("search.urls",namespace='search')),
    url(r'^categories/', include('products.urls_categories')),
    #url(r'^$',HomepageView.as_view(),name ='HomepageView')
    url(r'^analytics/sales/$', SalesView.as_view(),name='sales-analytics'),
    url(r'^analytics/sales/data/$',SalesAjaxView.as_view(),name='sales-analytics-data'),
    url(r'^featured/$', ProductFeaturedListView.as_view(), name='products'),
    url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view(), name='products'),
    url(r'^admin/', admin.site.urls),
    #url(r'^paytm/', include('paytm.urls')),
]
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
