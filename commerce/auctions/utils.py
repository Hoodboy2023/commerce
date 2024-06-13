from .models import Auction_listing


def get_categories():
    return Auction_listing.objects.values('category').distinct()