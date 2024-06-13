from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Auction_listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="items")
    title = models.CharField(max_length=64, null=False)
    description =  models.CharField(max_length=120,null=False)
    current_price = models.IntegerField(null=False)
    photo = models.CharField(max_length=250, blank=True)
    category =  models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=10, null=False, default="Open")
    date_created = models.DateField(auto_now_add=True)

   
class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="auction_bids")
    bid =  models.IntegerField()   

class Comments(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    listing =  models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="auction_comments")
    comment =  models.CharField(max_length=200)

    def __str__(self):
        return f"<{self.comment}>"

class Watchlist(models.Model):
    listing = models.ForeignKey(Auction_listing,on_delete=models.CASCADE, related_name="watchlists")
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user_watchlists")