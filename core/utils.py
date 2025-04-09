

from .models import Cart

def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user, is_active=True)
    return cart

# utils.py

from hashlib import sha256
from django.http import HttpRequest

def get_client_ip(request: HttpRequest) -> str:
    """Récupère l'IP réelle de l'utilisateur."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_device_fingerprint(request: HttpRequest) -> str:
    """Génère une empreinte unique pour l'appareil."""
    user_agent = request.META.get('HTTP_USER_AGENT', '')  # User agent de l'utilisateur
    ip = get_client_ip(request)  # Récupère l'IP
    fingerprint = f"{user_agent}{ip}"  # Combine l'IP et l'user agent pour générer une empreinte
    return sha256(fingerprint.encode()).hexdigest()  # Retourne l'empreinte hashée
