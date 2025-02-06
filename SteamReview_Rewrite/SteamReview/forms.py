from django import forms
import requests

class GameSelectForm(forms.Form):
    game_choice = forms.ChoiceField(
        label="Select Game:",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, searched_game=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Url for Steam API
        url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        try:
            # Getting JSON data from Steam API
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Steam API: {e}")

        # Creating variable that stores all the games
        apps = data.get("applist", {}).get("apps", [])

        # Searching through all games to find those that match what user is searching for
        if searched_game:
            matches = [app for app in apps if searched_game.lower() in app['name'].lower()]
        else:
            matches = apps

        # Displaying only 10 most accurate results
        limited_choices = sorted(
            [(app['appid'], app['name']) for app in matches if app['name']],
            key=lambda x: x[1]
        )[:10]

        # Putting those 10 results in game choice form in html
        self.fields['game_choice'].choices = limited_choices
