from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.userAuth, name="userAuth"),  # Added a new URL pattern for /poop/
    path("analyze_flavor_view/", views.analyze_flavor_view, name="analyze_flavor_view"),
    path("upload", views.upload, name="upload"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)