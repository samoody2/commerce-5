from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("new_listing", views.new_listing, name="new_listing")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #this allows the media files saved to the listings to be displayed