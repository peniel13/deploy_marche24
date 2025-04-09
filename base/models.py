from django.db import models




class WebsiteLink(models.Model):
    # Champ pour l'image de profil
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    # Champ pour le nom
    name = models.CharField(max_length=100)
    
    # Champ pour ajouter un lien vers un site web
    website_link = models.URLField(max_length=200, null=True, blank=True)
    
    # Champ pour la description
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Video(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="videos")
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    video_file = models.FileField(upload_to="videos/")
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    featured = models.BooleanField(default=False)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Publicite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="publicites")
    title = models.CharField(max_length=100, unique=True)  # Titre de la publicité
    slug = models.SlugField(blank=True, null=True)  # Slug automatique basé sur le titre
    description = models.TextField()  # Description de la publicité
    video_file = models.FileField(upload_to="publicites/videos/")  # Vidéo associée à la publicité
    thumbnail = models.ImageField(upload_to="publicites/thumbnails/", blank=True, null=True)  # Image miniature
    created = models.DateField(auto_now_add=True)  # Date de création
    updated = models.DateField(auto_now=True)  # Date de mise à jour
    featured = models.BooleanField(default=False)  # Si la publicité est mise en avant
    link = models.URLField(max_length=200, blank=True, null=True)  # Lien vers un site web pour la publicité

    def save(self, *args, **kwargs):
        # Crée un slug basé sur le titre si celui-ci n'est pas défini
        if not self.slug:
            self.slug = slugify(self.title)
        super(Publicite, self).save(*args, **kwargs)

    def __str__(self):
        return self.title  # Renvoie le titre de la publicité

