from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import Farmer, Product
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import auth
from django.contrib import messages


@login_required
def add_product(request):
    if request.method == 'POST':
        product = Product()
        product.farmer = request.user.farmer
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.image = request.FILES.get('image')
        product.save()
        return redirect('product_list')
    return render(request, 'market/add_product.html')


def product_list(request):
    user_location = None
    if request.user.is_authenticated:
        user_location = request.user.farmer.location
        #user_point = Point(request.user.farmer.latitude, request.user.farmer.longitude)
        #   products = Product.objects.annotate(distance=Distance('farmer__location_point', user_point)).order_by('distance')
        products = Product.objects.all()
    else:
        products = Product.objects.all()
    return render(request, 'market/product_list.html', {'products': products, 'user_location': user_location})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'market/product_detail.html', {'product': product})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.farmer != product.farmer:
        return redirect('product_list')
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'market/delete_product.html', {'product': product})


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.farmer != product.farmer:
        return redirect('product_list')
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.save()
        return redirect('product_detail', pk=pk)
    return render(request, 'market/edit_product.html', {'product': product})


@login_required
def edit_farmer(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    if request.user.farmer != farmer:
        return redirect('product_list')
    if request.method == 'POST':
        farmer.location = request.POST.get('location')
        farmer.save()
        return redirect('farmer_detail', pk=pk)
    return render(request, 'market/edit_farmer.html', {'farmer': farmer})


def farmer_detail(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    return render(request, 'market/farmer_detail.html', {'farmer': farmer})


@login_required
def delete_farmer(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    if request.user.farmer != farmer:
        return redirect('product_list')
    if request.method == 'POST':
        farmer.delete()
        return redirect('product_list')
    return render(request, 'market/delete_farmer.html', {'farmer': farmer})


@login_required
def search_farmer(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        farmers = Farmer.objects.filter(location__icontains=query)
        return render(request, 'market/search_farmer.html', {'farmers': farmers, 'query': query})
    return redirect('product_list')


def nearest_farmers(request):
    user_point = Point(request.user.farmer.latitude, request.user.farmer.longitude)
    farmers = Farmer.objects.annotate(distance=Distance('location_point', user_point)).order_by('distance')
    return render(request, 'market/nearest_farmers.html', {'farmers': farmers})


@login_required
def create_farmer(request):
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            farmer = form.save(commit=False)
            farmer.user = request.user
            farmer.save()
            return redirect('product_list')
    else:
        form = FarmerForm()
    return render(request, 'market/create_farmer.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request)
            return redirect('index')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'signup.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')