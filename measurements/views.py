from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo
# Create your views here.


def calculate_distance_view(request):
    obj = get_object_or_404(Measurement, id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='measurements')

    ip = '72.14.207.99'
    country, city, lat, lon = get_geo(ip)
    location = geolocator.geocode(city)

    # location coordinates

    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data['destination']
        destination = geolocator.geocode(destination_)

        # Destination Coordinates

        d_lat = destination.latitude
        d_lon = destination.longitude

        pointB = (d_lat, d_lon)

        # Distance calculation

        distance = round(geodesic(pointA, pointB).km, 2)

        instance.location = location
        instance.distance = distance
        instance.save()

    context = {
        'distance': obj,
        'form': form,
    }

    return render(request, 'measurements/main.html', context)
