from django.conf.urls import url

from .views import (
        OrderListView,
        OrderDetailView,
        #admin_order_detail,
       # admin_order_pdf
        )


urlpatterns = [
    url(r'^$', OrderListView.as_view(), name='list'),
    url(r'^(?P<order_id>[0-9A-Za-z]+)/$', OrderDetailView.as_view(), name='detail'),
    #url(r'^admin/order/(?P<order_id>\d+)/$',admin_order_detail, name='admin_order_detail'),
   # url(r'^admin/order/(?P<order_id>\d+)/pdf/$',admin_order_pdf,name='admin_order_pdf'),
]