import os

import requests
import openai


def api_openweather(lat: str, lon: str) -> tuple[dict, float]: 
    """
    Function to retrieve the current temperature from OpenWeatherMap API based on the provided latitude and longitude.

    Parameters:
        lat (str): Latitude coordinate.
        lon (str): Longitude coordinate.

    Returns:
        dict: code Code of error, message Description of error
        float: Current temperature in Celsius if successful, or a JSON response with error information if unsuccessful.
    
    Raises:
        Exception: If any error occurs during the API request or data processing.
    """
    try:
        # Retrieve the API key from environment variable
        api_key = os.getenv("API_KEY_OPENWEATHERMAP")

        # Construct the API URL with latitude, longitude, API key, and units (metric for Celsius)
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

        # Send a GET request to the API URL and obtain the response in JSON format
        res = requests.get(url)
        data = res.json()

        # Check if the API response contains error information (status code other than 200)
        if data["cod"] != 200:
            return data  # Return the JSON response with error information
        else:
            # If the response is successful, extract and return the current temperature in Celsius
            return data['main']['temp']

    except Exception as err:
        # If any exception occurs during the API request or data processing, raise an exception with the error message
        raise Exception(f"api_openweather: {err}")

    

# FORMULARIO --> RESPUESTA
def api_chatgpt(data: dict):
    try:
        openai.api_key = os.getenv("API_KEY_OPENAI")
        prompt = f"Soy de género {data['genero']}." \
                 f"Tengo {data['edad']} años." \
                 f"Peso {data['peso']} kilos." \
                 f"Bebo agua {data['agua']}." \
                 f"{data['enfermedad']} tengo enfermedad preexistente." \
                 f"{data['medicacion']} tomo medicación." \
                 f"Realizo {data['actividad']} actividad física." \
                 f"Estoy expuesto al sol {data['sol']}." \
                 "Quiero que me respondas en 4 bloques:" \
                 "Según mis datos, quiero que me hagas una valoración personalizada, 100 a 200 caracteres, sobre la posibilidad que tengo de sufrir un golpe de calor." \
                 "Hazme una lista de 5 medidas que debería tomar los días más calurosos para evitar un golpe de calor." \
                 "Hazme una liststa de 5 síntomas que puedo sufrir con un golpe de calor." \
                 "Finaliza añadiendo que si padezco alguno de ellos, acuda al centro de salud más cercano." \
                 "Usa un lenguaje formal pero accesible."
        
        completion = openai.Completion.create(engine='text-davinci-003',
                                            prompt=prompt,
                                            max_tokens=2048)
        return completion.choices[0].text
    except Exception as err:
        return f"ERROR {err}"
