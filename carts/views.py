from django.shortcuts import render
from .models import Cart


def carthome(request):
    cart_obj = Cart.objects.new_cart_or_get_cart(request)
    return render(request, 'cart_home.html',{})