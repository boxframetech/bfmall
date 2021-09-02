from django.shortcuts import render,get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Product
from carts.models import Cart


# Create your views here.

class ProductList(ListView):
    queryset = Product.objects.all()
    template_name = 'products/allproduct.html'



class ProductDetail(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/productdetail.html'

    def get_object(self,*args,**kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        instance = get_object_or_404(Product, slug=slug)
        return instance

    def get_context_data(self, *args,**kwargs):
        context = super(ProductDetail, self).get_context_data(*args,**kwargs)
        cart_obj, new_obj = Cart.objects.new_cart_or_get_cart(self.request)
        context["cart"] = cart_obj
        return context
    