from django import forms
from django.conf import settings
from litreview import models


class UserFollowForm(forms.Form):
    """
    Description: formulaire dédié à l'abonnement.
    Paramètre(s):
    - forms: par défaut, on instancie une classe sans modèle de référence
    """
    follow_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    username = settings.AUTH_USER_MODEL


class UnsubscribeForm(forms.Form):
    """
    Description: formulaire dédié au désabonnement.
    Paramètre(s):
    - forms: par défaut, on instancie une classe sans modèle de référence
    """
    unsubscribe_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    username = settings.AUTH_USER_MODEL


class TicketCreationForm(forms.ModelForm):
    """
    Description: formulaire dédié à la création d'une demande de critique.
    Paramètre(s):
    - forms: par défaut, on instancie sur la base d'un modèle de référence
    """
    edit_form = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


class TicketImageDeleteForm(forms.Form):
    """
    Description: formulaire dédié à la suppression d'une image liée à une demande de critique.
    Paramètre(s):
    - forms: par défaut, on instancie un Form
    """
    delete_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewCreationForm(forms.ModelForm):
    """
    Description: formulaire dédié à la création d'une demande de critique.
    Paramètre(s):
    - forms: par défaut, on instancie sur la base d'un modèle de référence
    """
    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]
