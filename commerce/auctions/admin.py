from django.contrib import admin
from .models import Auction_listing,Comments,Watchlist
# Register your models here.
admin.site.register(Auction_listing)
admin.site.register(Comments)
admin.site.register(Watchlist)