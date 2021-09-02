from django.shortcuts import render,redirect
from products.models import Product
from .models import Cart

def carthome(request):
    cart_obj, new_obj = Cart.objects.new_cart_or_get_cart(request)
    products_in_cart = cart_obj.product.all()
    return render(request, 'cart_home.html',{'product_in_cart':products_in_cart,'cart':cart_obj}) 


def cart_update (request):
    product_id =request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('cart:carthome')    
    
        cart_obj, new_obj = Cart.objects.new_cart_or_get_cart(request)
        if product_obj in cart_obj.product.all():
            cart_obj.product.remove(product_id)
        else:
            cart_obj.product.add(product_id)
        request.session['num_products_in_cart'] = cart_obj.product.count()
    return redirect("cart:carthome")

