from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Max
from .models import User, Category, Bid, Notifications, Listing, Comment, Watchlist


def index(request):
    listing = Listing.objects.all()
    return render(request, "index.html", {"listings": listing})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


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
            return render(request, "register.html", {
                "message": "Passwords must match."
            })


        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
def categories(request):
    categories = Category.objects.all()
    return render(request, "category.html", {"categories": categories})


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    comments = Comment.objects.filter(listing=listing)
    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(listing=pk, user=request.user).exists()
        return render(request, 'listing_detail.html', {"listing": listing,
                                                    "comments": comments,
                                                    "in_watchlist": in_watchlist})
    else:
        return render(request, 'listing_detail.html', {"listing": listing,
                                                       "comments": comments})

def category_items(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(category=category)
    return render(request, 'category_items.html', {'category': category, 'items': listings})

def place_bid(request, listing_id):
    if request.method == 'POST':
        bid_amount = request.POST.get('bid')
        user = request.user
        listing = get_object_or_404(Listing, pk=listing_id)

        try:
            bid_amount = float(bid_amount)
        except ValueError:
            messages.error(request, 'Please enter a valid bid amount.')
            return redirect('listing_detail', pk=listing_id)

        current_max_bid = Bid.objects.filter(listing=listing).aggregate(Max('bids'))['bids__max']

        if current_max_bid and bid_amount <= current_max_bid:
            messages.error(request, 'Your bid must be higher than the current highest bid.')
        else:
            bid = Bid.objects.create(user=user, listing=listing, bids=bid_amount)
            bid.save()
            listing.current_bid = bid_amount
            listing.save()
            messages.success(request, 'Your bid has been placed successfully.')

        return redirect('listing_detail', pk=listing_id)
    else:
        return redirect('index')
def create_listing(request):
    categories = Category.objects.all()
    if request.user.is_authenticated and request.method == 'POST':
        name = request.POST.get('name')
        bid = request.POST.get('bid')
        description = request.POST.get('description')
        category = get_object_or_404(Category, pk=request.POST.get('category'))
        image = request.FILES.get('image')
        user_id = request.user
        try:
            bid = float(bid)
        except ValueError:
            messages.error(request, 'Please enter a valid bid')
        listing = Listing.objects.create(
            name=name,
            description=description,
            category=category,
            images=image,
            usr=user_id,
            current_bid=bid,
        )
        new_bid = Bid.objects.create(user=user_id, listing=listing, bids=bid)
        new_bid.save()
        return redirect('listing_detail', pk=listing.pk)
    elif not request.user.is_authenticated:
        messages.error(request, 'You are not logged in.')
        return render(request, 'create_listing.html', {'categories': categories})
    else:
        return render(request, 'create_listing.html', {'categories': categories})
def add_comment(request, listing_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        comment = Comment.objects.create(user=user, text=text, listing=listing)
        comment.save()
    return redirect('listing_detail', pk=listing_id)
def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    watchlist_item = Watchlist.objects.filter(user=user, listing=listing)
    if watchlist_item:
        watchlist_item.delete()
    else:
        watchlist = Watchlist.objects.create(user=user, listing=listing)
        watchlist.save()
    return redirect('listing_detail', pk=listing_id)


def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    return render(request, 'watchlist.html', {'watchlist': watchlist_items})

def notifications(request):
    notifications = Notifications.objects.filter(user=request.user)
    return render(request, 'notif.html', {'notifications': notifications})



def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    bids = Bid.objects.filter(listing=listing)
    sent_to_users = []
    watchlist_item = Watchlist.objects.filter(user=user, listing=listing)
    if watchlist_item:
        watchlist_item.delete()

    max_bid_instance = bids.order_by('-bids').first()
    if max_bid_instance:
        max_bid_user = max_bid_instance.user
    else:
        max_bid_user = None
    for bid in bids:
        if bid.user not in sent_to_users:
            if bid.user == max_bid_user:
                notification_text = f'Congratulations! You won the listing "{listing.name}".'
                sent_to_users.append(bid.user)
            else:
                sent_to_users.append(bid.user)
                notification_text = f'Sorry! You lost the listing "{listing.name}".'
            notification = Notifications.objects.create(user=bid.user, text=notification_text, listing=listing)
            notification.winner = max_bid_user
            notification.save()
    messages.success(request, 'The listing has been closed successfully.')

    listing.active = False
    listing.save()

    return redirect('listing_detail', pk=listing_id)
def delete_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.delete()
    return redirect('index')












