import requests
import json
from rest_framework import request


url = 'http://some_kind_of_external_api_where_will_I_send_it_url/submitData/'

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
    "coords": {
        "latitude": request.data.get('latitude'),
        "longitude": request.data.get('longitude')
    },
    "level": {
        "winter": "High",
        "summer": "Low",
        "autumn": "Medium",
        "spring": "High"
    },
    "images": [
        {"title": "Image 1"},
        {"title": "Image 2"}
    ]
}

headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.json())