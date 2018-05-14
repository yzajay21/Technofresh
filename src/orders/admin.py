from django.contrib import admin
from .models import Order, ProductPurchase,OrderItem
from django.http import HttpResponse
from django.core.urlresolvers import reverse
# Register your models here.

admin.site.register(ProductPurchase)


def order_detail(obj):
    return '<a href="{}">View</a>'.format(reverse('orders:admin_order_detail',
                                                  args=[obj.id]))
order_detail.allow_tags = True

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

def order_pdf(obj):
    return '<a href="{}">PDF</a>'.format(reverse('orders:admin_order_pdf', args=[obj.id]))
    order_pdf.allow_tags = True
    order_pdf.short_description = 'PDF bill'

class OrderAdmin(admin.ModelAdmin):
    list_display = [order_pdf]
    # actions=[export_to_csv]
	#list_filter = ['status']
	#inlines = [OrderItemInline]

admin.site.register(Order)