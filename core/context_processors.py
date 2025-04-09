# myapp/context_processors.py

from .models import Cart
from .utils import get_or_create_cart  # Assurez-vous que vous avez une fonction get_or_create_cart

def cart(request):
    if request.user.is_authenticated:
        cart = get_or_create_cart(request.user)
    else:
        cart = None
    return {'cart': cart}
