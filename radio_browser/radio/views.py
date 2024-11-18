from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from pyradios import RadioBrowser
from .models import Favorite
from django.core.paginator import Paginator
import json
from django.views.decorators.http import require_http_methods

def home(request):
    return render(request, 'home.html')

def search(request):
    query = request.GET.get('query', '')
    page = int(request.GET.get('page', 1))
    rb = RadioBrowser()
    
    if query:
        stations = rb.search(name=query, limit=1000)  # Adjust limit as needed
    else:
        stations = rb.stations(limit=1000)  # Adjust limit as needed

    paginator = Paginator(stations, 12)  # 12 stations per page
    page_obj = paginator.get_page(page)

    return JsonResponse({
        'results': list(page_obj),
        'total_pages': paginator.num_pages,
    })

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
def favorites(request):
    user_favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'favorites': user_favorites})

@login_required
def favorites_list(request):
    user_favorites = Favorite.objects.filter(user=request.user)
    favorites_data = [
        {
            'id': favorite.id,
            'station_id': favorite.station_id,
            'name': favorite.name,
            'url': favorite.url,
            'country': favorite.country
        }
        for favorite in user_favorites
    ]
    return JsonResponse(favorites_data, safe=False)

@login_required
def remove_favorite(request):
    if request.method == 'POST':
        station_id = request.POST.get('station_id')
        if not station_id:
            return JsonResponse({'success': False, 'message': 'Station ID is required'})
        
        deleted, _ = Favorite.objects.filter(user=request.user, station_id=station_id).delete()
        if deleted:
            return JsonResponse({'success': True, 'message': 'Favorite removed successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Favorite not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})