from rest_framework import serializers

class NearbyResultsViewModelSerializer(serializers.Serializer):
    place_id = serializers.CharField()
    name = serializers.CharField() 
    vicinity = serializers.CharField()
    business_status = serializers.CharField(required = False)
    rating = serializers.IntegerField(required = False),
    types = serializers.ListField(child=serializers.CharField(), required = False)
    
    def get_rating(self, obj):
        return obj.rating if obj.rating else 0
    
    def get_business_status(self, obj):
        return obj.business_status if obj.business_status else "Closed_Temporarily"
    
    def get_types(self, obj):
        return obj.type if obj.type else []
    
    def to_dict(self, obj):
        data = super().to_representation(obj)
        data["rating"] = self.get_rating(obj)
        data["business_status"] = self.get_business_status(obj)
        data["types"] = self.get_type(obj)
        return data;
    
    class Meta:
        fields = ["place_id", "name","vicinity","business_status", "rating", "types"]

