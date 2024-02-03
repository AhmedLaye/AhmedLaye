from django.urls import path
from .views import *

urlpatterns=[
    path('', index, name='home'),
    path('login/',login_page, name='login'),
    path('logout/',logout_user, name='logout'),
    path('signup/',signup, name='signup'),
    path('categorie/<int:CatId>',categorieV, name='categorie'),
    path('detail/<int:productId>/',detail, name='detail'),
    path('order/<int:order_id>/',order_details, name='order_details'),

    path('detail/<int:id>/add-to-cart/',add_to_cart, name='add-to-cart'),
    path('cart/',cart,name='cart'),
     path('cart/delete/',delete_cart,name='delete_cart'),

    path('checkout/',checkout, name="checkout"),
    path('confirmation/', confirmation, name="confirmation"),
    path('commande/', Allcommande, name="commande"),
    path('commander/', CommandeCaisse, name="new_commande"),
    path('commander/<int:id>/add-to-cart/',add_to_cart, name='add-to-cart'),
    path('update_commande_statut/<int:commande_id>/', update_commande_statut, name='update_commande_statut'),
]