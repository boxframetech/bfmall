from django.db import models
from django.db.models.signals import pre_save, post_save

from carts.models import Cart
from bfmall.utils import unique_order_id_generator

# Create your models here.
ORDER_STATUS_CHOICE = (
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded')
)


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, default='created', choices=ORDER_STATUS_CHOICE)
    delivery_total = models.DecimalField(default=10.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00,max_digits=9, decimal_places=2)

    def __str__(self):
        return self.order_id

    def update_order_total(self):
        cart_total = self.cart.total 
        delivery_total = self.delivery_total
        new_total = cart_total + delivery_total
        self.total = new_total
        self.save()
        return new_total


def order_id_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(order_id_pre_save_receiver, sender=Order)


# Cart and shipping total post save
def post_save_cart_total(sender, instance,created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total 
        cart_id = cart_obj.id 
        qs = Order.objects.filter(cart__id = cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_order_total()

post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance,created,*args,**kwargs):
    if created:
        instance.update_order_total()

post_save.connect(post_save_order, sender=Order)