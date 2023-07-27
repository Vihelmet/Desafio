import requests


def temperatura(ciudad):
    
    try:

        url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=bb3d32afaf3faac9ed88f681a557f98d&units=metric".format(ciudad)

        res = requests.get(url)

        data = res.json()

        temp = data['main']['temp']

        return print(temp)
    
    except Exception as e:

        return print(f"ERROR {e}")