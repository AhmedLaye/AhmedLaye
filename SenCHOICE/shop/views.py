
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Product, Commande, Category, Slider,Commande, Cart, Order, deal
from django.contrib import messages
from shop.models import User
from django.contrib.auth import authenticate, login, logout
from . import forms
from django.contrib.auth import login, authenticate  # import des fonctions login et authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import get_object_or_404
import pandas
from django.http import HttpResponseRedirect
import plotly.express as px
from django.core.cache import cache
from django.db import models
from django.contrib.auth.hashers import make_password






# Maintenant, visitors_count contient le nombre de visiteurs


def index(request):
     balance=0
     valeurPanier=0
     visitors_count = cache.get('visitors_count', 0)
     visitors_count += 1
     cache.set('visitors_count', visitors_count)

     if request.user.is_superuser:
       
        products = Product.objects.all()
        categories = Category.objects.all()
        commandes = Commande.objects.all()
        totalCommande = commandes.count() 
        category_names = [category.name for category in categories]
        product_counts = [Product.objects.filter(category=category).count() for category in categories]
        product_names = [product.title for product in products]
        total_quantities_sold = [Order.objects.filter(product=product, ordered=True).aggregate(total_quantity_sold=models.Sum('quantity'))['total_quantity_sold'] or 0 for product in products]

        # Créer le graphique
        fig = px.bar(x=category_names, y=product_counts, labels={'x': 'Catégorie', 'y': 'Nombre de produits'},
                   title='Nombre de produits par catégorie', color_discrete_sequence=['pink'])

        # Convertir le graphique en HTML
        graph_html = fig.to_html(full_html=False)
        

        # Combine product names and quantities into a list of tuples
        data = list(zip(product_names, total_quantities_sold))

        # Sort the list of tuples by quantities sold in descending order
        sorted_data = sorted(data, key=lambda x: x[1], reverse=True)

        # Take the top 5 best-selling products
        top_5_data = sorted_data[:5]

        # Unpack the data for the chart
        top_5_product_names, top_5_total_quantities_sold = zip(*top_5_data)
        fig1 = px.bar(x=top_5_product_names, y=top_5_total_quantities_sold, labels={'x': 'Produit', 'y': 'Quantité vendue'},
                  title='Top 5 Produits les plus vendus', color_discrete_sequence=['indigo'], )

        fig1.update_xaxes(tickangle = 70,)
        # Convert the chart to HTML
        graph_html1 = fig1.to_html(full_html=False)
        
        for com in commandes:
            balance+=float(com.total)  
        
        orders=Order.objects.all()
        total=0
        for article in orders:
            valeurPanier+=article.quantity
            total+=article.product.price

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
            'total':total,
            'products':products,
            'balance':balance,
            'visitors_count':visitors_count,
            'graph_html': graph_html,
            'graph_html1':graph_html1
    
        })
        
     else:
        promo=deal.objects.all()
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
            'promo':promo
            
            })
        # 'listProd':listProd, 'prod':produit,'categ':categ,


def detail(request, myid):
    product_object = Product.objects.get(id=myid)
    
    return render(request, 'shop/detail.html', {'product': product_object}) 



def login_page(request):
    message = ''
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            message = f'Bonjour, {user.username}! Vous êtes connecté.'

            # Redirect to the originally requested URL or home if not available
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            message = 'Identifiants invalides.'

    return render(request, 'shop/connexion/login.html', {'message': message})


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        telephone = request.POST.get('telephone')
        password = request.POST.get('password')
        
        try:
            print(f'Username: {username}, Password: {password}')
            user = User.objects.create_user(username=username, telephone=telephone, password=make_password(password))
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! You have successfully registered.')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        except Exception as e:
            print(f'Registration failed. {e}')
            messages.error(request, f'Registration failed. {e}')

    return render(request, 'shop/connexion/signup.html')





def logout_user(request):
    logout(request)
    return redirect('home')

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

    # Check if the product is already in the cart
    order, created = Order.objects.get_or_create(user=user, product=product, ordered=False)

    if not created:
        order.quantity += 1
        order.save()
        return HttpResponseRedirect(reverse('detail', args=[id]) + "?added=False")

    # If the order is created, add it to the cart
    cart.orders.add(order)
    cart.save()

    return HttpResponseRedirect(reverse('detail', args=[id]) + "?added=True")

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
        adress=request.POST.get('address')
       
        command = Commande(
            prod=items,
            total=total,
            nom=user,
            email=user.email,
            address=adress,
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
            #commande.delete()
            return redirect('/')  # Rediriger vers la vue de liste de commandes après la suppression

        # Mettre à jour l'état de la commande
        commande.statut = nouveau_statut
        commande.save()
        
        return redirect('home') 
    
    return redirect('/')

def order_details(request, order_id):
    order = get_object_or_404(Commande, id=order_id)
    if request.method=='POST':
        order.STATUT=request.POST.get('statut')
        order.save()
        return redirect('home')

    return render(request, 'shop/order_details.html', {'order': order, })

