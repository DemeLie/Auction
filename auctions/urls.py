from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("listing/<int:pk>/", views.listing_detail, name='listing_detail'),
    path('category/<int:category_id>/', views.category_items, name='category_items'),
    path('place_bid/<int:listing_id>/', views.place_bid, name='place_bid'),
    path('create_listing', views.create_listing, name='create_listing'),
    path('add_comment/<int:listing_id>', views.add_comment, name='add_comment'),
    path('add_to_watchlist/<int:listing_id>', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('notifications/', views.notifications, name='notifications'),
    path('close_listing/<int:listing_id>', views.close_listing, name='close_listing'),
    path('delete_listing/<int:listing_id>', views.delete_listing, name='delete_listing')
]
