from django.urls import re_path
from .import views

urlpatterns = [
    re_path(r'^api/nearby_locations$', views.nearby_location_list),
    re_path(r'^api/get_location_details$', views.location_detail_view, name='get_location_details')
]
