from re import search
from .forms import GameSelectForm

from django.shortcuts import render, redirect
from SteamReview.forms import GameSelectForm
import requests

# Page that fetches a site to select a game
def GameSelection(request):
    # Getting a game to search for
    searched_game = request.GET.get('q', '')

    # Sending searched game to form in forms.py
    form = GameSelectForm(searched_game=searched_game)
    game_details = None

    if request.method == 'POST':
        #Showing game details after selecting game
        #Getting data from steam site to then display on mine site
        app_id = request.POST.get('app_choice')
        url = f"http://store.steampowered.com/api/appdetails?appids={app_id}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            api_data = response.json()
            game_details = api_data.get(app_id, {}).get('data', {})
        except requests.RequestException as e:
            game_details = {'error': str(e)}

        #Returning page with game details
        # return render(request, 'newReview.html', {
        #     'form': form,
        #     'game_details': game_details,
        #     'app_id': app_id,
        # })
        return redirect('NewReview', {
            'app_id': app_id,
        })

    return render(request, 'GameSelection.html', {
        'form': form,
        'game_details': game_details,
    })

def NewReview(request):
    searched_game = request.POST.get('searched_game')

    # Redirect to page with review
    return render(request)
