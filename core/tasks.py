from celery import shared_task
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Advertisement, Share, UserPoints

@shared_task
def share_ad_and_award_points(user_id, ad_id):
    # Récupère l'utilisateur et la publicité
    user = User.objects.get(id=user_id)
    ad = Advertisement.objects.get(id=ad_id)

    # Créer une nouvelle entrée de partage
    Share.objects.create(user=user, ad=ad)

    # Ajouter les points pour le partage (3 points)
    user_points = UserPoints.objects.get(user=user)
    user_points.points += 3
    user_points.save()

    # Mettre à jour un compteur de partages dans l'objet Advertisement
    ad.shares_count += 1
    ad.save()

    return f"User {user.username} shared ad {ad.slug} and received 3 points."

from celery import shared_task
from .models import Advertisement, Share, UserPoints
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def handle_share_task(user_id, ad_id):
    try:
        user = User.objects.get(id=user_id)
        ad = Advertisement.objects.get(id=ad_id)

        # Créer un partage si non existant
        if not Share.objects.filter(user=user, ad=ad).exists():
            Share.objects.create(user=user, ad=ad)
            ad.shares_count += 1
            ad.save()

            user_points, _ = UserPoints.objects.get_or_create(user=user)
            user_points.points += 3
            user_points.save()
            return {"status": "success", "shares_count": ad.shares_count, "points": user_points.points}
        else:
            return {"status": "error", "message": "Déjà partagé"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
