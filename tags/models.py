from django.db import models
from django.db.models.signals import pre_save
from bfmall.utils import unique_slug_generator
from products.models import Product

# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True,unique=True)
    product = models.ManyToManyField(Product, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

def tag_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_receiver, sender=Tag)
