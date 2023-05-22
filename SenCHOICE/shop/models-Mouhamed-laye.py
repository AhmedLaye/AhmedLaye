from django.utils import timezone
from email.mime import image
from django.db import models
from distutils.command.upload import upload
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.urls import reverse
from django.utils.text import slugify
import pandas




class User(AbstractUser):
    adresse=models.CharField(null=True, max_length=100)
    pays=models.CharField(null=True, max_length=100)
    ville=models.CharField(null=True, max_length=100)
   
class Category(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now=True)
    banner=models.ImageField(upload_to="image_banner")
    image=models.ImageField(upload_to="image_category_carre")
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name    

class slider(models.Model):
    image=models.ImageField(upload_to="image_slider")
    def __str__(self):
        return "image"
        

class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True)
    category = ForeignKey(Category, related_name='categorie', on_delete=models.CASCADE) 
    image= models.ImageField(upload_to="image_produit")
    stock=models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True)
    slug=models.CharField(max_length=200, null=True, blank=True)
    date_expiration=models.DateField(null=True, blank=True)
    class Meta:
        ordering = ['category']  

    def __str__(self):
        return self.title           

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug":self.slug})
    
    def save(self, *args,**kwargs):
        self.slug = self.slug or slugify(self.title)
        super().save(*args,**kwargs)

    
class Commande(models.Model):
    fini= 'fini'
    traitement='en cours de traitement'
    livraison = 'livraison en cours'
    livrer='livré'
    STATUT = [
        (traitement, 'en cours de traitement'),
        (fini, 'traitement fini'),
         (livraison,'livraison en cours'),
        (livrer,'livré'),
        ]
    items = models.CharField(max_length=300,null=True)
    total = models.CharField(max_length=200, null=True)
    nom=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    pays = models.CharField(max_length=300)
    # zipcode = models.CharField(max_length=300)
    date_commande = models.DateTimeField(auto_now=True)
    # statut=models.CharField(choices=STATUT, max_length=100, null=True)

    class Meta:
        ordering = ['-date_commande']

    def __str__(self):
        return self.email

class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE,)
    quantity=models.IntegerField(default=1)
    ordered=models.BooleanField(default=False)
    ordered_date=models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.title} ({self.quantity})"
    

class Cart(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    orders=models.ManyToManyField(Order)
    es_valider=models.BooleanField(default=False)
    
    
    def delete(self, *args,** kwargs):
        for order in self.orders.all():
            order.ordered=True
            order.ordered_date=timezone.now()
            order.save()
        self.orders.clear()
        super().delete(*args,** kwargs)

    
        


    
    def __str__(self):
        return  self.user.username
    