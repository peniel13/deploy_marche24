from django.contrib import admin
from .models import Store,CategoryStore, Typestore
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'profile_pic', 'is_active',
                    'is_staff', 'is_superuser', 'last_login','last_ip', 'device_fingerprint',)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "profile_pic"),
            },
        ),
    )
    # Définir les champs modifiables dans le formulaire d'édition d'un utilisateur
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('last_ip', 'device_fingerprint')}),
    )
admin.site.register(CustomUser, CustomUserAdmin)

class StoreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Store, StoreAdmin)

class TypestoreAdmin(admin.ModelAdmin):
    list_display = ('nom',)

class CategoryStoreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'typestore')

admin.site.register(Typestore, TypestoreAdmin)
admin.site.register(CategoryStore, CategoryStoreAdmin)

from .models import Category

# Define the Category admin class
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'store')  # Columns to display in the list view
    search_fields = ('name',)  # Enable search by name
    list_filter = ('store',)  # Allow filtering categories by store
    ordering = ('store', 'name')  # Order categories by store and name

    # You can add more customization if necessary
    # e.g., make store a read-only field for categories already created
    readonly_fields = ('store',)

# Register the Category model with the CategoryAdmin class
admin.site.register(Category, CategoryAdmin)

from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category,Photo
class PhotoInline(admin.TabularInline):  # Tu peux aussi utiliser StackInline si tu préfères
    model = Photo
    extra = 1  # Affiche un champ vide de formulaire supplémentaire pour ajouter une photo
    fields = ('image',) 

class ProductAdmin(admin.ModelAdmin):
    # Définition des champs à afficher dans la liste des produits
    list_display = ('name', 'category', 'price', 'price_with_commission', 'stock', 'image_tag', 'created_at')

    # Filtres dans l'interface d'administration
    list_filter = ('category', 'price', 'stock', 'created_at')

    # Recherche par nom de produit, catégorie, prix, etc.
    search_fields = ['name', 'category__name', 'price', 'store',]

    # Ajout d'un inline pour afficher les photos associées
    inlines = [PhotoInline]

    # Méthode pour afficher l'image du produit dans l'admin
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "Pas d'image"
    
    image_tag.short_description = 'Image'

    # Optionnel : Méthode pour afficher la catégorie de manière lisible
    def get_category(self, obj):
        return obj.category.name if obj.category else "Non définie"
    get_category.short_description = 'Catégorie'

    # Ajouter price_with_commission en lecture seule
    def get_readonly_fields(self, request, obj=None):
        # On peut définir ici les champs qui doivent être en lecture seule
        return super().get_readonly_fields(request, obj) + ('price_with_commission',)

# Enregistrer le modèle et son administration
admin.site.register(Product, ProductAdmin)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'uploaded_at')
    search_fields = ('product',)
    list_filter = ('product',)

# Enregistrer les modèles dans l'admin
admin.site.register(Photo, PhotoAdmin)

from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem, Product

# Admin pour Cart
from django.contrib import admin
from .models import Cart

class CartAdmin(admin.ModelAdmin):
    # Colonnes affichées dans l'admin
    list_display = ('user', 'created_at', 'total_with_commission', 'item_count', 'is_ordered','is_active')

    # Filtres disponibles dans l'admin
    list_filter = ('created_at', 'user', 'is_ordered','is_active')  # Ajoutez 'is_ordered' pour filtrer

    # Recherche dans l'admin par nom d'utilisateur
    search_fields = ('user__username',)

    # Méthode pour afficher le total du panier avec la commission
    def total_with_commission(self, obj):
        return obj.get_total()  # Appelle la méthode get_total pour afficher le prix total + la commission

    total_with_commission.short_description = 'Total avec commission'  # Nom de la colonne

    # Méthode pour afficher le nombre d'articles dans le panier
    def item_count(self, obj):
        return obj.get_item_count()  # Appelle la méthode get_item_count pour afficher le nombre d'articles

    item_count.short_description = 'Nombre d\'articles'

# Enregistrer le modèle CartAdmin
admin.site.register(Cart, CartAdmin)



# Admin pour CartItem
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'total_price')  # Colonnes affichées
    list_filter = ('cart', 'product')  # Filtres dans l'admin
    search_fields = ('product__name', 'cart__user__username')  # Recherche par produit et utilisateur

    # Méthode pour afficher le prix total d'un article dans le panier
    def total_price(self, obj):
        return obj.get_total_price()  # Appelle la méthode get_total_price du modèle CartItem pour afficher le prix total

    total_price.short_description = 'Prix total'

# Enregistrer le modèle CartItemAdmin
admin.site.register(CartItem, CartItemAdmin)


from .models import Testimonial,Testimonialproduct

class TestimonialAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans la liste d'administration
    list_display = ('store', 'user', 'rating', 'created_at', 'content_snippet')

    # Ajout d'un filtre pour la date de création
    list_filter = ('created_at', 'rating')

    # Ajout d'une barre de recherche (par exemple par le nom de l'utilisateur ou le contenu)
    search_fields = ('user__username', 'content')

    # Ajout d'une fonctionnalité pour trier les témoignages
    ordering = ('-created_at',)

    # Raccourcir l'affichage du contenu (pour ne pas afficher tout le texte dans la liste)
    def content_snippet(self, obj):
        # Limite le texte à 100 caractères
        return obj.content[:100] + '...'
    content_snippet.short_description = 'Extrait du témoignage'

    # Personnaliser le formulaire dans l'admin
    fieldsets = (
        (None, {
            'fields': ('store', 'user', 'content', 'rating')
        }),
        ('Informations supplémentaires', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    # Rendre le champ 'created_at' en lecture seule
    readonly_fields = ('created_at',)

# Enregistrement de l'admin
admin.site.register(Testimonial, TestimonialAdmin)


class TestimonialproductAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans la liste d'administration
    list_display = ('product', 'user', 'rating', 'created_at', 'content_snippet')

    # Ajout d'un filtre pour la date de création
    list_filter = ('created_at', 'rating')

    # Ajout d'une barre de recherche (par exemple par le nom de l'utilisateur ou le contenu)
    search_fields = ('user__username', 'content')

    # Ajout d'une fonctionnalité pour trier les témoignages
    ordering = ('-created_at',)

    # Raccourcir l'affichage du contenu (pour ne pas afficher tout le texte dans la liste)
    def content_snippet(self, obj):
        # Limite le texte à 100 caractères
        return obj.content[:100] + '...'
    content_snippet.short_description = 'Extrait du témoignage'

    # Personnaliser le formulaire dans l'admin
    fieldsets = (
        (None, {
            'fields': ('product', 'user', 'content', 'rating')
        }),
        ('Informations supplémentaires', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    # Rendre le champ 'created_at' en lecture seule
    readonly_fields = ('created_at',)

# Enregistrement de l'admin
admin.site.register(Testimonialproduct, TestimonialproductAdmin)

from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import format_html
from django.contrib import admin
from .models import Order, OrderItem
from django.utils.translation import gettext_lazy as _

# Classe d'administration pour OrderItem (Article de commande)
from django.contrib import admin

# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0  # Nombre d'éléments vides à ajouter par défaut
#     readonly_fields = ('product', 'quantity', 'price_at_time_of_order', 'get_total_price', 'store')  # Ajout de 'store'
    
#     def get_total_price(self, obj):
#         return obj.get_total_price()
#     get_total_price.short_description = 'Total'

#     # Afficher le magasin de l'article de la commande dans l'inline
#     def store(self, obj):
#         return obj.product.store.name  # Accès au magasin via le produit
#     store.short_description = 'Magasin'

# admin.py
from django.contrib import admin
from .models import Order, OrderItem

# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0
#     fields = ['product', 'quantity', 'price_at_time_of_order', 'get_store']

#     def get_store(self, obj):
#         return obj.product.store  
from django.contrib import admin
from .models import Order, OrderItem
from django.utils.translation import gettext_lazy as _

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['product', 'quantity', 'price_at_time_of_order']  # Champs visibles dans l'inline
    readonly_fields = ['get_store']  # Afficher 'get_store' comme champ en lecture seule

    # Méthode pour récupérer le store du produit
    def get_store(self, obj):
        return obj.product.store.name if obj.product and obj.product.store else None  # Accéder au store via le produit
    get_store.short_description = _('Store')

class OrderAdmin(admin.ModelAdmin):
    # Affichage des champs dans l'admin
    list_display = ('id', 'user', 'get_stores', 'status', 'activated', 'total_amount', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'activated')  # Ajout de 'activated' dans les filtres
    search_fields = ('user__username', 'status')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    # Affichage des articles de la commande sous forme de sous-table (inline)
    inlines = [OrderItemInline]

    # Actions personnalisées pour l'admin
    actions = ['mark_as_shipped', 'calculate_total', 'activate_order']

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
        self.message_user(request, _("Les commandes ont été marquées comme expédiées."))
    mark_as_shipped.short_description = _("Marquer comme expédiée")

    def calculate_total(self, request, queryset):
        for order in queryset:
            order.calculate_total()
        self.message_user(request, _("Les montants totaux ont été recalculés."))
    calculate_total.short_description = _("Calculer le montant total")

    def activate_order(self, request, queryset):
        # Activer la commande pour Mobile Money (passage de activated=False à activated=True)
        queryset.update(activated=True)
        self.message_user(request, _("Les commandes ont été activées."))
    activate_order.short_description = _("Activer les commandes Mobile Money")

    # Méthode pour afficher les magasins associés à une commande (uniquement un magasin par commande)
    def get_stores(self, obj):
        # On récupère tous les stores associés à cette commande via les articles de la commande
        stores = set(item.product.store.name for item in obj.items.all() if item.product.store)  # Utilisation d'un set pour éviter les doublons
        return ", ".join(stores)
    get_stores.short_description = _("Magasins associés")

    def save_model(self, request, obj, form, change):
        # Appel de la méthode parent pour sauvegarder l'objet
        super().save_model(request, obj, form, change)
    
    def update_user_points(self, request, queryset):
        """Action pour mettre à jour les points de l'utilisateur après 5 achats"""
        for order in queryset:
            order.update_user_points()  # Appel de la méthode pour chaque commande sélectionnée
        self.message_user(request, _("Les points des utilisateurs ont été mis à jour après l'achat."))
    update_user_points.short_description = _("Mettre à jour les points des utilisateurs")
    
    # def update_user_points(self, request, queryset):
    #     """Action pour mettre à jour les points de l'utilisateur après 5 achats"""
    #     for order in queryset:
    #         order.update_user_points()  # Appel de la méthode pour chaque commande sélectionnée
    #     self.message_user(request, _("Les points des utilisateurs ont été mis à jour après l'achat."))
    # update_user_points.short_description = _("Mettre à jour les points des utilisateurs")


# Enregistrement des modèles dans l'admin
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)

from django.contrib import admin
from .models import UserLocation

class UserLocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'latitude', 'longitude', 'created_at')  # Afficher ces champs dans la liste
    search_fields = ('user__username',)  # Permet de rechercher par le nom d'utilisateur
    list_filter = ('created_at',)  # Permet de filtrer par date de création

admin.site.register(UserLocation, UserLocationAdmin)

# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0
#     fields = ['product', 'quantity', 'price_at_time_of_order', 'get_store']

#     # Méthode pour récupérer le store du produit
#     def get_store(self, obj):
#         return obj.product.store if obj.product else None  # Accéder au store via le produit

#     get_store.short_description = 'Store'
# class OrderAdmin(admin.ModelAdmin):
#     inlines = [OrderItemInline]

# # Classe d'administration pour Order (Commande)
# class OrderAdmin(admin.ModelAdmin):
#     # Affichage des champs dans l'admin
#     list_display = ('id', 'user', 'get_stores', 'status', 'activated', 'total_amount', 'created_at', 'updated_at')
#     list_filter = ('status', 'created_at', 'activated')  # Ajout de 'activated' dans les filtres
#     search_fields = ('user__username', 'status')
#     date_hierarchy = 'created_at'
#     ordering = ('-created_at',)

#     # Affichage des articles de la commande sous forme de sous-table (inline)
#     inlines = [OrderItemInline]

#     # Actions personnalisées pour l'admin
#     actions = ['mark_as_shipped', 'calculate_total', 'activate_order']

#     def mark_as_shipped(self, request, queryset):
#         queryset.update(status='shipped')
#         self.message_user(request, _("Les commandes ont été marquées comme expédiées."))
#     mark_as_shipped.short_description = _("Marquer comme expédiée")

#     def calculate_total(self, request, queryset):
#         for order in queryset:
#             order.calculate_total()
#         self.message_user(request, _("Les montants totaux ont été recalculés."))
#     calculate_total.short_description = _("Calculer le montant total")

#     def activate_order(self, request, queryset):
#         # Activer la commande pour Mobile Money (passage de activated=False à activated=True)
#         queryset.update(activated=True)
#         self.message_user(request, _("Les commandes ont été activées."))
#     activate_order.short_description = _("Activer les commandes Mobile Money")

#     # Méthode pour afficher les magasins associés à une commande (uniquement un magasin par commande)
#     def get_stores(self, obj):
#         # On récupère tous les stores associés à cette commande via les articles de la commande
#         stores = set(item.store.name for item in obj.items.all())  # Utilisation d'un set pour éviter les doublons
#         return ", ".join(stores)
#     get_stores.short_description = _("Magasins associés")

#     def save_model(self, request, obj, form, change):
#         # Appel de la méthode parent pour sauvegarder l'objet
#         super().save_model(request, obj, form, change)

# # Enregistrement des modèles dans l'admin
# admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem)

# # Classe d'administration pour OrderItem
# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0  # Nombre d'éléments vides à ajouter par défaut
#     readonly_fields = ('product', 'quantity', 'price_at_time_of_order', 'get_total_price')

#     def get_total_price(self, obj):
#         return obj.get_total_price()
#     get_total_price.short_description = 'Total'

# from django.contrib import admin
# from .models import Order, OrderItem
# from django.utils.translation import gettext_lazy as _

# class OrderAdmin(admin.ModelAdmin):
#     # Affichage des champs dans l'admin
#     list_display = ('id', 'user', 'store', 'status', 'activated', 'total_amount', 'created_at', 'updated_at')
#     list_filter = ('status', 'store', 'created_at', 'activated')  # Ajout de 'activated' dans les filtres
#     search_fields = ('user__username', 'store__name', 'status')
#     date_hierarchy = 'created_at'
#     ordering = ('-created_at',)
    
#     # Affichage des articles de la commande sous forme de sous-table (inline)
#     inlines = [OrderItemInline]

#     # Actions personnalisées pour l'admin
#     actions = ['mark_as_shipped', 'calculate_total', 'activate_order']

#     def mark_as_shipped(self, request, queryset):
#         queryset.update(status='shipped')
#         self.message_user(request, _("Les commandes ont été marquées comme expédiées."))
#     mark_as_shipped.short_description = _("Marquer comme expédiée")

#     def calculate_total(self, request, queryset):
#         for order in queryset:
#             order.calculate_total()
#         self.message_user(request, _("Les montants totaux ont été recalculés."))
#     calculate_total.short_description = _("Calculer le montant total")

#     def activate_order(self, request, queryset):
#         # Activer la commande pour Mobile Money (passage de activated=False à activated=True)
#         queryset.update(activated=True)
#         self.message_user(request, _("Les commandes ont été activées."))
#     activate_order.short_description = _("Activer les commandes Mobile Money")

#     def save_model(self, request, obj, form, change):
#         # Appel de la méthode parent pour sauver l'objet
#         super().save_model(request, obj, form, change)

# # Enregistrement des modèles dans l'admin
# admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem)


from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import MobileMoneyPayment, Cart, Order, OrderItem
from .utils import get_or_create_cart  # Assurez-vous d'importer votre méthode pour récupérer/Créer le panier
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib import admin
from .models import MobileMoneyPayment
from .models import Cart, Order, OrderItem
# admin.py
class MobileMoneyPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_number', 'transaction_id', 'first_name', 'last_name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('transaction_number', 'user__username', 'transaction_id')
    actions = ['validate_payment']

    def validate_payment(self, request, queryset):
        # Marquer les paiements comme validés
        queryset.update(status='validated')

        # Créer la commande pour chaque paiement validé
        for payment in queryset:
            cart = get_or_create_cart(payment.user)
            order = Order.objects.create(
                user=payment.user,
                store=cart.items.first().product.store,
                status='paid',
            )

            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price_at_time_of_order=cart_item.product.price
                )

            order.calculate_total()  # Mettre à jour le total de la commande
            cart.items.all().delete()  # Vider le panier

        self.message_user(request, "Les paiements ont été validés et les commandes ont été créées.")

    validate_payment.short_description = "Valider les paiements et créer les commandes"

# Enregistrer l'admin pour MobileMoneyPayment
admin.site.register(MobileMoneyPayment, MobileMoneyPaymentAdmin)

from django.contrib import admin
from .models import CommandeLivraison

class CommandeLivraisonAdmin(admin.ModelAdmin):
    # Afficher les champs dans la liste de l'admin
    list_display = ('nom', 'prenom', 'email', 'numero_tel', 'numero_id_colis', 'statut', 'date_commande', 'user')
    
    # Ajouter des filtres par statut, utilisateur et date
    list_filter = ('statut', 'user', 'date_commande')
    
    # Recherche par nom, email, numéro ID colis
    search_fields = ('nom', 'prenom', 'email', 'numero_id_colis')
    
    # Permettre de modifier les champs directement depuis la liste des objets
    list_editable = ('statut',)
    
    # Afficher les détails dans la vue d'édition
    fieldsets = (
        (None, {
            'fields': ('nom', 'prenom', 'email', 'numero_tel', 'user')
        }),
        ('Détails de la livraison', {
            'fields': ('adresse_livraison', 'description_colis', 'endroit_recuperation', 'numero_id_colis')
        }),
        ('Statut et dates', {
            'fields': ('statut', 'date_commande')
        }),
    )
    
    # Empêcher la modification de la date de commande
    readonly_fields = ('date_commande',)
    
    # Tris par défaut sur la date de commande (tri par date décroissante)
    ordering = ('-date_commande',)
    
    # Ajouter un bouton pour changer de statut rapidement
    actions = ['marquer_comme_livree']

    def marquer_comme_livree(self, request, queryset):
        """Action pour marquer la commande comme livrée."""
        queryset.update(statut='livree')
    marquer_comme_livree.short_description = "Marquer comme livrée"

# Enregistrer le modèle et son admin
admin.site.register( CommandeLivraison, CommandeLivraisonAdmin)




from .models import ContactProduct

class ContactProductAdmin(admin.ModelAdmin):
    # Définir les champs à afficher dans la liste
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'product', 'created_at')
    
    # Ajouter des filtres pour faciliter la recherche
    list_filter = ('created_at', 'product',)
    
    # Ajouter un champ de recherche pour rechercher des contacts par nom ou email
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'product__name')

    # Configurer les champs qui peuvent être édités directement dans la liste (in-line editing)
    list_editable = ('phone_number', 'email')

    # Configuration des actions
    actions = ['mark_as_processed']

    def mark_as_processed(self, request, queryset):
        # Exemple d'action personnalisée pour marquer les demandes comme traitées
        queryset.update(description="Demande traitée")
        self.message_user(request, "Les demandes sélectionnées ont été marquées comme traitées.")

    mark_as_processed.short_description = "Marquer comme traitée"

# Enregistrer le modèle avec l'admin
admin.site.register(ContactProduct, ContactProductAdmin)


from .models import ContactStore

class ContactStoreAdmin(admin.ModelAdmin):
    # Définir les champs à afficher dans la liste
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'store', 'created_at')
    
    # Ajouter des filtres pour faciliter la recherche
    list_filter = ('created_at', 'store',)
    
    # Ajouter un champ de recherche pour rechercher des contacts par nom ou email
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'store__name')

    # Configurer les champs qui peuvent être édités directement dans la liste (in-line editing)
    list_editable = ('phone_number', 'email')

    # Configuration des actions
    actions = ['mark_as_processed']

    def mark_as_processed(self, request, queryset):
        # Exemple d'action personnalisée pour marquer les demandes comme traitées
        queryset.update(description="Demande traitée")
        self.message_user(request, "Les demandes sélectionnées ont été marquées comme traitées.")

    mark_as_processed.short_description = "Marquer comme traitée"

# Enregistrer le modèle avec l'admin
admin.site.register(ContactStore, ContactStoreAdmin)


# from django.contrib import admin
# from .models import MobileMoneyTransaction

# @admin.register(MobileMoneyTransaction)
# class MobileMoneyTransactionAdmin(admin.ModelAdmin):
#     list_display = ('order', 'transaction_id', 'mobile_money_number', 'amount', 'is_verified', 'verified_at')
#     list_filter = ('is_verified', 'verified_at')
#     search_fields = ('transaction_id', 'mobile_money_number', 'order__id')
#     readonly_fields = ('transaction_id', 'mobile_money_number', 'amount', 'verified_at')

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         # Filtrer les transactions en attente de vérification
#         return queryset.filter(is_verified=False)



# Inline pour afficher les articles de commande sous la commande

from django.contrib import admin
from .models import UserPoints

from django.contrib import admin
from .models import UserPoints

from django.contrib import admin
from .models import UserPoints
from django.contrib import admin
from .models import UserPoints
class UserPointsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_points', 'ad_points', 'total_purchases', 'spent_points', 'get_user_email')
    search_fields = ('user__username', 'user__email')
    list_filter = ('points', 'ad_points', 'total_purchases', 'spent_points')  # Ajout du filtre sur spent_points
    ordering = ('user',)

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = "Email de l'utilisateur"

    def total_points(self, obj):
        return obj.points
    total_points.short_description = "Total des points"

    def has_add_permission(self, request):
        return False  # Empêche l'ajout manuel

    def has_delete_permission(self, request, obj=None):
        return False  # Empêche la suppression des UserPoints

    def reset_all_points(self, request, queryset):
        queryset.update(points=0, ad_points=0, spent_points=0)  # Réinitialisation complète
        self.message_user(request, "Les points ont été réinitialisés pour les utilisateurs sélectionnés.")
    reset_all_points.short_description = "Réinitialiser tous les points"

    def reset_ad_points(self, request, queryset):
        queryset.update(ad_points=0)
        self.message_user(request, "Les points publicitaires ont été réinitialisés.")
    reset_ad_points.short_description = "Réinitialiser uniquement les points publicitaires"

    actions = ['reset_all_points', 'reset_ad_points']

admin.site.register(UserPoints, UserPointsAdmin)




from django.contrib import admin
from .models import ProductPoints,PhotoPoints

class PhotoPointsInline(admin.TabularInline):  # Permet d'afficher les images associées dans la page d'une publicité
    model = PhotoPoints
    extra = 1  # Nombre de champs vides supplémentaires pour l'ajout de nouvelles images
    fields = ('image',) 

class ProductPointsAdmin(admin.ModelAdmin):
    list_display = ('name', 'points_required', 'description', 'created_at')  # Afficher le nom du produit, les points nécessaires, la description et la date de création
    search_fields = ('name',)  # Recherche par nom de produit
    list_filter = ('points_required', 'created_at')  # Filtrer par nombre de points et par date de création
    ordering = ('name',)  # Trier par nom du produit
    list_per_page = 10  # Afficher 10 produits récompenses par page
    inlines = [PhotoPointsInline]
admin.site.register(ProductPoints, ProductPointsAdmin)

class PhotoPointsAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'uploaded_at')  # Afficher le produit et l'image
    search_fields = ('product__name',)  # Recherche par nom de produit
    list_filter = ('uploaded_at',)  # Filtrer par date de téléchargement
    ordering = ('-uploaded_at',) 

# Enregistrer le modèle des images associées aux publicités
admin.site.register(PhotoPoints, PhotoPointsAdmin)

from django.contrib import admin
from .models import ContactProductPoints

class ContactProductPointsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'product_reward', 'created_at')  # Afficher les champs pertinents
    search_fields = ('first_name', 'last_name', 'email', 'product_reward__product__name')  # Recherche par prénom, nom, email ou nom du produit
    list_filter = ('product_reward',)  # Filtrer par produit récompense
    ordering = ('-created_at',)  # Trier par date de création (ordre décroissant)
    list_per_page = 10  # Afficher 10 demandes par page

admin.site.register(ContactProductPoints, ContactProductPointsAdmin)

from django.contrib import admin
from .models import  Purchase

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'points_used', 'purchase_date')
    list_filter = ('purchase_date', 'user')  # Vous pouvez filtrer par date et utilisateur
    search_fields = ('user__username', 'product__name')  # Recherche par utilisateur et produit
    ordering = ('-purchase_date',)  # Trier par date d'achat décroissante

admin.site.register(Purchase, PurchaseAdmin)

from django.contrib import admin
from .models import AssignerCategory

@admin.register(AssignerCategory)
class AssignerCategoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'category')  # Afficher ces colonnes dans la liste admin
    search_fields = ('product__name', 'category__name')  # Ajouter une recherche
    list_filter = ('category',)  # Ajouter un filtre par catégorie


from django.contrib import admin
from .models import Advertisement

# admin.py
from django.contrib import admin
from .models import Comment, Advertisement

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0  # Pas de ligne vide supplémentaire
    readonly_fields = ['user', 'content', 'created_at']
    # Affiche l'utilisateur, le contenu du commentaire, et la date de création du commentaire
    fields = ['user', 'content', 'created_at']

from django.contrib import admin
from .models import Advertisement, PhotoAds

class PhotoAdsInline(admin.TabularInline):  # Permet d'afficher les images associées dans la page d'une publicité
    model = PhotoAds
    extra = 1  # Nombre de champs vides supplémentaires pour l'ajout de nouvelles images
    fields = ('image',) 

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'likes_count', 'comments_count', 'shares_count')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

    inlines = [PhotoAdsInline]  # Ajoute les images associées à la publicité dans l'admin

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.shares_count = obj.shares_count  # Met à jour le compteur de partages si nécessaire
        obj.save()

# Enregistrer le modèle Advertisement avec son admin personnalisé
admin.site.register(Advertisement, AdvertisementAdmin)

class PhotoAdsAdmin(admin.ModelAdmin):
    list_display = ('ads', 'image', 'uploaded_at')
    search_fields = ('ads__title',)
    list_filter = ('ads',)

# Enregistrer le modèle des images associées aux publicités
admin.site.register(PhotoAds, PhotoAdsAdmin)


# Enregistrer le modèle Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad', 'content', 'created_at')
    search_fields = ('user__username', 'ad__title', 'content')
    list_filter = ('created_at',)
    readonly_fields = ['user', 'ad', 'content', 'created_at']



from django.contrib import admin
from .models import AdInteraction

class AdInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad', 'interaction_type', 'timestamp')
    search_fields = ('user__username', 'ad__title')
    list_filter = ('interaction_type', 'timestamp')
    ordering = ('-timestamp',)

admin.site.register(AdInteraction, AdInteractionAdmin)

from django.contrib import admin
from .models import Share,PopUpAdvertisement

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad', 'shared_at')  # Colonnes visibles dans la liste
    list_filter = ('shared_at', 'user')  # Filtres sur la barre latérale
    search_fields = ('user__username', 'ad__title')  # Champ de recherche
    ordering = ('-shared_at',)  # Trie par date de partage décroissante

from django.contrib import admin
from .models import PointConversion

@admin.register(PointConversion)
class PointConversionAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversion_rate', 'display_conversion')  # Afficher les informations pertinentes
    search_fields = ('conversion_rate',)  # Permet de chercher par taux de conversion
    list_filter = ('conversion_rate',)  # Permet de filtrer par taux de conversion
    ordering = ('-conversion_rate',)  # Trier par taux de conversion de manière décroissante

    def display_conversion(self, obj):
        """Affiche un message avec le taux de conversion en USD."""
        return f"1 point = {obj.conversion_rate} USD"
    
    display_conversion.short_description = 'Taux de Conversion'

# admin.py
from django.contrib import admin
from django.utils.timezone import now
from .models import PopUpAdvertisement

from django.contrib import admin
from .models import PopUpAdvertisement

# Personnalisation de l'interface d'administration pour PopUpAdvertisement
class PopUpAdvertisementAdmin(admin.ModelAdmin):
    list_display = ('media_type', 'is_active', 'created_at')  # Colonnes affichées dans la liste
    list_filter = ('is_active', 'media_type')  # Filtres disponibles dans la colonne de filtre
    search_fields = ('media_type',)  # Permet de rechercher par type de média
    ordering = ('-created_at',)  # Trie les publicités par date de création (du plus récent au plus ancien)
    
    # Ajoutez d'autres personnalisations ici si nécessaire
    
# Enregistrer le modèle avec l'administration personnalisée
admin.site.register(PopUpAdvertisement, PopUpAdvertisementAdmin)

from django.contrib import admin
from .models import SpotPubStore

@admin.register(SpotPubStore)
class SpotPubStoreAdmin(admin.ModelAdmin):
    list_display = ('store', 'uploaded_at')
    search_fields = ('store__name',)
    readonly_fields = ('uploaded_at',)

    def has_add_permission(self, request):
        # Empêche l'ajout manuel depuis l'admin, car le lien est OneToOne avec Store
        return False