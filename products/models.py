import random
import os
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.db.models import Q
from bfmall.utils import unique_slug_generator


def get_file_extension(filename):
    base_name = os.path.basename(filename)
    name,extension = os.path.split(base_name)
    return name,extension

def upload_image_path(instance, filename):
    new_filename = random.randint(1,2222222)
    name,extension = get_file_extension(filename)
    final_filename = f'{new_filename}{extension}'
    return f'product/{new_filename}/{final_filename}'


# Model Managers
class ProductManager(models.Manager):
    def productsearch(self,query):
        lookups = (Q(title__icontains=query) | 
        Q(description__icontains=query)|
        Q(price__iexact=query)|
        Q(tag__title__icontains=query))
        return self.get_queryset().filter(lookups).distinct()


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True,unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2,max_digits=9, blank=True, null=True)
    main_image = models.ImageField(upload_to=upload_image_path)
    # image_1,image_2, image_3, category,size='small,medium,large,babies
    is_new = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse('product-detail',kwargs={'slug':self.slug})

    def __str__(self):
        return self.slug

def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)
