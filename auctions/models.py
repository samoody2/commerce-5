from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateField
from django.db.models.fields.related import ForeignKey

#given to us
class User(AbstractUser):
    pass

# class to track category names
class Category(models.Model):
    category = models.CharField(max_length=15)
    def __str__(self):
        return f"(self.category)"

# class for our listings, the "heart" of the website. using many to one relationships so that sellers can have multiple listings and there can be multiple watchers
class Listing(models.Model):
   #foreign key so that a seller can have multiple listings
    seller = ForeignKey(User, related_name='seller_listings', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=True)
    #category can have multiple listings
    category = ForeignKey(Category, on_delete=models.CASCADE, related_name='category_listings')
    starting_bid = models.FloatField(blank=True, null=True)
    current_bid = models.FloatField(blank=True, null=True)
    #settings.py has a MEDIA_URL path that will allow images to be stored there. similar to the STATIC_URL included
    image = models.ImageField(upload_to ='uploads/')
    #boolean used to make sure only active listings are displayed
    active = models.BooleanField(default= True)
    start_date= models.DateField(auto_now_add=True)
    #many to many field so multiple items can be added by multiple people to their watchlists
    on_watchlist= models.ManyToManyField(User, blank=True, related_name='watchlist_items')
    
    #returning the title, category and seller
    def __str__(self):
        return f"{self.title, self.category, self.seller}"

#model will handle the bid submission, using foreignkeys to allow multiple listings and users to pass through
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.FloatField



'''

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    user_comment = models.CharField(max_length=250)
'''
