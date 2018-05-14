from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed,post_delete
from products.models import Product,Variation

User = settings.AUTH_USER_MODEL

# Create your models here.


class CartItem(models.Model):
    cart = models.ForeignKey("Cart")
    item = models.ForeignKey(Variation)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item.title

    def remove(self):
        return self.item.remove_from_cart()


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity
    if qty >= 1:
        price = instance.item.get_price()
        line_item_total = Decimal(qty) * Decimal(price)
        instance.line_item_total = line_item_total

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)



def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()

post_save.connect(cart_item_post_save_receiver, sender=CartItem)

post_delete.connect(cart_item_post_save_receiver, sender=CartItem)

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)
class Cart(models.Model):
    quantity    = models.PositiveIntegerField(default=1)
    items = models.ManyToManyField(Variation, through=CartItem)
    user        = models.ForeignKey(User, null=True, blank=True)
    products    = models.ManyToManyField(Product, blank=True)
    subtotal    = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    objects		= CartManager()
    
    def __str__(self):
        return str(self.id)

def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)




def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0 and instance.subtotal :
        instance.total = Decimal(instance.subtotal) * Decimal(1.08)
    else:
        instance.total = 0.00

pre_save.connect(pre_save_cart_receiver, sender=Cart)


