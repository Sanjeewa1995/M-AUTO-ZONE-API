from django.urls import path
from request.views import VehiclePartRequestListCreateView, VehiclePartRequestDetailView,   vehicle_part_request_stats_view

app_name = 'request'

urlpatterns = [
    # Vehicle Part Request URLs
    path('vehicle-part-requests/',
         VehiclePartRequestListCreateView.as_view(),
         name='vehicle-part-request-list-create'),
    path('vehicle-part-requests/<int:pk>/',
         VehiclePartRequestDetailView.as_view(),
         name='vehicle-part-request-detail'),
    path('vehicle-part-requests/stats/',
         vehicle_part_request_stats_view,
         name='vehicle-part-request-stats'),
]
