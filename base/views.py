from django.shortcuts import render,redirect
from core.models import Store, Category, Product,Typestore,CategoryStore,Advertisement,UserPoints,AdInteraction,UserLocation,Share,PopUpAdvertisement
from .models import WebsiteLink,Publicite
from core.forms import AdInteractionForm
from django.db.models import Q
from django.db import transaction

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

    if request.user.is_authenticated:
        user = request.user
        user_points = UserPoints.objects.filter(user=user).first()
        if not user_points:
            user_points = UserPoints.objects.create(user=user, points=0)

        user_sex = getattr(user, 'sex', None)
        user_commune = (getattr(user, 'commune', '') or '').lower()
        user_city = (getattr(user, 'city', '') or '').lower()
        user_address = (getattr(user, 'address', '') or '').lower().split()
        user_keywords = (getattr(user, 'interests', '') or '').lower().split(',')

        user_location = UserLocation.objects.filter(user=user).first()
        user_lat = float(user_location.latitude) if user_location and user_location.latitude else None
        user_lon = float(user_location.longitude) if user_location and user_location.longitude else None

        filtered_ads = []

        for ad in ads:
            show_to_user = False

            if ad.target_all_users:
                show_to_user = True
            else:
                match_count = 0
                total_conditions = 0

                # Sexe ciblé
                if ad.target_sex:
                    total_conditions += 1
                    if ad.target_sex == user_sex:
                        match_count += 1

                # Commune ciblée
                if ad.target_communes:
                    total_conditions += 1
                    ad_communes = [c.lower() for c in ad.target_communes]
                    if user_commune in ad_communes:
                        match_count += 1

                # Ville ciblée
                if ad.target_cities:
                    total_conditions += 1
                    ad_cities = [c.lower() for c in ad.target_cities]
                    if user_city in ad_cities:
                        match_count += 1

                # Mots-clés ciblés
                if ad.target_keywords:
                    total_conditions += 1
                    ad_keywords = [k.strip().lower() for k in ad.target_keywords.split(',')]
                    if any(k in user_keywords for k in ad_keywords):
                        match_count += 1

                # Adresse ciblée (sous forme de mots-clés dans une phrase)
                if ad.target_address_keywords:
                    total_conditions += 1
                    ad_address_keywords = [k.strip().lower() for k in ad.target_address_keywords.split(',')]
                    if any(k in user_address for k in ad_address_keywords):
                        match_count += 1

                # Ciblage géographique par distance
                if ad.target_latitude and ad.target_longitude and ad.target_radius_km and user_lat and user_lon:
                    total_conditions += 1
                    distance = ((user_lat - float(ad.target_latitude))**2 + (user_lon - float(ad.target_longitude))**2) ** 0.5 * 111  # approx conversion deg -> km
                    if distance <= float(ad.target_radius_km):
                        match_count += 1

                if total_conditions > 0 and match_count == total_conditions:
                    show_to_user = True

            if show_to_user:
                if ad.max_target_users:
                    with transaction.atomic():
                        ad = Advertisement.objects.select_for_update().get(id=ad.id)
                        if ad.targeted_users.count() >= ad.max_target_users:
                            show_to_user = False
                        elif not ad.targeted_users.filter(id=user.id).exists():
                            ad.targeted_users.add(user)
                elif not ad.targeted_users.filter(id=user.id).exists():
                    ad.targeted_users.add(user)

            ad.user_has_liked = AdInteraction.objects.filter(
                user=user,
                ad=ad,
                interaction_type='like'
            ).exists()

            if show_to_user:
                filtered_ads.append(ad)

        ads = filtered_ads

    else:
        user_points = None
        for ad in ads:
            ad.user_has_liked = False
        ads = [ad for ad in ads if ad.target_all_users]

    if request.method == 'POST':
        form = AdInteractionForm(request.POST)
        if form.is_valid():
            ad = form.cleaned_data['ad']
            interaction_type = form.cleaned_data['interaction_type']

            if request.user.is_authenticated and not AdInteraction.objects.filter(user=request.user, ad=ad, interaction_type=interaction_type).exists():
                AdInteraction.objects.create(
                    user=request.user,
                    ad=ad,
                    interaction_type=interaction_type
                )

                points_to_add = {
                    'like': 1,
                    'comment': 2,
                    'share': 3
                }.get(interaction_type, 0)

                user_points.add_ad_points(points_to_add)

                return redirect('advertisement_list')
    else:
        form = AdInteractionForm()

    user_shares = []
    ad_absolute_urls = {}

    if request.user.is_authenticated:
        # Récupère toutes les pubs déjà partagées par l'utilisateur
        shared_ads = Share.objects.filter(user=request.user, ad__in=ads).values_list('ad_id', flat=True)
        user_shares = list(shared_ads)
   
    # Génère les URLs absolues pour chaque publicité
    ad_absolute_urls = {ad.id: request.build_absolute_uri(ad.get_absolute_url()) for ad in ads}      

    ad_popup = PopUpAdvertisement.objects.filter(is_active=True).first()          
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
        'user_shares': user_shares,
        'ad_absolute_urls': ad_absolute_urls,
        'ad_popup': ad_popup,
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
    stores = Store.objects.filter(is_active=True).order_by('-created_at')
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
