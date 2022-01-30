from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm  
from .restapis import *

# Get an instance of a logger
logger = logging.getLogger(__name__)


def about_page(request):
    
    justLoggedIn = login_function(request)
    if justLoggedIn:
        return redirect('djangoapp:about_us')

    template = loader.get_template('djangoapp/about.html')
    context = {}
    return HttpResponse(template.render(context, request))


def contact_page(request):
    
    justLoggedIn = login_function(request)
    if justLoggedIn:
        return redirect('djangoapp:contact_us')

    context = {}
    return render(request, 'djangoapp/contact.html', context)


def login_request(request):
    
    justLoggedIn = login_function(request)
    if justLoggedIn:
        return redirect('djangoapp:login')
    template = loader.get_template('djangoapp/login.html')

    context = {}
    return HttpResponse(template.render(context, request))


def logout_request(request):

    if not login_function(request):
        logout(request)

    justLoggedIn = login_function(request)
    if justLoggedIn:
        return redirect('djangoapp:login')

    context = {}
    return render(request, 'djangoapp/logout_page.html', context)


def registration_page(request):
    
    justLoggedIn = login_function(request)
    if justLoggedIn:
        return redirect('djangoapp:register_account')

    template = loader.get_template('djangoapp/registration.html')
    saved = False

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # If the form is valid, save the user fields
            form.save()
            saved = True
    else:
        form = CustomUserCreationForm()

    context = { 'form' : form, 'saved' : saved }
    return HttpResponse(template.render(context, request))


def get_dealerships(request):

    justLoggedIn = login_function(request)
    if justLoggedIn:
        return redirect('djangoapp:index')

    if request.method == "GET":
        template = loader.get_template('djangoapp/index.html')
        url = "https://5c90c98b.us-south.apigw.appdomain.cloud/api/dealership/"
        dealerships = get_dealers_from_cf(url)
        context = {"dealerships": dealerships}
        return (HttpResponse(template.render(context, request)))
    elif not justLoggedIn:
        template = loader.get_template('djangoapp/index.html')
        url = "https://5c90c98b.us-south.apigw.appdomain.cloud/api/dealership/"
        dealerships = get_dealers_from_cf(url)
        context = {"dealerships": dealerships}
        return (HttpResponse(template.render(context, request)))


def get_dealer_details(request, dealership_id):

    justLoggedIn = login_function(request)
    if justLoggedIn:
        return redirect('djangoapp:reviews', dealership_id=dealership_id)

    if request.method == "GET":
        url = "https://5c90c98b.us-south.apigw.appdomain.cloud/api/review/dealership"
        reviews = get_dealer_reviews_from_cf(url, dealership_id, 'cATEkEA-WpY2rQadoGOcQaJoN-lcBzWVihPRXK8EOuN4')
        context = {"reviews": reviews}
        return render(request, 'djangoapp/dealer_details.html', context)
    elif not justLoggedIn:
        url = "https://5c90c98b.us-south.apigw.appdomain.cloud/api/review/dealership"
        reviews = get_dealer_reviews_from_cf(url, dealership_id, 'cATEkEA-WpY2rQadoGOcQaJoN-lcBzWVihPRXK8EOuN4')
        context = {"reviews": reviews}
        return render(request, 'djangoapp/dealer_details.html', context)


from django.contrib.auth.decorators import login_required

def add_review(request, car_year=datetime.now().year, car_make="default", car_model="default", purchase_date=datetime.today(), dealership_review="Put your review here", dealership="16", sentiment="neutral"):

    # Is required to already be logged in.

    if request.method == "POST":
        json_payload = dict()
        url = "https://5c90c98b.us-south.apigw.appdomain.cloud/api/review"
        review = dict()
        review["car_year"] = request.POST['car_year']
        review["car_make"] = request.POST['car_make']
        review["car_model"] = request.POST['car_model']
        review["purchase_date"] = request.POST['purchase_date']
        review["dealership_review"] = request.POST['dealership_review']
        review["dealership"] = request.POST['dealership']
        review["sentiment"] = request.POST['sentiment'].lower()
        json_payload["review"] = review
        print(json_payload)
        result = post_request(url, json_payload)
    if request.method == "GET":
        default_payload = dict()
        defaults = dict()
        defaults["car_year"] = car_year
        defaults["car_make"] = car_make
        defaults["car_model"] = car_model
        defaults["purchase_date"] = purchase_date
        defaults["dealership_review"] = dealership_review
        defaults["dealership"] = dealership
        defaults["sentiment"] = sentiment
        default_payload["defaults"] = defaults
        context = {"default_payload": default_payload}
        template = loader.get_template('djangoapp/add_review.html')
        result = (HttpResponse(template.render(context, request)))

    print(result.status_code)

    if request.method == "POST" and result.status_code == 200:
        return redirect('djangoapp:reviews', dealership_id=request.POST.get('dealership', '1'))

    return HttpResponse(result)


def login_function(request):

    # TODO
    # This should be handled somehow
    # It should also be tokenized
    # It should also be a separate module

    try:
        if request.method == 'POST':
            username = request.POST.get('Username')
            password = request.POST.get('Password')
            first_name = request.POST.get('First Name')
            last_name = request.POST.get('Last Name')

            user = authenticate(request, username=username, password=password, first_name=first_name, last_name=last_name)
            
            if user is not None:
                login(request, user)
                return True
            else:
                print('The user did not supply valid credentials, or did not request a log in - thus, they were not logged in.')
    except Exception as error:
        print('An error occurred during a log in attempt!')
        print(error)