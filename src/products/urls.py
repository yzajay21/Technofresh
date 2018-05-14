
from django.conf.urls import include, url



from .views import ProductDetailView, ProductDetailSlugView, ProductListView,VariationListView,ProductFeaturedListView, ProductFeaturedDetailView, product_detail_view

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$',ProductDetailView.as_view()),
    url(r'^(?P<slug>[\w-]+)/$',ProductDetailSlugView.as_view(), name='detail'),
    url(r'^$', ProductFeaturedListView.as_view(), name='featured-products'),
    
    url(r'^(?P<pk>\d+)/$',ProductDetailView.as_view()),
    url(r'^(?P<pk>\d+)/inventory/$', VariationListView.as_view(), name='product_inventory'),
    #url(r'^(?P<id>\d+)', product_detail_view, name='product-fbv'),


]