from auctions.forms import CategoryForm, ListingForm, BidForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Category

# displays all active listings
def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listing": listings
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

# our listing page view
def listing(request, listing_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    listing = Listing.objects.get(id=listing_id)        
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid_form": BidForm(),
        "comment_form": CommentForm()        
    })

#gets all items on users watchlist
@login_required
def watchlist(request):
    listings = request.user.watchlist_items.all()
    categories = Category.objects.all()
    return render(request, "auctions/watchlist.html")

# displays and adds categories
@login_required
def categories(request):
    category = request.GET.get("category")
    categories = Category.objects.all()
    if request.method == "POST":
        categoryform = CategoryForm(request.POST)
        if categoryform.is_valid():
            categoryform.save()
            form= CategoryForm()
        return render(request, "auctions/categories.html", {
                        "form": form,
            "categories": categories
        })
        # HttpResponseRedirect(reverse("auction/categories", kwargs={'categories': categories}))
    else:
        form = CategoryForm()
    return render(request, "auctions/categories.html", {
            "form": form,
            "categories": categories
    })

#makes new auction listing
@login_required
def new_listing(request):
    if request.method == "POST":
        newListing = ListingForm(request.POST)
        if newListing.is_valid():
            newListing.seller = request.user
            newListing.save(commit=False)
        return HttpResponseRedirect(reverse("index"))
    else:
            form = ListingForm()
    return render(request, "auctions/new_listing.html", {
         "form": form
        })
