# core/tasks.py

from celery import shared_task
from django.contrib.auth import get_user_model
from core.models import Advertisement, Share, UserPoints

User = get_user_model()

@shared_task
def process_ad_share(user_id, ad_id):
    try:
        user = User.objects.get(id=user_id)
        ad = Advertisement.objects.get(id=ad_id)

        # Ne pas doubler les partages
        if not Share.objects.filter(user=user, ad=ad).exists():
            Share.objects.create(user=user, ad=ad)

            user_points, created = UserPoints.objects.get_or_create(user=user)
            user_points.points += 3  # ou 5 selon ton système
            user_points.save()

            ad.shares_count += 1
            ad.save()
    except Exception as e:
        print(f"[process_ad_share] Erreur : {e}")
