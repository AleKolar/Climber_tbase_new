import requests
import json
from ..models import Coord

def get_coords_data():
    coords_instance = Coord.objects.first()

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
        {"title": "Image 1", "data": "Image Data 1"},  # Добавлены данные для изображений
        {"title": "Image 2", "data": "Image Data 2"}
    ],
    "status": "new"
}