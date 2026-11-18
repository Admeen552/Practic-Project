from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def reg(request):
    return render(request, 'reg.html')

def aut(request):
    return render(request, 'aut.html')

def cart(request):
    return render(request, 'cart.html')

def wishList(request):
    return render(request, 'wishList.html')

def catalog(request):
    return render(request, 'catalog.html')

def checkOut(request):
    return render(request, 'checkOut.html')

def profile(request):
    return render(request, 'profile.html')

def product(request):
    return render(request, 'product.html')
