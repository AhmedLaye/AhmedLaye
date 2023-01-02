
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Product, Commande, Category, slider,Commande, Cart, Order
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . import forms
from django.contrib.auth import login, authenticate  # import des fonctions login et authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import get_object_or_404
from django.db.models import Q
import pandas

@login_required
def index(request):

     if request.user.is_superuser:
       
        
        products = Product.objects.all()
        categories = Category.objects.all()
        commandes = Commande.objects.all()
        totalCommande = commandes.count()
       


        my_dict = {}  
        for cat in Category.objects.all():
            list_product = []
            for prod in Product.objects.filter(category__id=cat.id):
                if prod.category == cat:
                    list_product.append(prod)
                my_dict[cat] = list_product          
        
        
        
        

        return render(request, 'shop/admin.html',
        {'list_product': pandas.DataFrame(list_product),
        
       
        'my_dict':my_dict,
        'commandes':commandes,
        "totalCommande":totalCommande,
        

        
        
        })
        
     else:
        my_dict = {}  
        for cat in Category.objects.all():
            list_product = []
            for prod in Product.objects.filter(category__id=cat.id):
                if prod.category == cat:
                    list_product.append(prod)
                my_dict[cat] = list_product  
        
        product = Product.objects.all()
       
    
        categorie= Category.objects.all()
        CatId=1
        image_slide=slider.objects.all()
        cart=Cart.objects.get_or_create(user=request.user)
        
        try:
            cart=get_object_or_404(Cart, user=request.user)
        except:
            cart=Cart.objects.get_or_create(user=request.user)
            cart=Cart.save()
        panier=[]
        orders=Order.objects.all()

        valeurPanier=0
        total=0
        for article in orders:
            valeurPanier+=article.quantity
            total+=article.product.price

        item_name = request.GET.get('item-name')
        if item_name !='' and item_name is not None:
            product = Product.objects.filter(title__icontains=item_name)
        
     

        return render(request, 'shop/index.html', {
            'product': product,
            'categorie': categorie,
            'image_slide':image_slide,
            'valeurPanier':valeurPanier,
            'total':total,
            'my_dict':my_dict,
            })
        # 'listProd':listProd, 'prod':produit,'categ':categ,




def detail(request, myid):
    product_object = Product.objects.get(id=myid)
    
    return render(request, 'shop/detail.html', {'product': product_object}) 



def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Bonjour, {user.username}! Vous êtes connecté.'
                return redirect('home')
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'shop/login.html', context={'form': form, 'message': message})



def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect('home')
    return render(request, 'shop/signup.html', context={'form': form})


def logout_user(request):
    
    logout(request)
    return redirect('login')

def confirmation(request):
    info = Commande.objects.all()[:1]
    for item in info:
        nom = item.nom
    return render(request, 'shop/confirmation.html', {'name': nom}) 

def detail(request, productId):
    products=Product.objects.get(id=productId)
    product=Product.objects.filter(category__name=products.category.name)
    
    return render(request, 'shop/detail.html',{'products':products,'product':product})

def categorieV(request, CatId):
    products=Category.objects.get(id=CatId)# on fixe la categorie, son nom et l'mage banner
    if products:
        visited=1
    procat=Product.objects.filter(category__id=CatId) #list des produits de cette categorie

    return render(request, './shop/categorie/categorie.html',
    {'procat':procat,
     'products':products,
    }
    )         
def Allcommande(request):
    commandes=Commande.objects.filter(nom__first_name=request.user.username)
    return render(request,'shop/commande.html',{'commandes':commandes} )


def add_to_cart(request,id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    cart, _ = Cart.objects.get_or_create(user=user)
    order,created = Order.objects.get_or_create(user=user,
    product=product)
    # ordered=False,
    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity+=1
        order.save()
    
    return redirect("detail",id)

@login_required
def cart(request):
    user = request.user
    cart=get_object_or_404(Cart, user=user)
    orders=cart.orders.all()
    valeurPanier=0
    total=0
    for article in orders:
        
        valeurPanier+=article.quantity
        total+=article.product.price
    return render(request, 'shop/cart.html', context={"orders":orders,'total':total})


def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()
    return redirect('home')




@login_required
def checkout(request):
    if request.method == 'POST':
        items=request.POST.get('items')
        total =request.POST.get('total')
        nom = request.user
        email = request.user.email
        address = request.user.adresse
        ville = request.user.ville
        pays = request.user.pays
        # zipcode= request.POST.get('zipcode')
        com = Commande(items=items,total=total, nom=nom, email=email, address=address, ville=ville, pays=pays,)
        # zipcode=zipcode
        com.save()
        return redirect('confirmation')
    return render(request,'shop/checkout.html') 
        
    