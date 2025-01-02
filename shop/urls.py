from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('cart/', views.cart_page, name='cart'),
    path('favourites/', views.favourites_page, name='favourites'),
    path('fav_view/', views.fav_view, name='fav_view'),
    path('remove_favourite/<str:fid>/', views.remove_favourite, name='remove_favourite'),
    path('remove_cart/<str:cid>/', views.remove_cart, name='remove_cart'),
    path('collections/', views.collections, name='collections'),
    path('collections/<str:name>/', views.collections_view, name='collections'),
    path('collections/<str:cname>/<str:pname>', views.product_details, name='product_details'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
]