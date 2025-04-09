from django.shortcuts import render,redirect
from core.models import Store, Category, Product,Typestore,CategoryStore,Advertisement,UserPoints,AdInteraction
from .models import WebsiteLink,Publicite
from core.forms import AdInteractionForm
from django.db.models import Q

# Create your views here.
def my_view(request):
    form = AdInteractionForm()  # Initialisation par défaut
    if request.method == "POST":
        form = AdInteractionForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, "template.html", {"form": form})  # ✅ Toujours défini

def index(request):
    # Récupérer les 3 derniers magasins
    stores = Store.objects.all().order_by('-created_at')[:3]
    
    favorite_stores = Store.objects.filter(favoritestore=True).order_by('-created_at')
    # Calculer la note moyenne de chaque store à l'aide d'agrégation
    for store in stores:
        testimonials = Testimonial.objects.filter(store=store)
        if testimonials.exists():
            store.average_rating = testimonials.aggregate(Avg('rating'))['rating__avg']
        else:
            store.average_rating = 0

    # Récupérer les 3 derniers produits
    products = Product.objects.all().order_by('-created_at')[:3]

    # Calculer la note moyenne de chaque produit à l'aide d'agrégation
    for product in products:
        testimonials = Testimonialproduct.objects.filter(product=product)  # Récupère les témoignages associés
        if testimonials.exists():
            product.average_rating = testimonials.aggregate(Avg('rating'))['rating__avg']
        else:
            product.average_rating = 0

    # Récupérer les liens des sites web et implémenter la recherche
    websites = WebsiteLink.objects.all()
    search_query = request.GET.get('search', '').strip()  # On enlève les espaces en début et fin
    if search_query:
    # On remplace les espaces multiples par un espace unique et on effectue la recherche
       search_query = ' '.join(search_query.split())
       websites = websites.filter(name__icontains=search_query) | websites.filter(description__icontains=search_query)


    # Pagination des WebsiteLinks
    paginator = Paginator(websites, 3)  # 3 WebsiteLinks par page
    page = request.GET.get('page')

    try:
        websites = paginator.page(page)
    except PageNotAnInteger:
        websites = paginator.page(1)
    except EmptyPage:
        websites = paginator.page(paginator.num_pages)
     # Récupérer les publicités vidéo
    ads = Advertisement.objects.all().order_by('-created_at')[:3]  # Trie les publicités par date de création décroissante
    form = AdInteractionForm()
    # Récupérer la dernière publicité active pour affichage dans le modal
    
    # Vérifie si l'utilisateur est authentifié
    if request.user.is_authenticated:
        # Récupérer les points de l'utilisateur pour l'affichage dans la vue (optionnel)
        user_points = UserPoints.objects.filter(user=request.user).first()
        if not user_points:
            user_points = UserPoints.objects.create(user=request.user, points=0)

        # Vérifier si l'utilisateur a liké chaque publicité
        for ad in ads:
            ad.user_has_liked = AdInteraction.objects.filter(
                user=request.user, 
                ad=ad, 
                interaction_type='like'
            ).exists()
    else:
        # Si l'utilisateur n'est pas authentifié, on donne 0 points
        user_points = None
        for ad in ads:
            ad.user_has_liked = False

    # Gérer les interactions
    if request.method == 'POST':
        form = AdInteractionForm(request.POST)
        if form.is_valid():
            ad = form.cleaned_data['ad']
            interaction_type = form.cleaned_data['interaction_type']
            
            # Vérifier si l'utilisateur a déjà effectué cette interaction
            if request.user.is_authenticated and not AdInteraction.objects.filter(user=request.user, ad=ad, interaction_type=interaction_type).exists():
                # Créer l'interaction
                AdInteraction.objects.create(
                    user=request.user,
                    ad=ad,
                    interaction_type=interaction_type
                )
                
                # Ajouter des points pour l'utilisateur
                points_to_add = 0
                if interaction_type == 'like':
                    points_to_add = 1
                elif interaction_type == 'comment':
                    points_to_add = 2
                elif interaction_type == 'share':
                    points_to_add = 5

                # Ajouter les points à l'utilisateur si authentifié
                if request.user.is_authenticated:
                    user_points.add_ad_points(points_to_add)
                
                # Rediriger pour éviter la soumission multiple
                return redirect('advertisement_list')
            
              
      # Les 3 dernières publicités
    # Passer toutes les données nécessaires au template
    return render(request, "base/index.html", {  
        'stores': stores,  # Liste des 3 derniers magasins
        'favorite_stores':favorite_stores,
        'products': products,  # Liste des 3 derniers produits
        'websites': websites,  # Liens des sites web avec pagination
        'paginator': paginator,  # Paginator pour la pagination des WebsiteLinks
        'rating_choices': Testimonial.RATING_CHOICES,  # Options de note pour les témoignages
        'range_10': range(1, 11),  # Plage des étoiles pour l'affichage des notes
        'ads': ads,
        'form': form,
        'user_points': user_points,
    })

def apropos(request):
    return render(request,'base/apropos.html')

def politique(request):
    return render(request,'base/politique.html')

def contact(request):
    return render(request,'base/contact.html')

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Sum

from django.contrib.auth.decorators import login_required

from django.db.models import Avg
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from core.models import Product, Category, Testimonialproduct  # Assurez-vous d'importer les bons modèles

def list_product(request):
    # Récupère tous les produits de tous les magasins
    products = Product.objects.all().order_by('-created_at')
    favorite_stores = Store.objects.filter(favoritestore=True).order_by('-created_at')
    # Filtrage par catégorie
    category_filter = request.GET.get('categorie', '')
    if category_filter:
        products = products.filter(category__id=category_filter)

    # Filtrage par nom
    product_name = request.GET.get('nom', '').strip()  # On enlève les espaces en début et fin
    if product_name:
    # On remplace les espaces multiples par un espace unique et on effectue la recherche
        product_name = ' '.join(product_name.split())
        products = products.filter(name__icontains=product_name) | products.filter(description__icontains=product_name)

    # Filtrage par prix
    prix_min = request.GET.get('prix_min', '')
    prix_max = request.GET.get('prix_max', '')
    if prix_min:
        try:
            prix_min = float(prix_min)
            products = products.filter(price__gte=prix_min)
        except ValueError:
            pass  # Ignore les valeurs incorrectes
    if prix_max:
        try:
            prix_max = float(prix_max)
            products = products.filter(price__lte=prix_max)
        except ValueError:
            pass  # Ignore les valeurs incorrectes

    # Calcul de la moyenne des ratings pour chaque produit
    for product in products:
        testimonials = Testimonialproduct.objects.filter(product=product)  # Récupère les témoignages associés
        if testimonials.exists():
            product.average_rating = testimonials.aggregate(Avg('rating'))['rating__avg']
        else:
            product.average_rating = 0

    # Filtrage par rating
    min_rating = request.GET.get('rating_min', '')
    if min_rating:
        try:
            min_rating = float(min_rating)
            products = products.filter(average_rating__gte=min_rating)
        except ValueError:
            pass  # Ignore les valeurs incorrectes

    # Pagination
    paginator = Paginator(products, 6)  # 6 produits par page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Récupère toutes les catégories pour le filtrage
    categories = Category.objects.all()

    # Plage de 1 à 10 pour les étoiles de rating
    range_10 = range(1, 11)
    total_products = Product.objects.filter().count()
    total_categories = Category.objects.count()

    context = {
        'products': products,
        'favorite_stores':favorite_stores,
        'categories': categories,
        'product_name': product_name,
        'category_filter': category_filter,
        'prix_min': prix_min,
        'prix_max': prix_max,
        'min_rating': min_rating,
        'paginator': paginator,
        'range_10': range_10,  # Plage pour les étoiles
        'total_products': total_products,  # Nombre total de produits
        'total_categories': total_categories,  # Nombre total de catégories
    }

    return render(request, 'base/list_product.html', context)


from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg
from core.models import Store, Testimonial

def list_store(request):
    stores = Store.objects.all().order_by('-created_at')
    favorite_stores = Store.objects.filter(favoritestore=True).order_by('-created_at')
    # Filtrage par nom
    store_name = request.GET.get('nom', '').strip()  # On enlève les espaces en début et en fin
    if store_name:
    # On remplace les espaces multiples par un seul espace et on effectue la recherche
       store_name = ' '.join(store_name.split())
       stores = stores.filter(name__icontains=store_name)
    
     # 🔍 **Filtrage par adresse**
    store_address = request.GET.get('adresse', '').strip()
    if store_address:
        store_address = ' '.join(store_address.split())  # Supprime les espaces multiples
        stores = stores.filter(adresse__icontains=store_address)

    # Filtrage par typestore
    typestore_id = request.GET.get('typestore')
    if typestore_id:
        stores = stores.filter(typestore_id=typestore_id)

    # Filtrage par categorystore
    categorystore_id = request.GET.get('categorystore')
    if categorystore_id:
        stores = stores.filter(categorystore_id=categorystore_id)

    # Pagination - 4 stores par page
    paginator = Paginator(stores, 6)
    page_number = request.GET.get('page')

    try:
        stores_page = paginator.page(page_number)
    except PageNotAnInteger:
        stores_page = paginator.page(1)
    except EmptyPage:
        stores_page = paginator.page(paginator.num_pages)

    # Calcul de la note moyenne de chaque store à l'aide d'agrégation
    for store in stores_page:
        testimonials = Testimonial.objects.filter(store=store)
        if testimonials.exists():
            store.average_rating = testimonials.aggregate(Avg('rating'))['rating__avg']
        else:
            store.average_rating = 0
    
    typestores = Typestore.objects.all()  # Charger tous les typestores
    categorystores = CategoryStore.objects.all()  # Charger toutes les catégories de stores pour l'initialisation
    total_stores = Store.objects.filter().count()
    total_categorystores = CategoryStore.objects.count()
    total_typestores = Typestore.objects.count()
    context = {
        'stores': stores_page,
        'favorite_stores':favorite_stores,
        'store_name': store_name,
        'store_address': store_address,
        'typestores': typestores,
        'categorystores': categorystores,
        'rating_choices': Testimonial.RATING_CHOICES,
        'range_10': range(1, 11),  # Créer la plage de 1 à 10 pour les étoiles
        'total_stores': total_stores,  # Nombre total de stores
        'total_categorystores': total_categorystores,  # Nombre total de catégories
        'total_typestores': total_typestores,  # Nombre total de types de stores
    }

    return render(request, "base/list_store.html", context)

from django.http import JsonResponse

def load_cellules(request):
    typestore_id = request.GET.get('typestore')
    categorystores = CategoryStore.objects.filter(typestore_id=typestore_id).values('id', 'nom')
    return JsonResponse(list(categorystores), safe=False)

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Video

from django.shortcuts import render, get_object_or_404
from .models import Video

def video_list(request):
    # Récupère toutes les vidéos
    videos = Video.objects.all()

    # Retourne à un template pour afficher la liste des vidéos
    return render(request, 'base/video_list.html', {'videos': videos})

def fetch_video(request, slug):
    # Récupère la vidéo en fonction du slug
    video = get_object_or_404(Video, slug=slug)

    # Vérifie si le fichier vidéo existe
    if not video.video_file:
        raise Http404("Vidéo non trouvée.")

    # Ouvre le fichier vidéo
    video_file = video.video_file.open()

    # Crée une réponse HTTP avec le contenu du fichier vidéo
    response = HttpResponse(video_file, content_type='video/mp4')

    # Définir le type de contenu pour permettre la lecture dans un lecteur vidéo
    response['Content-Disposition'] = f'inline; filename={video.title}.mp4'

    return response


from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from .models import Publicite  # Assure-toi que le modèle Publicite est bien importé

def fetch_video_pub(request, slug):
    # Récupère la publicité en fonction du slug
    publicite = get_object_or_404(Publicite, slug=slug)

    # Vérifie si le fichier vidéo existe
    if not publicite.video_file:
        raise Http404("Vidéo non trouvée.")

    # Ouvre le fichier vidéo
    video_file = publicite.video_file.open()

    # Crée une réponse HTTP avec le contenu du fichier vidéo
    response = HttpResponse(video_file, content_type='video/mp4')

    # Définir le type de contenu pour permettre la lecture dans un lecteur vidéo
    response['Content-Disposition'] = f'inline; filename={publicite.title}.mp4'

    return response

from django.shortcuts import render
from .models import Publicite

def publicite_video_list(request):
    # Récupère toutes les publicités vidéo
    publicites = Publicite.objects.all()

    # Retourne à un template pour afficher la liste des publicités vidéo
    return render(request, 'base/publicite_video_list.html', {'publicites': publicites})
