from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from .utils import get_categories
from django.contrib.auth.decorators import login_required
from .models import User, Auction_listing, Bids, Watchlist, Comments


def index(request):
    listings = Auction_listing.objects.all()
    print(categories)
    return render(request, "auctions/index.html", {
        "listings": listings, "categories": get_categories()
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.warning(request,"Invalid username and/or password.")
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.warning(request,"Passwords must match.")
            return render(request, "auctions/register.html")

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.warning(request,"Username already taken.")
            return render(request, "auctions/register.html", {
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        current_price = request.POST["current_price"]
        photo =  request.POST["photo"]
        category =  request.POST["category"]

        try:
            price = int(current_price)
            new_listing = Auction_listing(
                title=title, description=description, current_price=price,
                photo=photo, category=category, user=request.user)
            new_listing.save()
            messages.success(request, "Auction Activated")
            return HttpResponseRedirect(reverse("index"))
        except(ValueError):
            messages.warning(request, "Invalid Price")
            return HttpResponseRedirect(reverse("create_listing"))
    else:
        return render(request, "auctions/new.html",{"categories": get_categories()})


def listing(request, listing_id):
    listing = Auction_listing.objects.get(pk=int(listing_id))
    highest_bid = Bids.objects.aggregate(max_bid_price=Max('bid'))['max_bid_price']
    if request.method == "GET":
        comments = Comments.objects.filter(listing=listing)
        if request.user.is_authenticated:
            user_listing_bids = Bids.objects.filter(user=request.user, listing=listing)
            print(user_listing_bids)
        else:
            user_listing_bids=""
        return render(request, "auctions/listing.html", {
        "listing": listing, "highest_bid": highest_bid, "user_listing_bids": user_listing_bids, "comments": comments,
        "categories": get_categories()
        })
    else:
        bid_price = request.POST["bid"]
        try:
            if highest_bid:
                if int(bid_price) > highest_bid:
                    bid = Bids(listing=listing, bid=bid_price, user=request.user)
                    bid.save()
                    messages.success(request, "Bid successfully placed")
                else:
                    messages.warning(request, "Bid should be higher than Highest Bid!") 
            else: 
                if int(bid_price) > listing.current_price:
                    bid = Bids(listing=listing, bid=int(bid_price),user=request.user)
                    bid.save()
                    messages.success(request, "Bid successfully placed")
                else:
                    messages.warning(request, "Bid should be higher than price!") 
        except(ValueError):
            messages.warning(request, "Incorrect Input of Bid")                      
        return HttpResponseRedirect(reverse('listing', kwargs={"listing_id":listing_id}))
@login_required   
def watchlist(request):
    if request.method == "POST":
        try:
            listing_id = request.POST["remove_listing"]
            listing = Auction_listing.objects.get(pk=listing_id)
            watchlist_item = Watchlist.objects.filter(listing=listing,user=request.user)
            print(watchlist_item)
            if watchlist_item:
                watchlist_item.delete()
                messages.success(request,"Successfully removed from watchlist")
                return HttpResponseRedirect(reverse("watchlist"))
            else:
                return HttpResponseRedirect(reverse("watchlist"))
        except(MultiValueDictKeyError):
            listing_id = request.POST["watchlist_addition"]
            listing = Auction_listing.objects.get(pk=listing_id)
            on_watchlist = Watchlist.objects.filter(user=request.user, listing=listing)    
            if listing and not on_watchlist: 
                watchlist_addition = Watchlist(listing=listing, user=request.user)
                watchlist_addition.save()
                messages.success(request, "Successfully added to watchlist")
                return HttpResponseRedirect(reverse('listing', kwargs={"listing_id": listing_id}))
            messages.warning(request, "Already on watchlist")
            return HttpResponseRedirect(reverse('listing', kwargs={"listing_id":listing_id}))
    else:
        watchlists = Watchlist.objects.filter(user=request.user)
        print(watchlists)
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlists, "categories": get_categories()
        })
@login_required
def close_listing(request, listing_id):
    if request.method == "POST":
          listing = get_object_or_404(Auction_listing, pk=listing_id)
          listing.status = "Closed"
          listing.save()
          messages.success(request, "AUCTION CLOSED")
          return HttpResponseRedirect(reverse("listing", kwargs={"listing_id":listing_id}))
   
def comments(request):
   
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        comment = request.POST["comment"]
        listing = get_object_or_404(Auction_listing, pk=listing_id)
       
        comment_to_add = Comments(listing=listing, comment=comment, user=request.user)
        comment_to_add.save()

        messages.success(request, "Comment Added")
        return HttpResponseRedirect(reverse("listing", kwargs={"listing_id":listing_id}))
    
def categories(request,category):
    if request.method == "GET":
        listings = Auction_listing.objects.filter(category=category)
        return render(request, "auctions/category.html", {"category":category, "listings":listings, "categories": get_categories()})

