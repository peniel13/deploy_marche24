from django import forms
from .models import Store, Category, Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from simplemathcaptcha.fields import MathCaptchaField

class RegisterForm(UserCreationForm):
    email= forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder":"Enter email adress"}))
    username= forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"Enter username"}))
    password1= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"Enter password"}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"confirm password"}))

    captcha = MathCaptchaField()
    class Meta:
        model = get_user_model()
        fields = ["email","username","password1","password2"]
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas. Veuillez réessayer.")

        return cleaned_data
    

from django import forms
from django.contrib.auth import get_user_model

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
    # Ajoute ici toutes tes communes
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
    # Ajoute ici toutes tes villes
]

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter firstname"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter lastname"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter username"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "Enter email address"}))
    profile_pic = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Upload image"}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter address"}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter phone"}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "Enter bio"}))
    role = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter role"}))

    # Nouveaux champs pour ciblage
    sex = forms.ChoiceField(choices=SEX_CHOICES, required=False, widget=forms.Select(attrs={"class": "form-control"}))
    commune = forms.ChoiceField(choices=COMMUNE_CHOICES, required=False, widget=forms.Select(attrs={"class": "form-control"}))
    city = forms.ChoiceField(choices=CITY_CHOICES, required=False, widget=forms.Select(attrs={"class": "form-control"}))
    interests = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: sport, mode, jeux vidéo"}))

    class Meta:
        model = get_user_model()
        fields = [
            "first_name", "last_name", "username", "email", "address", "bio", "phone",
            "role", "profile_pic", "sex", "commune", "city", "interests"
        ]

# class UpdateProfileForm(forms.ModelForm):
#     first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter firstname"}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter lastname"}))
#     username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter username"}))
#     email = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "Enter email address"}))
#     profile_pic = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Upload image"}))
#     address = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter address"}))
#     phone = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter phone"}))
#     bio = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "Enter bio"}))
#     role = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter role"}))

#     class Meta:
#         model = get_user_model()
#         fields = ["first_name", "last_name", "username", "email", "address", "bio", "phone", "role", "profile_pic"]

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description','adresse',"thumbnail",'typestore','categorystore','latitude','longitude']  # Retiré le champ 'slug', car il est généré automatiquement
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez le nom du store'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez la description du store'
            }),
            'adresse': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez la description du store'
            }),
            'typestore': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'categorystore': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'latitude': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Latitude du store',
                'step': '0.000001'  # Pour plus de précision sur les décimales
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Longitude du store',
                'step': '0.000001'  # Pour plus de précision sur les décimales
            }),
        }

from django import forms
from .models import Testimonial,Testimonialproduct # Assurez-vous que le modèle Testimonial est importé

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['content', 'rating']  # Le champ 'store' est exclu car il est automatiquement pris en compte
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Partagez votre témoignage'
            }),
            'rating': forms.Select(choices=Testimonial.RATING_CHOICES, attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
        }

class TestimonialproductForm(forms.ModelForm):
    class Meta:
        model = Testimonialproduct
        fields = ['content', 'rating']  # Le champ 'store' est exclu car il est automatiquement pris en compte
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Partagez votre témoignage'
            }),
            'rating': forms.Select(choices=Testimonial.RATING_CHOICES, attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
        }


from .models import ContactProduct

class ContactProductForm(forms.ModelForm):
    class Meta:
        model = ContactProduct
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'description']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre adresse email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre numéro de téléphone'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Décrivez votre demande...',
                'rows': 4
            }),
        }

    # Optionnel: validation personnalisée pour le numéro de téléphone
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError("Le numéro de téléphone ne doit contenir que des chiffres.")
        return phone_number



from .models import ContactStore

class ContactStoreForm(forms.ModelForm):
    class Meta:
        model = ContactStore
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'description']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre adresse email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre numéro de téléphone'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Décrivez votre demande...',
                'rows': 4
            }),
        }

    # Optionnel: validation personnalisée pour le numéro de téléphone
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError("Le numéro de téléphone ne doit contenir que des chiffres.")
        return phone_number


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez le nom du store'
            }),
            }

from .models import Product,Photo,CartItem# Assurez-vous que le modèle Product est importé
from django import forms
from .models import Product

from decimal import Decimal

from django import forms
from .models import Product, Category
from django import forms
from .models import Product, Category

from django import forms
from .models import Product, Category,AssignerCategory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name',  'description', 'price', 'stock', 'image', 'image_galerie']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Application du même style pour chaque champ
        self.fields['name'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Entrez le nom du produit'
        })
        # self.fields['category'].widget.attrs.update({
        #     'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        # })
        self.fields['description'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Décrivez le produit',
            'rows': 4
        })
        self.fields['price'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Entrez le prix'
        })
        self.fields['stock'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Indiquez le stock disponible'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
        self.fields['image_galerie'].widget.attrs.update({
            'class': 'hidden',  # Cacher le champ image_galerie par défaut
        })


    def save(self, commit=True, *args, **kwargs):
        product = super().save(commit=False, *args, **kwargs)

        # Appliquer la commission de 30%
        if product.price is not None:
            commission = product.price * Decimal('0.30')  # Assurez-vous que la commission est en Decimal
            product.price_with_commission = product.price + commission

        if commit:
            product.save()

        return product


from django import forms
from .models import AssignerCategory, Category

class AssignerCategoryForm(forms.ModelForm):
    class Meta:
        model = AssignerCategory
        fields = ['category']

    def __init__(self, *args, **kwargs):
        store = kwargs.pop('store', None)  # Récupérer le store depuis la vue
        super().__init__(*args, **kwargs)

        # Filtrer les catégories disponibles pour ce store uniquement
        if store:
            self.fields['category'].queryset = Category.objects.filter(store=store)

        # Appliquer des styles aux champs
        self.fields['category'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        })

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name', 'category', 'description', 'price', 'stock', 'image', 'image_galerie']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Application du même style pour chaque champ
#         self.fields['name'].widget.attrs.update({
#             'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
#             'placeholder': 'Entrez le nom du produit'
#         })
#         self.fields['category'].widget.attrs.update({
#             'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
#         })
#         self.fields['description'].widget.attrs.update({
#             'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
#             'placeholder': 'Décrivez le produit',
#             'rows': 4
#         })
#         self.fields['price'].widget.attrs.update({
#             'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
#             'placeholder': 'Entrez le prix'
#         })
#         self.fields['stock'].widget.attrs.update({
#             'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
#             'placeholder': 'Indiquez le stock disponible'
#         })
#         self.fields['image'].widget.attrs.update({
#             'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
#         })
#         self.fields['image_galerie'].widget.attrs.update({
#             'class': 'hidden',  # Cacher le champ image_galerie par défaut
#         })
    
    
#     # Redéfinir la méthode save() pour appliquer la commission de 30% sur le prix
#     def save(self, commit=True, *args, **kwargs):
#         product = super().save(commit=False, *args, **kwargs)

#         # Appliquer la commission de 30%
#         if product.price is not None:
#             commission = product.price * Decimal('0.30')  # Assurez-vous que la commission est en Decimal
#             product.price_with_commission = product.price + commission
        
#         if commit:
#             product.save()

#         return product
    

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })

from django import forms
from .models import Cart, CartItem

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = []  # Le modèle Cart n'a pas de champs directement modifiables via un formulaire

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Le formulaire ne manipule pas directement des champs dans Cart, 
        # mais plutôt les CartItems associés au panier
        self.fields['quantity'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Quantité'
        })


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']  # Le champ 'quantity' permet de modifier la quantité d'un produit dans le panier

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Quantité',
        })

from django import forms
from .models import MobileMoneyPayment
from django.core.exceptions import ValidationError
# forms.py
from django import forms
from .models import MobileMoneyPayment

class MobileMoneyPaymentForm(forms.ModelForm):
    class Meta:
        model = MobileMoneyPayment
        fields = ['first_name', 'last_name', 'transaction_number', 'transaction_id', 'phone_number', 'delivery_option']
    
    def clean_transaction_id(self):
        transaction_id = self.cleaned_data['transaction_id']
        if MobileMoneyPayment.objects.filter(transaction_id=transaction_id).exists():
            raise forms.ValidationError("Ce numéro de transaction a déjà été utilisé.")
        return transaction_id

from django import forms
from .models import CommandeLivraison

class CommandeLivraisonForm(forms.ModelForm):
    class Meta:
        model = CommandeLivraison
        fields = [
            'nom', 'prenom', 'email', 'numero_tel', 'adresse_livraison', 
            'description_colis', 'endroit_recuperation', 'numero_id_colis'
        ]
        
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez votre nom'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez votre prénom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez votre email'
            }),
            'numero_tel': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez votre numéro de téléphone'
            }),
            'adresse_livraison': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez l\'adresse de livraison'
            }),
            'description_colis': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Description du colis'
            }),
            'endroit_recuperation': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Endroit de récupération'
            }),
            'numero_id_colis': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Numéro d\'ID du colis'
            }),
        }

    # Optionnel : Personnaliser la validation
    def clean_numero_tel(self):
        numero_tel = self.cleaned_data.get('numero_tel')
        if not numero_tel.isdigit():
            raise forms.ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres.")
        return numero_tel

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise forms.ValidationError("Veuillez entrer un email valide.")
        return email


from django import forms
from .models import ProductPoints

class ProductPointsForm(forms.ModelForm):
    class Meta:
        model = ProductPoints
        fields = ['name', 'points_required', 'description', 'image']  # Mise à jour du champ 'product' vers 'name'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
        self.fields['points_required'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Entrez le nombre de points nécessaires'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Décrivez le produit',
            'rows': 4
        })
        self.fields['image'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })

from django import forms
from .models import ContactProductPoints

class ContactProductPointsForm(forms.ModelForm):
    class Meta:
        model = ContactProductPoints
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'description']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre adresse email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Votre numéro de téléphone'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Décrivez votre demande...',
                'rows': 4
            }),
        }

    # Optionnel: validation personnalisée pour le numéro de téléphone
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError("Le numéro de téléphone ne doit contenir que des chiffres.")
        return phone_number


from django import forms
from .models import Advertisement
from django import forms
from .models import Advertisement
from core.models import SEX_CHOICES, COMMUNE_CHOICES, CITY_CHOICES  # adapte le chemin selon ton projet
class AdvertisementForm(forms.ModelForm):
    target_communes = forms.MultipleChoiceField(
        choices=COMMUNE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )
    target_cities = forms.MultipleChoiceField(
        choices=CITY_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Advertisement
        fields = [
            'title', 'description', 'media_type', 'media_file', 'url',
            'target_all_users', 'target_sex', 'target_communes',
            'target_cities', 'target_keywords', 'target_address_keywords',
            'target_latitude', 'target_longitude', 'target_radius_km',
            'max_target_users','max_likes', 'max_shares', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'media_type': forms.Select(attrs={'class': 'form-control'}),
            'media_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'target_all_users': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'target_sex': forms.Select(choices=SEX_CHOICES, attrs={'class': 'form-control'}),
            'target_keywords': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'sport, mode, jeux...', 'rows': 2
            }),
            'target_address_keywords': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'quartier, rue, avenue...', 'rows': 2
            }),
            'target_latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'target_longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'target_radius_km': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_target_users': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_likes': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_shares': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_target_communes(self):
        return self.cleaned_data.get('target_communes', [])

    def clean_target_cities(self):
        return self.cleaned_data.get('target_cities', [])

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.target_communes = self.cleaned_data.get('target_communes', [])
        instance.target_cities = self.cleaned_data.get('target_cities', [])
        if commit:
            instance.save()
            self.save_m2m()
        return instance


# class AdvertisementForm(forms.ModelForm):
#     class Meta:
#         model = Advertisement
#         fields = ['title', 'description', 'media_type', 'media_file', 'url']
        
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
#             'media_type': forms.Select(attrs={'class': 'form-control'}),
#             'media_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#             'url': forms.URLInput(attrs={'class': 'form-control'}),
#         }

from django import forms
from .models import AdInteraction

class AdInteractionForm(forms.ModelForm):
    class Meta:
        model = AdInteraction
        fields = ['ad', 'interaction_type']

        widgets = {
            'ad': forms.Select(attrs={'class': 'form-control'}),
            'interaction_type': forms.Select(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Le champ 'content' pour le texte du commentaire
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Votre commentaire...'})
        }


# forms.py
from django import forms
from .models import SpotPubStore

class SpotPubStoreForm(forms.ModelForm):
    class Meta:
        model = SpotPubStore
        fields = ['video']

    def clean_video(self):
        video = self.cleaned_data.get('video')
        max_size = 10 * 1024 * 1024  # 10 Mo

        if video and video.size > max_size:
            raise forms.ValidationError("La vidéo dépasse la taille maximale autorisée (10 Mo).")
        return video


from .models import LotteryParticipation
from django import forms
from .models import LotteryParticipation
class LotteryParticipationForm(forms.ModelForm):
    class Meta:
        model = LotteryParticipation
        fields = ['full_name', 'phone_number', 'id_transaction']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.lottery = kwargs.pop('lottery', None)
        super().__init__(*args, **kwargs)

        # Style unifié pour les champs
        self.fields['full_name'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Votre nom complet'
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Votre numéro de téléphone'
        })
        self.fields['id_transaction'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'ID de transaction'
        })

    def clean(self):
        cleaned_data = super().clean()
        if self.lottery.current_participant_count() >= self.lottery.max_participants:
            raise forms.ValidationError("Le nombre maximum de participants a été atteint.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        instance.lottery = self.lottery
        if commit:
            instance.save()
        return instance

from django import forms
from .models import StoreSubscription

class StoreSubscriptionForm(forms.ModelForm):
    class Meta:
        model = StoreSubscription
        fields = ['store']  # Le champ "store" est nécessaire pour créer une nouvelle souscription

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Passer l'utilisateur lors de l'initialisation du formulaire
        super().__init__(*args, **kwargs)
        if user:
            # Le formulaire doit seulement permettre l'abonnement à un magasin qui n'est pas encore souscrit par l'utilisateur
            self.fields['store'].queryset = Store.objects.exclude(subscribers=user)
        else:
            self.fields['store'].queryset = Store.objects.none()

from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Application de styles uniformes pour les champs
        self.fields['title'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Titre de la notification'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Description de la notification'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })

# class MobileMoneyPaymentForm(forms.ModelForm):
#     class Meta:
#         model = MobileMoneyPayment
#         fields = ['transaction_number', 'transaction_id', 'first_name', 'last_name']
#         widgets = {
#             'transaction_number': forms.TextInput(attrs={
#                 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
#                 'placeholder': 'Numéro de transaction'
#             }),
#             'transaction_id': forms.TextInput(attrs={
#                 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
#                 'placeholder': 'ID de transaction'
#             }),
#             'first_name': forms.TextInput(attrs={
#                 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
#                 'placeholder': 'Prénom'
#             }),
#             'last_name': forms.TextInput(attrs={
#                 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
#                 'placeholder': 'Nom'
#             }),
            
#         }

#     def clean_transaction_id(self):
#         transaction_id = self.cleaned_data['transaction_id']
#         if MobileMoneyPayment.objects.filter(transaction_id=transaction_id).exists():
#             raise ValidationError("Ce numéro de transaction a déjà été utilisé. Veuillez utiliser un numéro de transaction unique.")
#         return transaction_id


# from django import forms
# from .models import MobileMoneyTransaction

# class MobileMoneyTransactionForm(forms.ModelForm):
#     class Meta:
#         model = MobileMoneyTransaction
#         fields = ['mobile_money_number', 'transaction_id', 'amount']

#     def __init__(self, *args, **kwargs):
#         # S'assurer que le champ 'amount' est en lecture seule
#         super().__init__(*args, **kwargs)
#         if self.instance and self.instance.order:
#             self.fields['amount'].initial = self.instance.order.total_amount
#             self.fields['amount'].widget.attrs['readonly'] = True

#     def clean_transaction_id(self):
#         transaction_id = self.cleaned_data.get('transaction_id')
#         if MobileMoneyTransaction.objects.filter(transaction_id=transaction_id).exists():
#             raise forms.ValidationError("Cet ID de transaction a déjà été utilisé.")
#         return transaction_id

# from django import forms
# from .models import Order, OrderItem

# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['user', 'store', 'status', 'total_amount']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance:
#             self.fields['total_amount'].widget.attrs['readonly'] = True  # Montant total en lecture seule
#             self.fields['status'].widget.attrs['class'] = 'form-control'  # Appliquer un style personnalisé si besoin

# class OrderItemForm(forms.ModelForm):
#     class Meta:
#         model = OrderItem
#         fields = ['product', 'quantity', 'price_at_time_of_order']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance:
#             self.fields['price_at_time_of_order'].widget.attrs['readonly'] = True  # En lecture seule

