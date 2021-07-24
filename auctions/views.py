from auctions.forms import CategoryForm, ListingForm, BidForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Listing, Category, Comment, Watchlist

# displays all active listings
def index(request):
    listings = Listing.objects.filter(active=True)
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

# our listing page view
def listing(request, listing_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    listing = Listing.objects.get(id=listing_id)        
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid_form": BidForm(),
        "comments": listing.all_comments.all(),
        "comment_form": CommentForm()        
    })


# comment view handling user postings
@login_required
def comment(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    form = CommentForm(request.POST)
    new_comment = form.save(commit=False)
    new_comment.user = request.user
    new_comment.listing = listing
    new_comment.save()
    return HttpResponseRedirect(reverse("listing", kwargs=[listing_id]))


# gets all items on users watchlist
@login_required
def watchlist(request, listing_id):
    item_to_save = get_object_or_404(Listing, pk=listing_id)
    # Check if it's in the watchlist
    if Watchlist.objects.filter(user=request.user, watchlist_item=listing_id).exists():
        messages.add_message(request, messages.ERROR, "You already have it in your watchlist.")
        return HttpResponseRedirect(reverse("auctions:index"))
    # Gets list or creates
    user_list, created = Watchlist.objects.get_or_create(user=request.user)
    # Add watchlist item
    user_list.item.add(item_to_save)
    messages.add_message(request, messages.SUCCESS, "Successfully added to your watchlist")
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
    else:
        form = CategoryForm()
    return render(request, "auctions/categories.html", {
            "form": form,
            "categories": categories
    })


# shows individual category page
@login_required
def category(request, category_id):
    category_items = Listing.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "category": category,
        "categoryListings": category_id
    })

#makes new auction listing
@login_required
def new_listing(request):
    if request.method == "POST":
        newListing = ListingForm(request.POST)
        if newListing.is_valid():
            newListing.seller = request.seller
            newListing.save(commit=False)
        return HttpResponseRedirect(reverse("index"))
    else:
            form = ListingForm()
    return render(request, "auctions/new_listing.html", {
         "form": form
        })

def new_bid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    bid = float(request.POST['bid'])