from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.http import HttpResponse


# HOME PAGE
def index(request):
    return render(request, 'index.html')


# REGISTER
def registration(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if models.User.objects.filter(Email=email).exists():
            return HttpResponse("<script>alert('Email already exists'); window.location.href = '/registration/';</script>")
        models.User.objects.create(
            Name=request.POST.get('name'),
            Email=email,
            Phone=request.POST.get('phone'),
            Image=request.FILES.get('image'),
            DOB=request.POST.get('dob'),
            Pass=request.POST.get('pass')
        )

        return HttpResponse("<script>alert('Registration successfuliy...Please login');window.location.href = '/login/';</script>")  
    return render(request, 'registration.html')


# LOGIN
def user_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("pass")

        user = models.User.objects.filter(
            Email=email,
            Pass=password
        ).first()

        if user:

            request.session["email"] = user.Email

            return HttpResponse("<script>alert('Login successfully....');window.location.href = '/home/';</script>")

        else:

            return HttpResponse("<script>alert('Invalid email or password');window.location.href = '/login/';</script>")
    return render(request, "login.html")


# HOME
def home(request):

    if "email" not in request.session:
        return redirect("login")

    return render(request, 'home.html')


# PROFILE
def profile(request):

    if "email" not in request.session:
        return redirect("login")

    email = request.session.get("email")

    user = models.User.objects.filter(
        Email=email
    ).first()

    if not user:

        request.session.flush()
        return redirect("login")

    return render(request, "profile.html", {
        "user": user
    })


# EDIT PROFILE
def edit_profile(request):

    if "email" not in request.session:
        return redirect("login")

    email = request.session.get("email")

    user = models.User.objects.filter(
        Email=email
    ).first()

    if not user:

        request.session.flush()
        return redirect("login")

    if request.method == "POST":

        new_email = request.POST.get('email')

        # CHECK DUPLICATE EMAIL
        existing_user = models.User.objects.filter(
            Email=new_email
        ).exclude(id=user.id).first()

        if existing_user:

            return render(request, 'editprofile.html', {
                'user': user,
                'error': 'Email already exists'
            })

        user.Name = request.POST.get('name')
        user.Email = new_email
        user.Phone = request.POST.get('phone')
        user.DOB = request.POST.get('dob')
        user.Pass = request.POST.get('pass')

        if request.FILES.get('image'):
            user.Image = request.FILES.get('image')

        user.save()

        # UPDATE SESSION EMAIL
        request.session["email"] = user.Email

        return HttpResponse("<script>alert('Profile updated successfully');window.location.href = '/profile';</script>")

    return render(request, 'editprofile.html', {
        'user': user
    })


# LOGOUT
def logout_view(request):

    request.session.flush()

    return HttpResponse("<script>alert('Logout successfully....');window.location.href = '/login/';</script>")


# PRODUCT LIST
def product(request):
    products = models.Watch.objects.all()
    return render(request, 'product.html', {'product': products})


# PRODUCT DETAILS
def product_details(request, id):
    product = get_object_or_404(models.Watch, id=id)

    if request.method == "POST":
        request.session['product_id'] = product.id
        request.session['quantity'] = request.POST.get('quantity', 1)
        return redirect('payment')

    return render(request, 'product_details.html', {'product': product})

def add_to_cart(request, id):

    if "email" not in request.session:
        return redirect("login")

    user = models.User.objects.get(
        Email=request.session["email"]
    )

    watch = models.Watch.objects.get(id=id)

    cart_item = models.Cart.objects.filter(
        user=user,
        watch=watch
    ).first()

    if cart_item:

        cart_item.quantity += 1
        cart_item.save()

    else:

        models.Cart.objects.create(
            user=user,
            watch=watch,
            quantity=1
        )

    return HttpResponse("<script>alert('Item added to cart successfully');window.location.href = '/cart/';</script>")

def cart(request):

    if "email" not in request.session:
        return redirect("login")

    user = models.User.objects.get(
        Email=request.session["email"]
    )

    cart_items = models.Cart.objects.filter(
        user=user
    )

    total = 0

    for item in cart_items:

        total += item.watch.price * item.quantity

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )
def remove_cart(request, id):

    cart_item = models.Cart.objects.get(id=id)

    cart_item.delete()

    return redirect('cart')


# ADD TO WISHLIST
def add_to_wishlist(request, id):

    watch = models.Watch.objects.get(id=id)

    models.Wishlist.objects.get_or_create(
        watch=watch
    )

    return redirect('wishlist')


# WISHLIST PAGE
def wishlist(request):

    wishlist_items = models.Wishlist.objects.all()

    return render(
        request,
        'wishlist.html',
        {
            'wishlist_items': wishlist_items
        }
    )
    
def remove_wishlist(request, id):

    wishlist_item = get_object_or_404(models.Wishlist, id=id)
    wishlist_item.delete()

    return HttpResponse("<script>alert('Item removed from wishlist successfully');window.location.href = '/wishlist/';</script>")


    
    
    # PAYMENT PAGE
def payment(request):
    product_id = request.session.get('product_id')
    quantity = request.session.get('quantity', 1)

    product = get_object_or_404(models.Watch, id=product_id)

    total = product.price * int(quantity)

    return render(request, 'payment.html', {
        'product': product,
        'quantity': quantity,
        'total': total
    })


# BUY NOW
def buynow_page(request, id):
    product = get_object_or_404(models.Watch, id=id)
    return render(request, 'buynow.html', {'product': product})

def buy_cart(request):

    if 'email' not in request.session:
        return redirect('login')

    user = models.User.objects.get(
        Email=request.session['email']
    )

    cart_items = models.Cart.objects.filter(
        user=user
    )

    total = 0

    for item in cart_items:

        total += item.watch.price * item.quantity

    if request.method == "POST":

        payment = request.POST.get('payment')

        request.session['payment'] = payment
        request.session['total'] = float(total)

        # Optional: Clear cart after successful order
        cart_items.delete()

        return HttpResponse("<script>alert('Order placed successfully');window.location.href = '/success/';</script>")

    return render(
        request,
        'buy_cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )



# PAYMENT SUCCESS
def payment_success(request):

    total = request.session.get('total', 0)

    method = request.session.get(
        'payment_method',
        'Unknown'
    )

    return render(
        request,
        'success.html',
        {
            'total': total,
            'method': method
        }
    )