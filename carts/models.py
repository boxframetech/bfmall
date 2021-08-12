from django.db import models
from django.conf import settings
from products.models import Product


User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_cart_or_get_cart(self,request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user  = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create_new_cart(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def create_new_cart(self,user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.DO_NOTHING)
    product = models.ManyToManyField(Product, blank=True) 
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)