from django.contrib import admin
from .models import Category, User, Listing, Watchlist, Comment, Bid, Notifications
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Notifications)
