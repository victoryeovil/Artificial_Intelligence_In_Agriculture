from django.shortcuts import render
from .models import *
import requests
from requests.exceptions import RequestException
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    return render(request, 'index.html')


def farmer_dashboard(request):
    # Get crops associated with the logged-in farmer
    crops = Crop.objects.filter(farmer=request.user)

    return render(request, 'dashboard.html', {'crops': crops})




def get_weather_data(request):
    # Handle the case when weather data retrieval fails or mode is invalid
    return render(request, 'weather.html')


def current(request):
    # Get user location and weather mode from the request
    location = request.GET.get('location')
    if not location:
        location = 'Harare' # Default location if not provided

    # Make an API request to retrieve current weather data
    weather_api_key = 'cc212c67c6ed4b64bce142129232805'
    weather_api_url = f'https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={location}'
    
    try:
        response = requests.get(weather_api_url)
        response.raise_for_status()
    except RequestException as e:
        # Handle the case when the request fails
        return render(request, 'current_weather.html', {'error': f'Failed to retrieve weather data: {e}'})

    data = response.json()
    temperature = data['current']['temp_c']
    humidity = data['current']['humidity']
    rainfall = data['current']['precip_mm']

    # Store weather data in the database
    WeatherData.objects.create(location=location, temperature=temperature, humidity=humidity, rainfall=rainfall)

    # Return the weather data to the user interface
    return render(request, 'current_weather.html',
                  {'temperature': temperature, 'humidity': humidity, 'rainfall': rainfall})


def focus(request):
    # Get user location and weather mode from the request
    location = request.GET.get('location')
    if not location:
        location = 'Harare'  # Default location if not provided

    # Make a request to the Focus API to retrieve the location coordinates
    focus_api_key = 'cc212c67c6ed4b64bce142129232805'
    focus_api_url = f'https://api.focus.com/v1/locations?q={location}&key={focus_api_key}'
    
    try:
        response = requests.get(focus_api_url)
        response.raise_for_status()
    except RequestException as e:
        # Handle the case when the request fails
        return render(request, 'forecast_weather.html', {'error': f'Failed to retrieve location coordinates: {e}'})

    data = response.json()
    if data['results']:
        lat = data['results'][0]['latitude']
        lon = data['results'][0]['longitude']

        # Make an API request to retrieve weather datausing the location coordinates
        weather_api_key = 'cc212c67c6ed4b64bce142129232805'
        weather_api_url = f'https://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={lat},{lon}&days=1'
        
        try:
            weather_response = requests.get(weather_api_url)
            weather_response.raise_for_status()
        except RequestException as e:
            # Handle the case when the request fails
            return render(request, 'forecast_weather.html', {'error': f'Failed to retrieve weather data: {e}'})

        weather_data = weather_response.json()
        forecast = weather_data['forecast']['forecastday'][0]['day']
        temperature = forecast['avgtemp_c']
        humidity = forecast['avghumidity']
        rainfall = forecast['totalprecip_mm']

        # Store weather data in the database
        WeatherData.objects.create(location=location, temperature=temperature, humidity=humidity,
                                       rainfall=rainfall)

        # Return the weather data to the user interface
        return render(request, 'forecast_weather.html',
                          {'temperature': temperature, 'humidity': humidity, 'rainfall': rainfall})


def search_plant(request):
    query = request.GET.get('query')

    # Set up the OpenAI API request
    openai_api_key = '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'
    endpoint = 'https://api.openai.com/v1/engines/davinci-codex/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}',
    }
    data = {
        'prompt': f"Search information about {query} plant",
        'max_tokens': 100,
    }

    # Make a request to the OpenAI API
    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 200:
        data = response.json()
        plants = data['choices'][0]['text']

        return render(request, 'plant_search.html', {'plants': plants})
    else:
        return render(request, 'plant_search.html', {'error': 'Failed to fetch plant information.'})



def plant_search(request):
    query = request.GET.get('query')

    # Set up the Wikipedia API request
    endpoint = f'https://en.wikipedia.org/api/rest_v1/page/summary/{query}'

    # Make a request to the Wikipedia API
    response = requests.get(endpoint)

    if response.status_code == 200:
        data = response.json()
        return render(request, 'plant.html', {'plant': data})
    else:
        return render(request, 'plant.html', {'error': 'Failed to fetch plant information.'})
    



    
def landing(requests):
    return render(requests, 'landing.html')

def plant_disease_detection(request):
        query = request.GET.get('query')
        #image_file = request.FILES['image']

        # Set up the Plant.id API request
        plantid_api_key = 'k9VPUeNqGYKW5Sld5foaviR2PhHg7zXb3jUEXCTEDJNV0LTFf2'
        endpoint = f'https://api.plant.id/v2/identify'
        headers = {
            'Content-Type': 'application/json',
            'Api-Key': plantid_api_key,
        }
        data = {
            'images': [query],
            'organs': ['leaf', 'flower', 'fruit', 'stem', 'bark', 'whole'],
            'organs_details': True,
        }

        try:
            # Make aPOST request to the Plant.id API
            response = requests.post(endpoint, headers=headers, json=data)
            if response.status_code == 200:
                data = response.json()
                if data['suggestions']:
                    plant_name = data['suggestions'][0]['plant_name']
                    plant_details = data['suggestions'][0]['plant_details']
                    common_names = plant_details['common_names']
                    family = plant_details['family']
                    diseases = [disease['name'] for disease in plant_details['diseases']]
                    return render(request, 'plant_disease.html', {'plant_name': plant_name, 'common_names': common_names, 'family': family, 'diseases': diseases})
        except Exception as e:
            # Handle exceptions and errors here
            return HttpResponse('An error occurred.')
        
        # If no data was returned or no suggestions were found, return an empty response
        return HttpResponseRedirect('/')
