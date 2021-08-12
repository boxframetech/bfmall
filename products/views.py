from django.shortcuts import render,get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Product
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