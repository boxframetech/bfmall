from django.shortcuts import render
from django.views.generic.list import ListView
from products.models import Product

# Create your views here.

class SearchProductView(ListView):
    template_name = 'search/productsearch.html'

    def get_context_data(self, *args,**kwargs):
        context = super(SearchProductView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self, *args,**kwargs):
        request = self.request
        query = request.GET.get('q',None)
        if query is not None:
            return Product.objects.productsearch(query)
        return Product.objects.filter(featured=True)
