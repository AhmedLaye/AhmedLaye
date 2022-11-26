from django.urls import path
from .views import *

urlpatterns=[
    path('', index, name='home'),
    path('login/',login_page, name='login'),
    path('signup/',signup_page, name='signup'),
    path('logout/',logout_user, name='logout'),
    path('signup/',signup_page, name='signup'),
    path('categorie/<int:CatId>',categorieV, name='categorie'),
    path('detail/<int:productId>/',detail, name='detail'),
    path('detail/<int:id>/add-to-cart/',add_to_cart, name='add-to-cart'),
    path('cart/',cart,name='cart'),
     path('cart/delete/',delete_cart,name='delete_cart'),

    path('checkout/',checkout, name="checkout"),
    path('confirmation/', confirmation, name="confirmation"),
    path('commande/', Allcommande, name="commande"),


]