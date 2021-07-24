from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone


# given to us
class User(AbstractUser):
    pass


# class to track category names
class Category(models.Model):
    category = models.CharField(max_length=25)

    def __str__(self):
        return self.category


# class for our listings, the "heart" of the website.
# using many to one relationships so that sellers can have multiple listings
# and there can be multiple watchers
class Listing(models.Model):
    # foreign key so that a seller can have multiple listings
    seller = ForeignKey(
        User,
        related_name='seller_listings',
        on_delete=models.CASCADE
        )
    # will indicate the winning bidder
    buyer = ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=True)
    # category can have multiple listings
    category = ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category_listings'
        )
    starting_bid = models.FloatField(default='')
    current_bid = models.FloatField(default='0.0')
    # settings.py has a MEDIA_URL path
    # that will allow images to be stored there
    image = models.ImageField(upload_to='')
    # boolean used to make sure only active listings are displayed
    active = models.BooleanField(default=True)
    start_date = models.DateField(default=timezone.now)
    # many to many field
    # so multiple items can be added by multiple people
    # to their watchlists
    on_watchlist = models.ManyToManyField(
        User,
        blank=True,
        related_name='watchlist_items'
        )

    # returning the title, category and seller
    def __str__(self):
        return '{} sold by {}'.format(self.title, self.seller)


# model will handle the bids with foreignkeys
# to allow multiple listings and users to pass through
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.FloatField(default='')
    bid_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} has bid {} on {}'.format(
            self.bidder,
            self.bid_amount,
            self.listing
            )


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_comment = models.TextField(max_length=250)
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="all_comments")
    comment_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'On {self.comment_time} {self.user} said "{self.user_comment}"'

class Watchlist(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   watchlist_item = models.ManyToManyField(Listing)
   def __str__(self):
       return f"{self.user}'s WatchList"