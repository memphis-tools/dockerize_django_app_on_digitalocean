from django.shortcuts import render, redirect
from django.contrib import messages
from authentication.models import User, UserFollows
from . import forms


def signin(request):
    """
    Description: vue pour la page inscription
    Paramètre(s):
    - request: le paramètre par défaut indispensable
    """
    form = forms.LitreviewUserCreationForm()
    if request.method == "POST":
        form = forms.LitreviewUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            followed_user = User.objects.get(username=form.cleaned_data["username"].lower())
            user_follow = UserFollows(user=followed_user, followed_user=followed_user)
            user_follow.save()
            messages.success(request, message=f"Bienvenue {user.username}, merci de vous connecter")
            return redirect("feed")
        else:
            messages.error(request, message="Erreur de saisie")
    return render(request, "authentication/signin.html", context={"form": form})
