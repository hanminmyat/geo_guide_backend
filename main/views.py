from rest_framework.decorators import api_view
from rest_framework import viewsets
from .serializers import NearbyResultsViewModelSerializer
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
import requests
from django.conf import settings
from rest_framework.response import Response

# class NearbyLocationsView(APIView):
#     """
#     Retrieve nearby locations.
#     """

#     @staticmethod
#     def get_user_location(request):
#         """
#         Gets the user's GPS location.
#         """
#         user = request.user
#         if user.is_authenticated:
#             return Point(user.latitude, user.longitude)
#         return None

#     @api_view(['GET'])
#     def get(self, request):
#         """
#         Retrieve nearby locations based on the user's GPS location.
#         """
#         lat = request.query_params['lat']
#         log = request.query_params['log']

#         params = {
#             "location": f"{lat},{log}",
#             "radius": request.query_params['distance'],
#             "type": request.query_params['type'],
#             "key": "{settings.GOOGLE_MAP_API_KEY}",
#         }

#         url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

#         response = requests.get(url, params=params)

#         if response.status_code == 200:
#             places = response.json()["results"]
#             serializer = LocationSerializer(places, many=True)
#             return Response(serializer.data)
#         else:
#             raise Exception(f"Error fetching places: {response.status_code}")

@api_view(['GET'])
def nearby_location_list(request):
    if request.method == 'GET':
        lat = request.query_params['lat']
        log = request.query_params['log']        
        google_map_api_key = settings.__getattr__('GOOGLE_MAP_API_KEY')
        params = {
            "location": f"{lat},{log}",
            "radius": request.query_params['distance'],
            "type": request.query_params['type'],
            "key": google_map_api_key,
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
                
                place_view_model = nearby_location_viewModel(place)
                viewmodel_list.append(place_view_model)

            return Response(viewmodel_list)
        else:
            raise Exception(f"Error fetching places: {response.status_code}")

def nearby_location_viewModel(place):
    newPlaceModel = {
        "name": place['name'],
        "rating" : place['rating'],
        "business_status": place['business_status'],
        "vicinity": place['vicinity'],
        "types": place['types']
    }
    return newPlaceModel