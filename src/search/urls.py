from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


from products.views import ProductListView
from .views import SearchProductListView
urlpatterns = [
    # Examples:
    # url(r'^$', 'newsletter.views.home', name='home'),
    #url(r'^$', 'products.views.product_list', name='products'),
    url(r'^$', SearchProductListView.as_view(), name='query'),
]