from django.contrib import admin
from .models import *
# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display=('username','first_name', 'last_name','adresse', 'ville', 'pays' )
class AdminCategorie(admin.ModelAdmin):
    list_display = ('name', 'date_added')

class AdminProduct(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'date_added')
    search_fields = ('title',) 
    list_editable = ('price',)

class AdminCommande(admin.ModelAdmin):
    list_display = ('items','nom','email','address', 'ville', 'pays','total', 'date_commande', )

class AdminSlider(admin.ModelAdmin):
    pass

admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategorie)
admin.site.register(Commande, AdminCommande)
admin.site.register(slider, AdminSlider)
admin.site.register(User, AdminUser)
admin.site.register(Order)
admin.site.register(Cart)




