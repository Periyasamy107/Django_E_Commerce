import json
from django.shortcuts import render, redirect
from . models import Category, Product, Cart, Favourite
from django.contrib import messages
from . forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

def home(request):
    products = Product.objects.filter(trending=1)
    return render(request, 'shop/index.html', {'products':products})


def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Successful you can login now!!')
            return redirect('login')
        else:
            return render(request, 'shop/register.html', {'form':form})
    else:
        return render(request, 'shop/register.html', {'form':form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successful..!!')
                return redirect('home')
            else:
                messages.error(request, "Invalid User Name or Password")
                return redirect('login')
        return render(request, 'shop/login.html', {})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logged out Successful.')
    return redirect('home')

def collections(request):
    category = Category.objects.filter(status=0)
    return render(request, 'shop/collections.html', {'category':category})


def collections_view(request, name):
    if (Category.objects.filter(name=name, status=0)):
        products = Product.objects.filter(category__name=name)
        return render(request, 'shop/products/products.html', {'products':products, 'category_name':name})
    else:
        messages.warning('No such Category found.')
        return redirect('collections')
    

def product_details(request, cname, pname):
    if Category.objects.filter(name=cname, status=0):
        if Product.objects.filter(name=pname, status=0):
            products = Product.objects.filter(name=pname, status=0).first()
            return render(request, 'shop/products/product_details.html', {'products':products})
            
        else:
            products = Product.objects.filter(name=pname, status=1).all()
            messages.warning(request, 'No Product Details found...')
            return redirect('collections')
    else:
        messages.error(request, 'No such Category found.')
        return redirect('collections')


def add_to_cart(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data['product_qty']
            product_id = data['pid']
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id, product_id = product_id):
                    return JsonResponse({'status':'Product already in Cart'}, status=200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user=request.user, product_id = product_id, product_qty = product_qty)
                        return JsonResponse({'status':'Product Added to Cart'}, status = 200)
                    else:
                        return JsonResponse({'status':'Stock not available'}, status = 200)
            else:
                return JsonResponse({'status':'Product not found'}, status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)
    


def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'shop/cart.html', {'cart':cart})
    else:
        return redirect('home')
    

def remove_cart(request, cid):
    cart_item = Cart.objects.get(id=cid)
    cart_item.delete()
    return redirect('/cart')


def favourites_page(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_id = data['pid']
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id, product_id = product_id):
                    return JsonResponse({'status':'Product already in Favourite'}, status=200)
                else:
                    Favourite.objects.create(user=request.user, product_id = product_id)
                    return JsonResponse({'status':'Product Added to Favourites'}, status=200)
            else:
                return JsonResponse({'status': 'Product not found'}, status=200)
        else:
            return JsonResponse({'status':'Login to Add Favourites'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)
    

def fav_view(request):
    if request.user.is_authenticated:
        favourite = Favourite.objects.filter(user=request.user)
        return render(request, 'shop/favourite.html', {'favourite':favourite})
    else:
        return redirect('home')


def remove_favourite(request, fid):
    fav_item = Favourite.objects.get(id=fid)
    fav_item.delete()
    return redirect('fav_view')