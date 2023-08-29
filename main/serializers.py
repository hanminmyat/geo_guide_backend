from django.conf import settings
from rest_framework import serializers

# class LocationSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=255)
#     address = serializers.CharField(max_length=255)
#     type = serializers.CharField(max_length=255)
#     distance = serializers.FloatField()

#     def get_logo(self, location):
#         """
#         Returns the logo of the location from the Google Maps API.
#         """
#         params = {
#             "place_id": location["place_id"],
#             "key": {settings.GOOGLE_MAP_API_KEY},
#         }

#         url = "https://maps.googleapis.com/maps/api/place/details/json"

#         response = request.get(url, params=params)

#         if response.status_code == 200:
#             return response.json()["result"]["photos"][0]["photo_reference"]
#         else:
#             return None

#     def to_representation(self, instance):
#         """
#         Returns the representation of the location.
#         """
#         representation = super().to_representation(instance)
#         representation["logo"] = self.get_logo(instance)
#         return representation

class NearbyResultsViewModelSerializer(serializers.Serializer):
    business_status = serializers.CharField()
    name = serializers.CharField()
    vicinity = serializers.CharField()
    rating = serializers.IntegerField(source='rating')

    class Meta:
        fields = ["business_status", "name","vicinity", "rating"]
