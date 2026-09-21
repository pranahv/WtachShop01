from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("profile",views.profile,name="profile"),
    path("ediprofile",views.edit_profile,name="editprofile"),
    path("login/", views.user_login, name="login"),
    path("registration/", views.registration, name="registration"),

    path("product/", views.product, name="product"),

    path("product_details/<int:id>/", views.product_details, name="product_details"),

    path("add_to_cart/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"), 
    path("remove_cart/<int:id>/", views.remove_cart, name="remove_cart"),

    path("wishlist/", views.wishlist, name="wishlist"),
    path("add_to_wishlist/<int:id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("remove_wishlist/<int:id>/", views.remove_wishlist, name="remove_wishlist"),

    path("buy_cart/", views.buy_cart, name="buy_cart"),
    path("payment/", views.payment, name="payment"),
    path('success/', views.payment_success, name='success'),
    
    path("logout/", views.logout_view, name="logout_view"),
]