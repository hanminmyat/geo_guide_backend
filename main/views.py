from rest_framework.decorators import api_view
from .serializers import NearbyResultsViewModelSerializer
import requests
from django.conf import settings
from rest_framework.response import Response
from django.http import JsonResponse

def get_google_map_api_key():
    return settings.__getattr__('GOOGLE_MAP_API_KEY')

@api_view(['GET'])
def nearby_location_list(request):
    if request.method == 'GET':
        lat = request.query_params['lat']
        log = request.query_params['log'] 
        distance = request.query_params['distance']
        type = request.query_params.get('type', '')
              
        params = {
            "location": f"{lat},{log}",
            "radius": distance,
            "type": type,
            "key": get_google_map_api_key(),
        }

        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

        response = requests.get(url, params=params)

        if response.status_code == 200:
            places = response.json()["results"]
            # serializer = NearbyResultsViewModelSerializer(places, many=True)
            viewmodel_list = []
            for place in places:
                if place == places[0]:
                    continue
                
                place_view_model = NearbyResultsViewModelSerializer(place)
                viewmodel_list.append(place_view_model.data)

            return Response(viewmodel_list)
        else:
            raise Exception(f"Error fetching places: {response.status_code}")


@api_view(['GET'])
def location_detail_view(request):
        place_id = request.query_params["placeId"]
        mapApiKey = get_google_map_api_key()
        url = f'https://maps.googleapis.com/maps/api/place/details/json?key={mapApiKey}&place_id={place_id}'
        
        response = requests.get(url)
        data = response.json()
        
        if data.get('status') == 'OK':
            result = data['result']

            # Extract the desired information from the API response
            shop_info = {
                'name': result.get('name', ''),
                'logo_or_image': result.get('icon', ''),
                'address': result.get('formatted_address', ''),
                'rating': result.get('rating', ''),
                'open_hours': result.get('opening_hours', {}).get('weekday_text', []),
                'top_reviews': result.get('reviews', [])[:5],
            }

            return JsonResponse(shop_info)
        else:
            return JsonResponse({'error': 'Could not retrieve shop details'})

            