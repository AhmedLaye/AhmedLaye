
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Product, Commande, Category, Slider,Commande, Cart, Order
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
from django.http import HttpResponseRedirect



def index(request):
     balance=0
     if request.user.is_superuser:
        products = Product.objects.all()
        categories = Category.objects.all()
        commandes = Commande.objects.all()
        totalCommande = commandes.count()
        
        for com in commandes:
            balance+=float(com.total)  

        
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
         'valeurPanier':valeurPanier,
            'total':total,
            'products':products,
            'balance':balance
    
        })
        
     else:
        valeurPanier = 0
        total =0
        my_dict = {}  
        for cat in Category.objects.all():
            list_product = []
            for prod in Product.objects.filter(category__id=cat.id):
                if prod.category == cat:
                    list_product.append(prod)
                my_dict[cat] = list_product  
        
        product = Product.objects.all()
        categorie= Category.objects.all()
        slider=Slider.objects.all()
        CatId=1
        if request.user.is_authenticated :
            
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
            return render(request, 'shop/recherche.html', {'product':product, 'item_name':item_name})

        
    
        return render(request, 'shop/index.html', {
            'product': product,
            'categorie': categorie,
            
            'valeurPanier':valeurPanier,
            'total':total,
            'my_dict':my_dict,
            'slider':slider,
            
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


@login_required
def add_to_cart(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, product=product)

    if created:
        cart.orders.add(order)
        cart.save()
        return HttpResponseRedirect(reverse('detail', args=[id]) + "?added=True")

        
    else:
        order.quantity += 1
        order.save()
        return HttpResponseRedirect(reverse('detail', args=[id]) + "?added=False")


    if request.user.is_superuser:
        return redirect("new_commande")
    else:
        return redirect("detail", id)

@login_required
def cart(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    orders = cart.orders.all()
    total = sum(order.product.price * order.quantity for order in orders)

    return render(request, 'shop/cart.html', {'orders': orders, 'total': total})



def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()
    return redirect('home')


@login_required
def checkout(request):
    items = ""
    total = 0
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    orders = cart.orders.all()

    for order in orders:
        items += f"{order.product.title} x ({order.quantity}), "
        total += order.product.price * order.quantity
    
    context={'orders':orders,
             'total':total,
             }
    if request.method == 'POST':
        command = Commande(
            prod=items,
            total=total,
            nom=user,
            email=user.email,
            address=user.adresse,
            ville=user.ville,
            pays=user.pays,
            # statut=Commande.traitement  # Définir le statut initial comme "en cours de traitement"
        )
        command.save()

        cart.delete()

        return redirect('confirmation')

    return render(request, 'shop/checkout.html',context)

        

def CommandeCaisse(request):
    if request.user.is_superuser:
       
        
        products = Product.objects.all()
        categories = Category.objects.all()
        commandes = Commande.objects.all()
        totalCommande = commandes.count()
        user = request.user
        cart=get_object_or_404(Cart, user=user)
        orders=cart.orders.all()
        valeurPanier=0
        total=0
        for article in orders:
            
            valeurPanier+=article.quantity
            total+=article.product.price
        
    return render(request,'shop/admin/admin.html',{'products':products,
    "orders":orders,'total':total})



def update_commande_statut(request, commande_id):
    commande = get_object_or_404(Commande, pk=commande_id)
    
    if request.method == 'POST':
        # Récupérer le nouvel état de la commande depuis les données du formulaire
        nouveau_statut = request.POST.get('statut')

        # Vérifier si le nouveau statut est "livré"
        if nouveau_statut == 'livré':
            # Supprimer la commande
            commande.delete()
            return redirect('/')  # Rediriger vers la vue de liste de commandes après la suppression

        # Mettre à jour l'état de la commande
        commande.statut = nouveau_statut
        commande.save()
        
        return redirect('/') 
    
    return redirect('/')