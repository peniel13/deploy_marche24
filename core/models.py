from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify # type: ignore
from decimal import Decimal

# Create your models here.


# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)
#     profile_pic = models.ImageField(upload_to="p_img", blank=True, null=True)
#     address = models.CharField(max_length=50, blank=True, null=True)
#     phone = models.CharField(max_length=11, blank=True, null=True)
#     role = models.CharField(max_length=50, blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)  # Ajout du champ de vérification
#     last_ip = models.GenericIPAddressField(blank=True, null=True)
#     device_fingerprint = models.CharField(max_length=255, blank=True, null=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
    
#     def __str__(self):
#         return self.email
from django.contrib.auth.models import AbstractUser
from django.db import models

SEX_CHOICES = [
    ('male', 'Homme'),
    ('female', 'Femme'),
]

COMMUNE_CHOICES = [
    ('lubumbashi', 'Lubumbashi'),
    ('annexe', 'Annexe'),
    ('kenya', 'Kenya'),
    ('katuba', 'Katuba'),
    ('rwashi', 'Rwashi'),
    ('kampemba', 'Kampemba'),
    ('kamalondo', 'Kamalondo'),
    # ... ajoute tes communes ici
]

CITY_CHOICES = [
    ('lubumbashi', 'Lubumbashi'),
    ('likasi', 'Likasi'),
    ('kolwezi', 'Kolwezi'),
    ('kasumbalesa', 'Kasumbalesa'),
    ('kalemie', 'Kalemie'),
    ('kamina', 'Kamina'),
    ('kinshasa', 'Kinshasa'),
    ('kisangani', 'Kisangani'),
    ('mbujimayi', 'Mbujimayi'),
    
    # ... ajoute d’autres villes
]

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="p_img", blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    last_ip = models.GenericIPAddressField(blank=True, null=True)
    device_fingerprint = models.CharField(max_length=255, blank=True, null=True)

    # Ajouts pour ciblage :
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True)
    commune = models.CharField(max_length=50, choices=COMMUNE_CHOICES, blank=True, null=True)
    city = models.CharField(max_length=50, choices=CITY_CHOICES, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)  # ex: "sport, mode, jeux vidéo"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def compress_image(self, image_field, quality=70):
        if image_field:
            img = Image.open(image_field)
            img = img.convert('RGB')
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=quality)
            new_image_file = ContentFile(buffer.getvalue())
            filename = os.path.basename(image_field.name)
            return new_image_file, filename
        return None, None

    def save(self, *args, **kwargs):
        if self.profile_pic and not hasattr(self.profile_pic, '_compressed'):
            compressed_file, name = self.compress_image(self.profile_pic)
            if compressed_file:
                self.profile_pic.save(name, compressed_file, save=False)
                self.profile_pic._compressed = True
        super(CustomUser, self).save(*args, **kwargs)

    def profile_pic_size_ko(self):
        if self.profile_pic and hasattr(self.profile_pic, 'size'):
            return f"{self.profile_pic.size / 1024:.1f} Ko"
        return "Aucune image"
    profile_pic_size_ko.short_description = 'Taille image'

class Typestore(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class CategoryStore(models.Model):
    nom = models.CharField(max_length=100)
    typestore = models.ForeignKey(Typestore, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom
# Choix pour les communes
COMMUNES_CHOICES = [
    ('ngaliema', 'Ngaliema'),
    ('limete', 'Limete'),
    ('mongafula', 'Mongafula'),
    ('kingabwa', 'Kingabwa'),
    ('bandalungwa', 'Bandalungwa'),
    ('kinshasa', 'Kinshasa'),
    ('gombe', 'Gombe'),
    ('kasa-vubu', 'Kasa-Vubu'),
    ('ngiri-ngiri', 'Ngiri-Ngiri'),
    ('kinkole', 'Kinkole'),
    ('matete', 'Matete'),
    ('kinshasa', 'Kinshasa'),
    ('kimbanguiste', 'Kimbanguiste'),
    ('kalamu', 'Kalamu'),
    ('ngaba', 'Ngaba'),
    ('lemba', 'Lemba'),
    ('madrassah', 'Madrassah'),
    ('masina', 'Masina'),
    ('lualaba', 'Lualaba'),
    ('kwa-kabuya', 'Kwa-Kabuya'),
    ('makala', 'Makala'),
    ('bumbu', 'Bumbu'),
    ('ngombé', 'Ngombé'),
    ('eala', 'Eala'),
]
class Store(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stores")
    name = models.CharField(max_length=255)
    slug=models.SlugField(blank=True, null=True)
    description = models.TextField()
    adresse = models.TextField()
    thumbnail = models.ImageField(upload_to="img", null=True, blank=True, verbose_name="Image du Store")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    typestore = models.ForeignKey(Typestore, on_delete=models.SET_NULL, null=True, blank=True)
    categorystore = models.ForeignKey(CategoryStore, on_delete=models.SET_NULL, null=True, blank=True)
    apply_commission = models.BooleanField(default=True)
    favoritestore = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    # Champs pour la géolocalisation
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        # Compression de l'image thumbnail
        if self.thumbnail and not hasattr(self.thumbnail, '_compressed'):
            img = Image.open(self.thumbnail)
            img = img.convert('RGB')
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=70)
            new_image_file = ContentFile(buffer.getvalue())
            filename = os.path.basename(self.thumbnail.name)
            self.thumbnail.save(filename, new_image_file, save=False)
            self.thumbnail._compressed = True

        super(Store, self).save(*args, **kwargs)

    def thumbnail_size_ko(self):
        if self.thumbnail and hasattr(self.thumbnail, 'size'):
            return f"{self.thumbnail.size / 1024:.1f} Ko"
        return "Aucune image"
    
    def __str__(self):
        return self.name



from django.db import models
class UserLocation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location of {self.user.username} at {self.latitude}, {self.longitude}"



class Testimonial(models.Model):
    RATING_CHOICES = [(i, f'{i}/10') for i in range(1, 11)]  # Créer des choix de 1 à 10

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="testimonials")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()  # Le texte du témoignage
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=5)  # Choix entre 1 et 10
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Testimonial for {self.store.name} by {self.user.username}'
    
    class Meta:
        ordering = ['-created_at']




class Category(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=255)
   
    def __str__(self):
        return self.name

from decimal import Decimal
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os
class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="products", null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_with_commission = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    image_galerie = models.ImageField(upload_to='product/galerie/', null=True, blank=True, verbose_name="Image galerie")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_total_price(self, quantity):
        return self.price * quantity

    # --- Méthodes pour afficher la taille en Ko ---
    def image_size_ko(self):
        if self.image and hasattr(self.image, 'size'):
            return f"{self.image.size / 1024:.1f} Ko"
        return "Aucune image"

    def image_galerie_size_ko(self):
        if self.image_galerie and hasattr(self.image_galerie, 'size'):
            return f"{self.image_galerie.size / 1024:.1f} Ko"
        return "Aucune image"

    image_size_ko.short_description = "Taille image"
    image_galerie_size_ko.short_description = "Taille image galerie"

    # --- Méthode save pour compression ---
    def compress_image(self, image_field, quality=70):
        from PIL import Image
        from io import BytesIO
        from django.core.files.base import ContentFile

        if image_field:
            img = Image.open(image_field)
            img = img.convert('RGB')
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=quality)
            new_image_file = ContentFile(buffer.getvalue())
            filename = os.path.basename(image_field.name)
            return new_image_file, filename
        return None, None

    def save(self, *args, **kwargs):
        if self.store.apply_commission and self.price is not None:
            commission_rate = Decimal('0.30')
            commission = self.price * commission_rate
            self.price_with_commission = self.price + commission
        else:
            self.price_with_commission = self.price

        if self.image and not hasattr(self.image, '_compressed'):
            compressed_file, name = self.compress_image(self.image)
            if compressed_file:
                self.image.save(name, compressed_file, save=False)
                self.image._compressed = True

        if self.image_galerie and not hasattr(self.image_galerie, '_compressed'):
            compressed_file, name = self.compress_image(self.image_galerie)
            if compressed_file:
                self.image_galerie.save(name, compressed_file, save=False)
                self.image_galerie._compressed = True

        super(Product, self).save(*args, **kwargs)

# class Product(models.Model):
#     store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="products")
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="products", null=True, blank=True)  # ✅ Permet d'être null
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     # Champ pour le prix de base
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     # Champ pour afficher le prix avec commission
#     price_with_commission = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     stock = models.PositiveIntegerField()
#     image = models.ImageField(upload_to='products/', null=True, blank=True)
#     image_galerie = models.ImageField(upload_to='product/galerie/', null=True, blank=True, verbose_name="Image galerie")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

#     def get_total_price(self, quantity):
#         return self.price * quantity

#     def save(self, *args, **kwargs):
#         # Si le magasin a la commission activée, on applique la commission
#         if self.store.apply_commission and self.price is not None:
#             commission_rate = Decimal('0.30')  # 30% de commission
#             commission = self.price * commission_rate  # Calcul de la commission
#             self.price_with_commission = self.price + commission  # Calcul du prix avec commission
#         else:
#             self.price_with_commission = self.price  # Aucun prix de commission si désactivé
        
#         # Sauvegarde de l'objet
#         super(Product, self).save(*args, **kwargs)

class AssignerCategory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="category_assignment")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="assigned_products")

    def __str__(self):
        return f"{self.product.name} -> {self.category.name}"

from django.db import models

class ContactProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="contact_requests")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.product.name}"

class ContactStore(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="contact_requests")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.product.name}"


class Testimonialproduct(models.Model):
    RATING_CHOICES = [(i, f'{i}/10') for i in range(1, 11)]  # Créer des choix de 1 à 10

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="testimonials")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()  # Le texte du témoignage
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=5)  # Choix entre 1 et 10
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Testimonial for {self.store.name} by {self.user.username}'
    
    class Meta:
        ordering = ['-created_at']

class Photo(models.Model):
    product = models.ForeignKey(Product, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/galerie/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.product} - {self.image.name}"




# models.py
from django.db import models
from django.conf import settings

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True) # Ajoutez ce champ

    def __str__(self):
        return f"Panier de {self.user.username}"

    def get_total(self):
        total_price = sum(item.get_total_price() for item in self.items.all())
        commission = 0
        return total_price + commission

    def get_item_count(self):
        return sum(item.quantity for item in self.items.all())



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Définir un valeur par défaut de 1

    def __str__(self):
        return f"{self.product.name} - {self.quantity} x {self.product.price_with_commission}"

    def get_total_price(self):
        return self.product.price_with_commission * self.quantity


# models.py

from django.db import models
from decimal import Decimal
from django.conf import settings

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=50, choices=[('pending', 'En attente'), ('paid', 'Payée'), ('shipped', 'Expédiée'), ('served', 'Servie')],
        default='pending'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    activated = models.BooleanField(default=True)  # Par défaut, l'ordre est activé

    def __str__(self):
        return f"Commande {self.id} - {self.user.username} - {self.status}"

    def calculate_total(self):
        """Calculer et mettre à jour le montant total de la commande"""
        self.total_amount = sum(item.get_total_price() for item in self.items.all())
        self.save()

    def get_total(self):
        """Retourner le montant total de la commande"""
        return self.total_amount
    
    def update_user_points(self):
        """Incrémente le compteur de points après 5 commandes activées"""
        if not hasattr(self.user, 'userpoints'):
            self.user.userpoints = UserPoints.objects.create(user=self.user)

        user_points = self.user.userpoints
        user_points.total_purchases += 1  # Incrémenter le nombre total d'achats
        if user_points.total_purchases % 5 == 0:  # Vérifier si on atteint un multiple de 5
            user_points.points += 1  # Ajouter 1 point de fidélité

        user_points.save()

    def save(self, *args, **kwargs):
        """Mise à jour des points de l'utilisateur lorsque la commande est activée"""
        if self.activated:  # Vérifier si l'admin a activé la commande
            self.update_user_points()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_time_of_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} x {self.price_at_time_of_order}"

    def get_total_price(self):
        """Retourner le prix total pour cet item"""
        return self.price_at_time_of_order * self.quantity

    def get_store(self):
        """Retourner le store auquel appartient ce produit"""
        return self.product.store  # Accéder au store via le produit lié



# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
#     store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name="orders")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     status = models.CharField(
#         max_length=50, choices=[('pending', 'En attente'), ('En attente', 'Payée'), ('shipped', 'Expédiée'),('servit', 'Servit')],
#         default='pending'
#     )
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
#     activated = models.BooleanField(default=True)  # Par défaut, l'ordre est activé
    
#     def __str__(self):
#         return f"Commande {self.id} - {self.store.name} - {self.status}"

#     def calculate_total(self):
#         """Calculer et mettre à jour le montant total de la commande"""
#         self.total_amount = sum(item.get_total_price() for item in self.items.all())
#         self.save()

#     def get_total(self):
#         """Retourner le montant total de la commande"""
#         return self.total_amount


# # Article de commande (Produit associé à une commande)
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price_at_time_of_order = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.product.name} - {self.quantity} x {self.price_at_time_of_order}"

#     def get_total_price(self):
#         # Vérifie si price_at_time_of_order et quantity ne sont pas None
#         if self.price_at_time_of_order is None or self.quantity is None:
#             return Decimal('0.00')  # Retourne 0 si des valeurs manquent
#         return self.price_at_time_of_order * self.quantity

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price_at_time_of_order = models.DecimalField(max_digits=10, decimal_places=2)
   
#     def __str__(self):
#         return f"{self.product.name} - {self.quantity} x {self.price_at_time_of_order}"

#     def get_total_price(self):
#         return self.price_at_time_of_order * self.quantity


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# models.py
class MobileMoneyPayment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('validated', 'Validé'),
        ('rejected', 'Rejeté'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction_number = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100, unique=True)  # Transaction ID unique
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    delivery_option = models.CharField(max_length=100, choices=[('home', 'A domicile'), ('pickup', 'Récupérer soi-même')])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Etat du paiement
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.transaction_id}"

    def get_total_amount(self):
        # Calculer le montant total du panier
        return sum(item.product.price * item.quantity for item in self.cart.items.all())

class CommandeLivraison(models.Model):
    # Informations du client
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    numero_tel = models.CharField(max_length=15)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Détails de la livraison
    adresse_livraison = models.TextField()
    description_colis = models.TextField()
    endroit_recuperation = models.CharField(max_length=255)
    numero_id_colis = models.CharField(max_length=100)

    # Statut de la commande
    statut = models.CharField(
        max_length=20,
        choices=[('en_attente', 'En attente'), ('en_cours', 'En cours'), ('livree', 'Livrée')],
        default='en_attente'
    )
    
    # Dates
    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande {self.numero_id_colis} par {self.nom} {self.prenom}"

    class Meta:
        permissions = [
            ("peut_marquer_comme_livree", "Peut marquer les commandes comme livrées"),
        ]

class Classe(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

from django.db import models

from django.db import models

class ProductPoints(models.Model):
    name = models.CharField(max_length=255)
    points_required = models.PositiveIntegerField()  # Nombre de points nécessaires pour l'acheter
    description = models.TextField()  # Description du produit
    image = models.ImageField(upload_to='product_rewards/', blank=True, null=True)  # Image pour le produit
    created_at = models.DateTimeField(auto_now_add=True)  # Champ de date de création

    def __str__(self):
        return f"{self.name} - {self.points_required} points"


class PhotoPoints(models.Model):
    product = models.ForeignKey(ProductPoints, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photopoints/galerie/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.product} - {self.image.name}"

from django.db import models

class ContactProductPoints(models.Model):
    product_reward = models.ForeignKey('ProductPoints', on_delete=models.CASCADE, related_name="contact_requests")  # Lien vers le produit récompense
    first_name = models.CharField(max_length=255)  # Prénom de la personne
    last_name = models.CharField(max_length=255)  # Nom de la personne
    email = models.EmailField()  # Email de la personne
    phone_number = models.CharField(max_length=20)  # Numéro de téléphone
    description = models.TextField(blank=True, null=True)  # Message ou description (optionnel)
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création de la demande

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.product_reward.product.name}"



from django.db import models
from django.conf import settings

# class UserPoints(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     points = models.PositiveIntegerField(default=0)  # Points totaux utilisables
#     total_purchases = models.PositiveIntegerField(default=0)  # Nombre total d'achats effectués
#     ad_points = models.PositiveIntegerField(default=0)  # Points gagnés via les publicités

#     def __str__(self):
#         return f"{self.user.username} - {self.points} points"

#     def add_purchase(self):
#         """Incrémente le compteur de commandes et ajoute des points de fidélité."""
#         self.total_purchases += 1
#         if self.total_purchases % 5 == 0:
#             self.points += 1
#         self.save()

#     def add_ad_points(self, points):
#         """Ajoute des points en fonction des interactions publicitaires."""
#         self.ad_points += points
#         self.points += points  # Ajouter aux points globaux
#         self.save()
# class UserPoints(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     points = models.PositiveIntegerField(default=0)  # Points actuels utilisables
#     total_purchases = models.PositiveIntegerField(default=0)  # Nombre total d'achats effectués
#     ad_points = models.PositiveIntegerField(default=0)  # Points gagnés via les publicités
#     spent_points = models.PositiveIntegerField(default=0)  # ✅ Suivi des points dépensés

#     def __str__(self):
#         return f"{self.user.username} - {self.points} points"

#     def add_purchase(self):
#         """Ajoute un achat et applique les récompenses si nécessaire."""
#         self.total_purchases += 1
#         if self.total_purchases % 5 == 0:
#             self.points += 1  # ✅ Ajoute un point uniquement tous les 5 achats
#         self.save()

#     def spend_points(self, amount):
#         """Déduit des points lors d'un achat."""
#         if self.points >= amount:
#             self.points -= amount
#             self.spent_points += amount  # ✅ Enregistre les points dépensés
#             self.save()
#             return True
#         return False
class UserPoints(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)  # Points actuels utilisables
    total_purchases = models.PositiveIntegerField(default=0)  # Nombre total d'achats effectués
    ad_points = models.PositiveIntegerField(default=0)  # Points gagnés via les publicités
    spent_points = models.PositiveIntegerField(default=0)  # ✅ Suivi des points dépensés

    def __str__(self):
        return f"{self.user.username} - {self.points} points"

    def get_earned_points(self):
        """Calcule le total des points gagnés (likes, commentaires, partages, achats)."""
        likes = AdInteraction.objects.filter(user=self.user, interaction_type='like').count()
        comments = AdInteraction.objects.filter(user=self.user, interaction_type='comment').count()
        shares = AdInteraction.objects.filter(user=self.user, interaction_type='share').count()

        earned_points = likes + (comments * 2) + (shares * 5)  # Points gagnés via interactions
        earned_points += self.total_purchases // 5  # Ajout des points de fidélité (1 point tous les 5 achats)
        
        return earned_points

    def spend_points(self, amount):
        """Déduit des points lors d'un achat et enregistre la dépense."""
        if self.points >= amount:
           self.points -= amount
           self.spent_points += amount  # ✅ Mise à jour correcte
           self.save()
        
        # 🔥 Debugging pour voir les valeurs après sauvegarde
        obj = UserPoints.objects.get(user=self.user)  # Recharge depuis la BD
        print(f"✅ Points actuels : {obj.points} | Spent points : {obj.spent_points}")

        return True
        print("❌ Pas assez de points !")  # 🔥 Debugging
        return False



    def add_ad_points(self, points):
        """Ajoute des points en fonction des interactions publicitaires."""
        self.ad_points += points
        self.points += points  # Ajouter aux points globaux
        self.save()




from decimal import Decimal, ROUND_HALF_UP

class PointConversion(models.Model):
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=5, default=Decimal('0.00143'))  # 1 point = 0.00143 USD

    def __str__(self):
        return f"1 point = {self.conversion_rate} USD"

    def convert_points_to_usd(self, points):
        """Convertit les points en dollars avec un arrondi à 2 décimales."""
        result = Decimal(points) * self.conversion_rate
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)




class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Utilisateur qui a acheté
    product = models.ForeignKey(ProductPoints, on_delete=models.CASCADE)  # Produit acheté
    points_used = models.PositiveIntegerField()  # Nombre de points utilisés pour l'achat
    purchase_date = models.DateTimeField(auto_now_add=True)  # Date de l'achat

    def __str__(self):
        return f"Achat de {self.product.name} par {self.user.username} le {self.purchase_date}"


from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Advertisement(models.Model):
    MEDIA_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES)
    media_file = models.FileField(upload_to='ads/')  # Image ou vidéo
    url = models.URLField(blank=True, null=True)  # Lien externe (ex: site de l’annonceur)
    thumbnail_url = models.ImageField(upload_to='thumbnails/', null=True, blank=True)  # Miniature de la vidéo
    slug = models.SlugField(unique=True, blank=True)  
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    visits_count = models.PositiveIntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    # Autres champs...
    # Nouveaux champs pour le ciblage
    target_all_users = models.BooleanField(default=True)  # si True, tout le monde peut voir
    target_sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True)
    target_communes = models.JSONField(blank=True, null=True)  # ex: ["cocody", "abobo"]
    target_cities = models.JSONField(blank=True, null=True)    # ex: ["abidjan"]
    target_keywords = models.TextField(blank=True, null=True)  # mots-clés séparés par virgule
    max_target_users = models.PositiveIntegerField(blank=True, null=True)  # nombre max de personnes à atteindre
    targeted_users = models.ManyToManyField('CustomUser', blank=True)  # ceux qui ont déjà vu
    # models.py

    target_address_keywords = models.TextField(blank=True, null=True, help_text="Mots-clés extraits de l'adresse.")
    target_latitude = models.DecimalField(max_digits=20, decimal_places=18, blank=True, null=True)
    target_longitude = models.DecimalField(max_digits=20, decimal_places=18, blank=True, null=True)
    target_radius_km = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Rayon en kilomètres autour de la position ciblée.")

    def get_absolute_url(self):
      return reverse('advertisement_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.title

class PhotoAds(models.Model):
    ads = models.ForeignKey(Advertisement, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ads/galerie/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.ads} - {self.image.name}"

class Share(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Utilisation de AUTH_USER_MODEL
    ad = models.ForeignKey('core.Advertisement', on_delete=models.CASCADE)  # Remplace 'Advertisement' si besoin
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} a partagé {self.ad.title}"



class AdInteraction(models.Model):
    INTERACTION_CHOICES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('share', 'Share'),
        ('visit', 'Visit'),
        ('bonus_1_point', 'Bonus 1 Point'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ad = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="interactions")
    interaction_type = models.CharField(max_length=16, choices=INTERACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ad', 'interaction_type')  # Empêche les doublons

    def __str__(self):
        return f"{self.user.username} {self.interaction_type} {self.ad.title}"

    def toggle_like(self):
        if self.interaction_type == 'like':
         self.delete()  # Si c'est un "like", on supprime l'interaction pour "dislike"
        if self.ad.likes_count > 0:
            self.ad.likes_count -= 1  # Empêche de réduire à une valeur négative
        else:
         self.interaction_type = 'like'
         self.save()
         self.ad.likes_count += 1
        self.ad.save()

    

    def add_comment(self, content):
        """ Ajouter un commentaire à la publicité et gérer les points """
        if not Comment.objects.filter(user=self.user, ad=self.ad).exists():
            Comment.objects.create(user=self.user, ad=self.ad, content=content)
            self.ad.comments_count += 1
            self.user.userpoints.points += 2  # Ajouter 2 points pour un commentaire
            self.ad.save()
            self.user.userpoints.save()

   
    def share_ad(self):
        """ Ajouter un partage et gérer les points """
        # Vérifier combien de fois l'utilisateur a partagé cette annonce
        share_count = AdInteraction.objects.filter(user=self.user, ad=self.ad, interaction_type='share').count()

        if share_count < 1:  # L'utilisateur n'a pas encore partagé cette annonce
            self.interaction_type = 'share'
            self.save()
            self.ad.shares_count += 1
            self.user.userpoints.points += 3  # Ajouter 5 points pour chaque partage
            self.ad.save()
            self.user.userpoints.save()
        else:
            # Si l'utilisateur a déjà partagé cette publicité, il ne peut pas gagner de points pour un deuxième partage
            print("L'utilisateur a déjà partagé cette publicité.")

   


    def get_comments(self):
        from .models import Comment  # Importation locale pour éviter la circularité
        return Comment.objects.filter(ad=self)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # L'utilisateur qui commente
    ad = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="comments")  # La publicité à laquelle appartient le commentaire
    content = models.TextField()  # Le contenu du commentaire
    created_at = models.DateTimeField(auto_now_add=True)  # La date de création du commentaire

    class Meta:
        unique_together = ('user', 'ad')  # Un utilisateur ne peut commenter qu'une fois une même publicité

    def __str__(self):
        return f"Commentaire de {self.user.username} sur {self.ad.title}"



from django.db import models

class PopUpAdvertisement(models.Model):
    IMAGE = 'image'
    VIDEO = 'video'
    MEDIA_TYPE_CHOICES = [
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
    ]
    
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='ads/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Ajout d'un champ booléen pour activer/désactiver

    def __str__(self):
        return f"Publicité {'Active' if self.is_active else 'Inactive'} - {self.media_type}"




from django.db import models
from django.core.exceptions import ValidationError

class SpotPubStore(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE, related_name="spot_pub")
    video = models.FileField(upload_to='spot_pubs/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        max_size = 10 * 1024 * 1024  # 10 Mo en octets

        if self.video:
            if self.video.size > max_size:
                raise ValidationError("La vidéo dépasse la taille maximale autorisée (10 Mo).")

    def __str__(self):
        return f"Spot Pub pour {self.store.name}"


# models.py
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
class StoreVisit(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='daily_visits')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    date = models.DateField(default=timezone.now)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('store', 'user', 'ip_address', 'date')

    def __str__(self):
        return f"{self.store.name} - {self.date} - {self.user or self.ip_address}"


# class AdInteraction(models.Model):
#     INTERACTION_CHOICES = [
#         ('like', 'Like'),
#         ('comment', 'Comment'),
#         ('share', 'Share'),
#     ]

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     ad = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="interactions")
#     interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'ad', 'interaction_type')  # Empêche les doublons

#     def __str__(self):
#         return f"{self.user.username} {self.interaction_type} {self.ad.title}"

#     def toggle_like(self):
#     # Si l'utilisateur a déjà liké cette publicité
#         if self.interaction_type == 'like':
#         # On supprime le like (passer à dislike)
#            self.delete()
#            self.ad.likes_count -= 1  # Décrémenter le nombre de likes
#            self.user.userpoints.points -= 1  # Réduire de 1 point le total de l'utilisateur
#            self.user.userpoints.save()
#            self.ad.save()
#         else:
#         # Si c'est un "dislike", on change pour "like" et on ajoute un like
#            self.interaction_type = 'like'
#            self.save()
#            self.ad.likes_count += 1  # Incrémenter le nombre de likes
#            self.user.userpoints.points += 1  # Ajouter 1 point pour un like
#            self.user.userpoints.save()
#            self.ad.save()


#     def add_comment(self, content):
#         """ Ajouter un commentaire à la publicité et gérer les points """
#         if not Comment.objects.filter(user=self.user, ad=self.ad).exists():
#             Comment.objects.create(user=self.user, ad=self.ad, content=content)
#             self.ad.comments_count += 1
#             self.user.userpoints.points += 2  # Ajouter 2 points pour un commentaire
#             self.ad.save()
#             self.user.userpoints.save()

#     def share_ad(self):
#         """ Ajouter un partage et gérer les points """
#         # Vérifier combien de fois l'utilisateur a partagé cette annonce
#         share_count = Share.objects.filter(user=self.user, ad=self.ad).count()

#         # Si l'utilisateur a partagé moins de 2 fois, permettre le partage
#         if share_count < 2:
#             if self.interaction_type != 'share':  # Si ce n'est pas déjà un partage
#                 self.interaction_type = 'share'
#                 self.save()
#                 self.ad.shares_count += 1
#                 self.ad.save()

#         # Lorsque l'utilisateur atteint 2 partages, ajouter les points
#         elif share_count == 1:
#             if self.interaction_type != 'share':  # Assurer que ce n'est pas déjà un partage
#                 self.interaction_type = 'share'
#                 self.save()
#                 self.ad.shares_count += 1
#                 self.ad.save()

#                 # Ajouter 5 points pour le 2ème partage
#                 self.user.userpoints.points += 5
#                 self.user.userpoints.save()