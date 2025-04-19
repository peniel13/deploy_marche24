from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Définir le paramètre par défaut pour le module Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deploy_marche24.settings')

# Créer une instance de Celery
app = Celery('deploy_marche24')

# Utiliser la configuration de Celery définie dans les paramètres de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charger les tâches de toutes les applications Django installées
app.autodiscover_tasks()

