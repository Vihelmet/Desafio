import requests


def temperatura(lat, lon, api_key):
    
    try:

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

        res = requests.get(url)

        data = res.json()

        temp = data['main']['temp']

        return print(f"{temp}°")
    
    except Exception as e:

        return print("30°")