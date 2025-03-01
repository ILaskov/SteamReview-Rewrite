from re import search
from django.contrib.auth.decorators import login_required
from .forms import GameSelectForm
from django.shortcuts import render, redirect, get_object_or_404
from SteamReview.forms import GameSelectForm
import requests, markdown
from .models import Review
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages

#Creating main page with all reviews ordered by date
def index(request):
    reviews = Review.objects.all().order_by('-timestamp')
    return render(request, 'Index.html', {'reviews': reviews})


# Page that fetches a site to select a game
@login_required
def GameSelection(request):
    # Getting a game to search for
    searched_game = request.GET.get('q', '')

    # Sending searched game to form in forms.py
    form = GameSelectForm(searched_game=searched_game)
    game_details = None

    if request.method == 'POST':
        #Getting data from steam site to then display on mine site
        app_id = request.POST.get('game_choice')
        url = f"http://store.steampowered.com/api/appdetails?appids={app_id}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            api_data = response.json()
            game_details = api_data.get(app_id, {}).get('data', {})
        except requests.RequestException as e:
            game_details = {'error': str(e)}

        return redirect('NewReview', app_id=app_id)

    return render(request, 'GameSelection.html', {
        'form': form,
        'game_details': game_details,
    })

#Page to write your review
def NewReview(request, app_id):
    # Getting data from steam site to then display on mine site
    if app_id:
        url = f"http://store.steampowered.com/api/appdetails?appids={app_id}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            api_data = response.json()
            game_details = api_data.get(str(app_id), {}).get('data', {})
        except requests.RequestException as e:
            game_details = {'error': str(e)}

    if request.method == 'POST':
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')

        if review_text:
            formatted_text = markdown.markdown(review_text)

            # Creating a review object from models.py to store in database
            if app_id:
                # Getting data from my site and steam site to make review object
                url = f"http://store.steampowered.com/api/appdetails?appids={app_id}"
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    api_data = response.json()
                    game_details = api_data.get(str(app_id), {}).get('data', {})
                    app_name = game_details.get('name')
                    app_developers = ', '.join(game_details.get('developers', []))
                    image_url = game_details.get('header_image')
                    user = request.user
                except requests.RequestException as e:
                    game_details = {'error': str(e)}

                # Creating review object
                review = Review.objects.create(
                    app_id=app_id,
                    app_name=app_name,
                    app_developers=app_developers,
                    image_url=image_url,
                    review_text=formatted_text,
                    rating=rating,
                )

                # Redirect to page with review
                return redirect('ReviewDetails', pk=review.pk)
        else:
            messages.error(request, 'No review text provided')
            return render(request, 'NewReview.html', {
                'app_id': app_id,
                'game_details': game_details,
            })

    return render(request, 'NewReview.html', {
        'app_id': app_id,
        'game_details': game_details,
    })

#Page that shows review
def ReviewDetails(request, pk):
    #Gets object from database
    review = get_object_or_404(Review, pk=pk)

    if review.app_id:
        # Getting data from steam site to then display on mine site
        url = f"http://store.steampowered.com/api/appdetails?appids={review.app_id}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            api_data = response.json()
            game_details = api_data.get(review.app_id, {}).get('data', {})
        except requests.RequestException as e:
            game_details = {'error': str(e)}

    #Rendering site with all necessary data
    return render(request, 'Review.html', {
        'review': review,
        'game_details':game_details,
    })

#Register page
def Register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, "Register.html", {
        'form': form,
    })

#Login page
def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, "Login.html", {
        'form': form,
    })

#Loging out
def Logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
