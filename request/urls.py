from django.urls import path
from . import views

app_name = 'request'

urlpatterns = [
    # Vehicle Part Request URLs
    path('vehicle-part-requests/', 
         views.VehiclePartRequestListCreateView.as_view(), 
         name='vehicle-part-request-list-create'),
    path('vehicle-part-requests/<int:pk>/', 
         views.VehiclePartRequestDetailView.as_view(), 
         name='vehicle-part-request-detail'),
    path('vehicle-part-requests/stats/', 
         views.vehicle_part_request_stats_view, 
         name='vehicle-part-request-stats'),
]
