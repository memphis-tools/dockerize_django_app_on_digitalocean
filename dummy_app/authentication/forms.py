from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LitreviewUserCreationForm(UserCreationForm):
    """
    Description: formulaire dédié à la création d'un utilisateur.
    Paramètre(s):
    - UserCreationForm: formulaire générique pour la création d'un utilisateur
    """
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username"]
