from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from products.models import Product

# Create your views here.

class HomepageView(ListView):
    queryset = Product.objects.filter(featured=True)
    template_name = 'index.html'

