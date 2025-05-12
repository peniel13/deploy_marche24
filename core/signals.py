from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product  # ou le bon modèle produit
from core.models import Notification, StoreSubscription  # adapte selon ton projet

@receiver(post_save, sender=Product)
def notify_subscribers_on_product_change(sender, instance, created, **kwargs):
    store = instance.store
    subscribers = StoreSubscription.objects.filter(store=store).select_related('user')

    if created:
        message = f"Un nouveau produit a été ajouté par {store.name}."
    else:
        message = f"Un produit a été mis à jour par {store.name}."

    for subscription in subscribers:
        Notification.objects.create(
            user=subscription.user,
            store=store,
            message=message
        )
