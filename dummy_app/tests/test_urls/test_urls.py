import pytest

from django.urls import resolve, reverse
from authentication.models import User


# authentication views
def test_signin_url():
    """ Check if path leads to expected view. """
    path = reverse("signin")
    assert path == "/signin/"
    assert resolve(path).view_name == "signin"


def test_login_url():
    """ Check if path leads to expected view. """
    path = reverse("login")
    assert path == "/login/"
    assert resolve(path).view_name == "login"


# litreview views
def test_subscriptions_url():
    """ Check if path leads to expected view. """
    path = reverse("subscriptions")
    assert path == "/subscriptions/"
    assert resolve(path).view_name == "subscriptions"


def test_add_ticket_url():
    """ Check if path leads to expected view. """
    path = reverse("add_ticket")
    assert path == "/ticket/add"
    assert resolve(path).view_name == "add_ticket"
