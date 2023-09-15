from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain
import os

from authentication.models import User, UserFollows
from litreview.models import Ticket, Review
from . import forms


@login_required
def feed(request):
    """
    Description: vue pour la page accueil avec critiques et les demandes de critiques.
    Paramètre(s):
    - request: le paramètre par défaut indispensable
    """
    tickets_qset = Ticket.objects.filter(Q(user__in=request.user.abonnements.all()) | Q(user=request.user))
    reviews_qset_temp = Review.objects.filter(Q(user__in=request.user.abonnements.all()) | Q(user=request.user))
    reviews_qset = []
    for review in reviews_qset_temp:
        if review.ticket.user in request.user.abonnements.all() or review.ticket.user == request.user:
            reviews_qset.append(review)

    tickets_and_reviews = sorted(
        chain(tickets_qset, reviews_qset), key=lambda instance: instance.time_created, reverse=True
    )
    paginator = Paginator(tickets_and_reviews, settings.MAX_ITEMS_PER_PAGE)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    return render(request, "litreview/feed.html", context={"page_obj": page_obj})


@login_required
def posts(request):
    """
    Description: vue pour les seules publications de l'utilisateur connecté.
    Paramètre(s):
    - request: le paramètre par défaut indispensable
    """
    tickets = Ticket.objects.filter(Q(user=request.user))
    reviews = Review.objects.filter(Q(user=request.user))
    posts = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created, reverse=True)
    paginator = Paginator(posts, settings.MAX_ITEMS_PER_PAGE)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    return render(request, "litreview/posts.html", context={"page_obj": page_obj})


@login_required
def add_ticket(request):
    """
    Description: vue pour la page d'ajout d'une demande de critique.
    Paramètre(s):
    - request: le paramètre par défaut indispensable
    """
    ticket_creation_form = forms.TicketCreationForm()
    if request.method == "POST":
        ticket_creation_form = forms.TicketCreationForm(request.POST, request.FILES)
        if ticket_creation_form.is_valid():
            ticket_form = ticket_creation_form.save(commit=False)
            ticket_form.user = request.user
            ticket_form.save()
            messages.success(request, message="Ticket publié")
            return redirect("feed")
        else:
            messages.error(request, message="Vérifier votre saisie et que le fichier téléversé est une image")
    return render(request, "litreview/add_ticket.html", context={"ticket_creation_form": ticket_creation_form})


@login_required
def change_ticket(request, id):
    """
    Description: vue pour la page de modification d'une demande de critique.
    Paramètre(s):
    - request: le paramètre par défaut indispensable
    - id: un entier qui représente l'id de la demande de critique
    """
    ticket = Ticket.objects.get(id=id)
    ticket_creation_form = forms.TicketCreationForm(instance=ticket)
    ticket_image_delete_form = forms.TicketImageDeleteForm()
    if request.user.id == ticket.user.id:
        if request.method == "POST":
            original_ticket_image = ticket.image
            if "edit_form" in request.POST:
                ticket_creation_form = forms.TicketCreationForm(request.POST, request.FILES, instance=ticket)
                if ticket_creation_form.is_valid():
                    if "image" in request.FILES:
                        if request.FILES["image"] != original_ticket_image:
                            try:
                                os.remove(f"mediafiles/{original_ticket_image.name}")
                            except Exception as error:
                                messages.error(request,message=f"Erreur suppression {original_ticket_image.name}: {error}")
                    ticket.save()
                    messages.success(request, message=f"Ticket mis à jour")
                    return redirect("feed")
            if "delete_form" in request.POST:
                ticket.image.delete()
                messages.success(request, message="Image ticket supprimée")
    else:
        messages.error(request, message="Vous n'êtes pas l'auteur du ticket")
        return redirect("feed")
    context = {"ticket_creation_form": ticket_creation_form, "ticket_image_delete_form": ticket_image_delete_form}
    return render(request, "litreview/change_ticket.html", context={"ticket": ticket, "context": context})


@login_required
def delete_ticket(request, id):
    """
    Description: vue pour la page de suppression d'une demande de critique.
    Paramètre(s):
    - request: le paramètre par défaut indispensable
    - id: un entier qui représente l'id de la demande de critique
    """
    ticket = Ticket.objects.get(id=id)
    if request.user.id == ticket.user.id:
        if request.method == "POST":
            if ticket.user == request.user:
                ticket.image.delete()
                try:
                    os.remove(f"mediafiles/{ticket.image.name}")
                except:
                    pass
                ticket.delete()
                messages.success(request, message="Ticket supprimé")
                return redirect("feed")
    else:
        messages.error(request, message="Vous n'êtes pas l'auteur du ticket")
        return redirect("feed")
    return render(request, "litreview/delete_ticket.html", context={"ticket": ticket})


@login_required
def change_review(request, id):
    """
    Description: vue pour la page de modification d'une critique.
    Paramètre(s):
    - request: le paramètre par défaut indispensable
    - id: un entier qui représente l'id de la critique
    """
    review = Review.objects.get(id=id)
    review_creation_form = forms.ReviewCreationForm(instance=review)
    if request.user.id == review.user.id:
        if request.method == "POST":
            review_creation_form = forms.ReviewCreationForm(request.POST, request.FILES, instance=review)
            if review.user == request.user:
                if review_creation_form.is_valid():
                    review.save()
                    messages.success(request, message="Critique mise à jour")
                    return redirect("feed")
    else:
        messages.error(request, message="Vous n'êtes pas l'auteur de la critique")
        return redirect("feed")
    return render(request, "litreview/change_review.html", context={"review": review})


@login_required
def delete_review(request, id):
    """
    Description: vue pour la page de suppression d'une critique.
    Paramètre(s):
    - request: le paramètre par défaut indispensable
    - id: un entier qui représente l'id de la critique
    """
    review = Review.objects.get(id=id)
    ticket = Ticket.objects.get(id=review.ticket.id)
    if request.user.id == review.user.id:
        if request.method == "POST":
            if review.user == request.user:
                review.delete()
                ticket.has_been_reviewed = False
                ticket.save()
                messages.success(request, message="Critique supprimée")
                return redirect("feed")
    else:
        messages.error(request, message="Vous n'êtes pas l'auteur de la critique")
        return redirect("feed")
    return render(request, "litreview/delete_review.html", context={"review": review})


@login_required
def add_review(request):
    """
    Description: vue pour l'ajout à la fois d'une demande de critique et la critique elle même.
    Paramètre(s):
    - request: le paramètre par défaut indispensable
    """
    ticket_creation_form = forms.TicketCreationForm()
    review_creation_form = forms.ReviewCreationForm()
    context = {"ticket_creation_form": ticket_creation_form, "review_creation_form": review_creation_form}
    if request.method == "POST":
        ticket_creation_form = forms.TicketCreationForm(request.POST, request.FILES)
        review_creation_form = forms.ReviewCreationForm(request.POST)
        if all([ticket_creation_form.is_valid(), review_creation_form.is_valid()]):
            if review_creation_form.cleaned_data:
                rating_digit_value = review_creation_form['rating'].data
                ticket_form = ticket_creation_form.save(commit=False)
                ticket_form.user = request.user
                ticket_form.has_been_reviewed = True
                ticket_form.save()
                review_form = review_creation_form.save(commit=False)
                review_form.ticket = ticket_form
                review_form.rating = rating_digit_value
                review_form.user = request.user
                review_form.save()
                messages.success(request, message="Requête et critique ajoutées")
                return redirect("feed")
        else:
            messages.error(request, message="Vérifier votre saisie et que le fichier téléversé est une image")
    return render(request, "litreview/add_review.html", context=context)


@login_required
def add_response_review(request, id):
    """
    Description: vue pour l'ajout d'une critique à une demande.
    Paramètre(s):
    - request: le paramètre par défaut indispensable
    - id: un entier qui représente l'id de la demande de critique
    """
    ticket = get_object_or_404(Ticket, id=id)
    ticket_creation_form = forms.TicketCreationForm(instance=ticket)
    review_creation_form = forms.ReviewCreationForm()
    if ticket is not None:
        if request.method == "POST":
            review_creation_form = forms.ReviewCreationForm(request.POST)
            ticket_creation_form = forms.TicketCreationForm(instance=ticket)
            if review_creation_form.is_valid():
                if review_creation_form.cleaned_data:
                    rating_digit_value = review_creation_form['rating'].data
                    ticket_form = ticket_creation_form.save(commit=False)
                    ticket_form.has_been_reviewed = True
                    ticket_form.save()
                    review_form = review_creation_form.save(commit=False)
                    review_form.ticket = ticket
                    review_form.rating = rating_digit_value
                    review_form.user = request.user
                    review_form.save()
                    messages.success(request, message="Critique publiée en réponse au ticket")
                    return redirect("feed")
    context = {"review_creation_form": review_creation_form, "ticket": ticket}
    return render(request, "litreview/add_response_review.html", context=context)


@login_required
def subscribe_to_see_review(request, id):
    """
    Description: vue pour permettre de voir une critique si elle est formulée par un
    utilisateur non suivi.
    Paramètre(s):
    - request: le paramètre par défaut indispensable
    - id: un entier qui représente l'id de la demande de critique
    """
    ticket = get_object_or_404(Ticket, id=id)
    review = Review.objects.get(ticket=ticket)
    review_author = review.user
    form = forms.UserFollowForm()
    username_searched = review_author.username
    if request.user.username == username_searched:
        followed_user = True
    else:
        followed_user = UserFollows.objects.filter(user=request.user.id, followed_user=review_author)

    if request.method == "POST":
        form = forms.UserFollowForm(request.POST)
        followed_user = User.objects.get(username=username_searched.lower())
        user_follow = UserFollows(user=request.user, followed_user=followed_user)
        try:
            user_follow.save()
            request.user.save()
            User.objects.get(username=username_searched.lower()).save()
            messages.success(request, message="Abonnement pris en compte")
        except ObjectDoesNotExist:
            messages.warning(request, message="Vous êtes déjà abonné")

        return redirect("feed")

    context = {"review": review, "ticket": ticket, "form": form, "followed_user": followed_user}
    return render(request, "litreview/view_review_detail.html", context=context)


@login_required
def subscriptions(request):
    """
    Description: vue pour la page abonnements.
    Paramètre(s):
    - request: le paramètre par défaut indispensable
    """
    follow_form = forms.UserFollowForm()
    unsubscribe_form = forms.UnsubscribeForm()
    if request.method == "POST":
        if "follow_user" in request.POST:
            form = forms.UserFollowForm(request.POST)
            if form.is_valid() and form.cleaned_data:
                if request.POST["username"] != "":
                    username_searched = request.POST["username"]
                    try:
                        followed_user = User.objects.get(username=username_searched.lower())
                    except ObjectDoesNotExist:
                        messages.error(request, message="Utilisateur non trouvé")
                        return redirect("feed")

                    user_follow = UserFollows(user=request.user, followed_user=followed_user)
                    if followed_user.username == request.user.username:
                        messages.warning(request, message="Inutile de vous abonner à vous même")
                        return redirect("feed")

                    if followed_user.username == "admin":
                        messages.warning(request, message="Pas d'abonnement possible au compte admin")
                        return redirect("feed")

                    try:
                        user_follow.save()
                        request.user.save()
                        User.objects.get(username=username_searched.lower()).save()
                        messages.success(request, message="Abonnement pris en compte")
                    except Exception:
                        messages.warning(request, message="Vous êtes déjà abonné")
                    return redirect("feed")
        elif "unsubscribe_user" in request.POST:
            form = forms.UnsubscribeForm(request.POST)
            if form.is_valid():
                if request.POST["username"] != "":
                    username_searched = request.POST["username"].lower()
                    try:
                        followed_user = User.objects.get(username=username_searched)
                        user_follow = UserFollows.objects.get(user=request.user, followed_user=followed_user)
                        user_follow.delete()
                        messages.success(request, message="Désabonnement pris en compte")
                        return redirect("feed")
                    except ObjectDoesNotExist:
                        messages.error(request, message="Utilisateur non trouvé")
    user_subscriptions = request.user.following.all().exclude(followed_user=request.user)
    user_followers = request.user.followed_by.all().exclude(user=request.user)
    context = {
        "follow_form": follow_form,
        "unsubscribe_form": unsubscribe_form,
        "subscriptions": user_subscriptions,
        "followers": user_followers}
    return render(request, "litreview/subscriptions.html", context=context)
