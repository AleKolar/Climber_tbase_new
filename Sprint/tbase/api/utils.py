import requests
import json
from rest_framework.request import Request

from ..models import Coords

def get_coords_data():
    coords_instance = Coords.objects.first()

    if coords_instance:
        coords_data = {
            "latitude": coords_instance.latitude,
            "longitude": coords_instance.longitude
        }
        return coords_data
    else:
        return None

coords = get_coords_data()

data = {
    "beauty_title": "Beautiful Title",
    "title": "Title",
    "other_titles": "Other Titles",
    "connect": "Connection Info",
    "add_time": "2022-01-01T12:00:00Z",
    "user": {
        "email": "user@example.com",
        "name": "User Name"
    },
    "coords": coords,
    "level": {
        "winter": "High",
        "summer": "Low",
        "autumn": "Medium",
        "spring": "High"
    },
    "images": [
        {"title": "Image 1"},
        {"title": "Image 2"}
    ],
    "status": "new"
}