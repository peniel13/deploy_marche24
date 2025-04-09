from django.contrib import admin
from .models import WebsiteLink
# Register your models here.

admin.site.register(WebsiteLink)

from django.contrib import admin
from .models import Video
from .forms import VideoForm

class VideoAdmin(admin.ModelAdmin):
    form = VideoForm  # Utilise notre formulaire personnalisé pour l'administration

    list_display = ('title', 'user', 'created', 'updated', 'featured', )
    list_filter = ('featured', 'created')
    search_fields = ('title', 'description', 'user__username')  # Recherche par titre, description ou utilisateur
    prepopulated_fields = {'slug': ('title',)}  # Génère automatiquement le slug à partir du titre
    ordering = ('-created',)  # Tri par date de création (descendant)

    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'slug', 'description', 'video_file', 'thumbnail', 'featured')
        }),
        ('Dates', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created', 'updated')  # Ces champs sont en lecture seule dans l'admin

    # Personnalisation de l'affichage dans la liste des vidéos
    def video_file_link(self, obj):
        return f'<a href="{obj.video_file.url}" target="_blank">Voir la vidéo</a>'
    video_file_link.allow_tags = True
    video_file_link.short_description = 'Vidéo'

    # Ajouter la colonne 'video_file_link' à l'affichage dans l'admin
    list_display = ('title', 'user', 'video_file_link', 'created', 'updated', 'featured',)

# Enregistrer le modèle et son interface d'administration
admin.site.register(Video, VideoAdmin)


from django.contrib import admin
from .models import Publicite
from .forms import PubliciteForm

class PubliciteAdmin(admin.ModelAdmin):
    form = PubliciteForm  # Utilise notre formulaire personnalisé pour l'administration

    list_display = ('title', 'user', 'created', 'updated', 'featured', 'link')  # Colonnes affichées dans la liste
    list_filter = ('featured', 'created')  # Filtrer par "featured" et "created"
    search_fields = ('title', 'description', 'user__username', 'link')  # Recherche par titre, description, utilisateur et lien
    prepopulated_fields = {'slug': ('title',)}  # Génère automatiquement le slug à partir du titre
    ordering = ('-created',)  # Tri par date de création (descendant)

    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'slug', 'description', 'video_file', 'thumbnail', 'featured', 'link')
        }),
        ('Dates', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created', 'updated')  # Ces champs sont en lecture seule dans l'admin

    # Personnalisation de l'affichage du lien pour le fichier vidéo
    def video_file_link(self, obj):
        return f'<a href="{obj.video_file.url}" target="_blank">Voir la vidéo</a>'
    video_file_link.allow_tags = True
    video_file_link.short_description = 'Vidéo'

    # Ajouter la colonne 'video_file_link' à l'affichage dans l'admin
    list_display = ('title', 'user', 'video_file_link', 'created', 'updated', 'featured', 'link')

# Enregistrer le modèle et son interface d'administration
admin.site.register(Publicite, PubliciteAdmin)


