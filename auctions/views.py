from auctions.forms import ListingForm
from django.contrib.auth import authenticate, login, logout 
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Category


def index(request):
    listings= Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request):
    
    return render(request, "auctions/index.html")

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html")

@login_required
def categories(request):

    return render(request, "auctions/categories.html")

@login_required
def new_listing(request):
    if request.method == "POST":
        newListing= ListingForm(request.POST)
        if newListing.is_valid():
            newListing.save()
        return HttpResponseRedirect(reverse_lazy("index"))
    else:
            form = ListingForm()
    return render(request, "auctions/new_listing.html", {
         "form": form
        })