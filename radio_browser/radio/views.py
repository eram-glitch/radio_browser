
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests
from .models import Favorite

def home(request):
    return render(request, 'home.html')

def search_stations(request):
    query = request.GET.get('query', '')
    page = int(request.GET.get('page', 1))
    limit = 15
    offset = (page - 1) * limit
    url = f'http://all.api.radio-browser.info/json/stations/search?name={query}&limit={limit}&offset={offset}'
    response = requests.get(url)
    stations = response.json()
    return JsonResponse(stations, safe=False)

@login_required
def favorites(request):
    user_favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'favorites': user_favorites})

@login_required
def add_favorite(request):
    if request.method == 'POST':
        station_id = request.POST.get('station_id')
        name = request.POST.get('name')
        url = request.POST.get('url')
        country = request.POST.get('country')
        
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            station_id=station_id,
            defaults={'name': name, 'url': url, 'country': country}
        )
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def remove_favorite(request):
    if request.method == 'POST':
        station_id = request.POST.get('station_id')
        Favorite.objects.filter(user=request.user, station_id=station_id).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})