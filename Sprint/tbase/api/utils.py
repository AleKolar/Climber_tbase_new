import requests
import json
from ..models import Coords


def get_coords_data():
    coords_instance = Coords.objects.first()

    if coords_instance:
        coords_data = {
            "latitude": coords_instance.latitude,
            "longitude": coords_instance.longitude,
            "id": coords_instance.id,
        }
        return coords_data
    else:
        return None


def send_data_to_external_api(data):
    external_api_url = 'http://example.com/api/submit/'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(external_api_url, data=json.dumps(data), headers=headers)
    return response


# Ваш текущий код для формирования данных
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
        {"title": "Image 1", "data": "Image Data 1"},
        {"title": "Image 2", "data": "Image Data 2"}
    ],
    "status": "new"
}

# Отправка данных на внешний API
response = send_data_to_external_api(data)

# Обработка ответа
if response.status_code == 200:
    print("Отправлено успешно и на внешний API")
    print("Response:", response.json())
else:
    print("Ошибка при отправке на внешний API")
    print("Response:", response.text)
