from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
import authentication.views
import litreview.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", litreview.views.feed, name="feed"),
    path('login/', LoginView.as_view(
        template_name="authentication/login.html",
        redirect_authenticated_user=True
    ), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path("signin/", authentication.views.signin, name="signin"),
    path("subscriptions/", litreview.views.subscriptions, name="subscriptions"),
    path("feed/", litreview.views.feed, name="feed"),
    path("posts/", litreview.views.posts, name="posts"),
    path("ticket/add", litreview.views.add_ticket, name="add_ticket"),
    path("ticket/<int:id>/change", litreview.views.change_ticket, name="change_ticket"),
    path("ticket/<int:id>/delete", litreview.views.delete_ticket, name="delete_ticket"),
    path("review/add", litreview.views.add_review, name="add_review"),
    path("review/<int:id>/change", litreview.views.change_review, name="change_review"),
    path("review/<int:id>/delete", litreview.views.delete_review, name="delete_review"),
    path("review/<int:id>/add", litreview.views.add_response_review, name="add_response_review"),
    path(
        "review/<int:id>/get",
        litreview.views.subscribe_to_see_review,
        name="subscribe_to_see_review"),
]
