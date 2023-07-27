import os

import requests
import openai


# LOCALIZACION --> TEMPERATURA
def api_openweather(lat, lon):
    try:
        api_key = os.getenv("API_KEY_OPENWEATHERMAP")
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        res = requests.get(url)
        data = res.json()
        return data['main']['temp']
    
    except Exception as err:
        raise(f"api_openweather: {err}")
    

# FORMULARIO --> RESPUESTA
def api_chatgpt(genero, edad, peso, agua, enfermedad, medicacion, actividad, sol):
    try:
        openai.api_key = os.getenv("API_KEY_OPENAI")
        prompt = f"Soy de género {genero}." \
                 f"Tengo {edad} años." \
                 f"Peso {peso} kilos." \
                 f"Bebo agua {agua}." \
                 f"{enfermedad} tengo enfermedad preexistente." \
                 f"{medicacion} tomo medicación." \
                 f"Realizo {actividad} actividad física." \
                 f"Estoy expuesto al sol {sol}." \
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
    except Exception as e:
        return "ERROR {e}"
