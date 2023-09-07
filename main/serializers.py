from rest_framework import serializers

class NearbyResultsViewModelSerializer(serializers.Serializer):
    place_id = serializers.CharField()
    icon = serializers.CharField(required = False)
    name = serializers.CharField()
    vicinity = serializers.CharField()
    business_status = serializers.CharField(required = False)
    rating = serializers.IntegerField(required = False)
    price_level = serializers.IntegerField(required = False)
    open_now = serializers.BooleanField(required= False)
    types = serializers.ListField(child=serializers.CharField(), required = False)
    
    def get_rating(self, obj):
        return obj.rating if obj.rating else 0
    
    def get_priceLevel(self, obj):
        return obj.price_level if obj.price_level else 0
    
    def get_business_status(self, obj):
        return obj.business_status if obj.business_status else "Closed_Temporarily"
    
    def get_types(self, obj):
        return obj.type if obj.type else []
    
    def get_openNow_status(self, obj):
        return obj["opening_hours"]["open_now"] if obj["opening_hours"]["open_now"] and obj.business_status == 'OPERATIONAL' else False
    
    def to_dict(self, obj):
        data = super().to_representation(obj)
        data["rating"] = self.get_rating(obj)
        data["business_status"] = self.get_business_status(obj)
        data["types"] = self.get_type(obj)
        data["price_level"] = self.get_priceLevel(obj)
        data["open_now"] = self.get_openNow_status(obj)
        return data;
    
    class Meta:
        fields = ["place_id", "name","vicinity","business_status", "rating", "types", "price_level", "open_now"]

