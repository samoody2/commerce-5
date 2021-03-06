from django.forms import ModelForm
from auctions.models import Category, Comment, Listing, Bid


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["category"]


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "category", "starting_bid", "image"]


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_amount"]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["user_comment"]
