from django.conf.urls import url

from .views import (
        AccountHomeView,
        AccountEmailActivateView,
        UserDetailUpdateView,

        )
from products.views import UserProductHistoryListView

urlpatterns = [
    url(r'^$', AccountHomeView.as_view(), name='home'),
    url(r'^details/$', UserDetailUpdateView.as_view(), name='user-update'),
    url(r'^history/products$',UserProductHistoryListView.as_view(),name='user-product-history'),
    url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivateView.as_view(), name='email-activate'),
    url(r'^email/resend-activation/$', 
            AccountEmailActivateView.as_view(), 
            name='resend-activation'),
]