from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.userAuth, name="userAuth"),  # Added a new URL pattern for /poop/
    path("analyze_flavor_view/", views.analyze_flavor_view, name="analyze_flavor_view"),
]
