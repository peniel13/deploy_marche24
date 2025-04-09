from django import forms
from .models import  WebsiteLink

class WebsiteLinkForm(forms.ModelForm):
    class Meta:
        model = WebsiteLink
        fields = ['profile_picture', 'name', 'website_link', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Rendre la zone de texte plus grande
        }

    # Optionnel: Vous pouvez ajouter des validations ou des personnalisations ici
    def clean_website_link(self):
        website_link = self.cleaned_data.get('website_link')
        if website_link and not website_link.startswith('http'):
            raise forms.ValidationError('Le lien doit commencer par "http://" ou "https://"')
        return website_link

from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['user', 'title', 'description', 'video_file', 'thumbnail', 'featured']

    # Tu peux ajouter des validations personnalisées ici si nécessaire
    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')
        if video_file:
            if video_file.size > 100 * 1024 * 1024:  # Limite de taille à 100MB
                raise forms.ValidationError("La taille de la vidéo ne doit pas dépasser 100 MB.")
        return video_file

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get('thumbnail')
        if thumbnail:
            if thumbnail.size > 5 * 1024 * 1024:  # Limite de taille de l'image miniature à 5MB
                raise forms.ValidationError("La taille de l'image miniature ne doit pas dépasser 5 MB.")
        return thumbnail

from django import forms
from .models import Publicite

class PubliciteForm(forms.ModelForm):
    class Meta:
        model = Publicite
        fields = ['user', 'title', 'description', 'video_file', 'thumbnail', 'featured', 'link']

    # Validation de la taille du fichier vidéo
    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')
        if video_file:
            if video_file.size > 100 * 1024 * 1024:  # Limite de taille à 100MB
                raise forms.ValidationError("La taille de la vidéo ne doit pas dépasser 100 MB.")
        return video_file

    # Validation de la taille de l'image miniature
    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get('thumbnail')
        if thumbnail:
            if thumbnail.size > 5 * 1024 * 1024:  # Limite de taille à 5MB
                raise forms.ValidationError("La taille de l'image miniature ne doit pas dépasser 5 MB.")
        return thumbnail

    # Validation du champ link pour s'assurer qu'il est bien une URL valide
    def clean_link(self):
        link = self.cleaned_data.get('link')
        if link:
            if not link.startswith('http://') and not link.startswith('https://'):
                raise forms.ValidationError("Le lien doit commencer par 'http://' ou 'https://'.")
        return link
