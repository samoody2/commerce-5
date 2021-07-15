from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from auctions.models import Listing, Category, User, Bid, Comment
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    pass
admin.site.register(Listing, ListingAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)

class BidAdmin(admin.ModelAdmin):
    pass
admin.site.register(Bid, BidAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comment, CommentAdmin)
