from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from datetime import datetime
import logging


from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealer_reviews_from_cf, post_request

# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/d8e38deb-4063-49c9-a27b-c9eb3d80bdad/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context = {'dealerships': dealerships}
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


def get_dealership(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/d8e38deb-4063-49c9-a27b-c9eb3d80bdad/api/dealership"
        dealerships = get_dealer_by_id(url, "7c97b90dce394280045a0e50d4eed89b")
        return HttpResponse(dealerships)


def get_view_test_page(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/view.html', context)


def about_us(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


def contact_us(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')


def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)


def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


def get_dealer_details(request, dealer_id):
    url = 'https://us-south.functions.appdomain.cloud/api/v1/web/d8e38deb-4063-49c9-a27b-c9eb3d80bdad/api/review'

    reviews = get_dealer_reviews_from_cf(url, dealer_id)
    context = {
        "reviews": reviews
    }

    return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealer_id=0):
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to post a review.")

    if request.method == 'POST':
        review = {"time": datetime.utcnow().isoformat(), "name": request.user.username, "dealership": dealer_id,
                  "review": request.POST.get("review"), "purchase": request.POST.get("purchase")}

        json_payload = {"review": review}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/d8e38deb-4063-49c9-a27b-c9eb3d80bdad/api/review"
        response = post_request(url, json_payload, dealerId=dealer_id)
        # Handle the response here
        return HttpResponse(response.text)
    else:
        context = {
            "cars": [
                {"id": 1, "make": "Toyota", "year": "2020"},
                {"id": 2, "make": "BMW", "year": "2021"},
                {"id": 3, "make": "Mercedes", "year": "2018"},
            ]
        }
        return render(request, "djangoapp/add_review.html", context)
