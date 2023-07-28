from flask import Flask, jsonify, request
import openai
import requests
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()
api_key = os.getenv('API_KEY')
ow_key = os.getenv('OW_KEY')

# FORMULARIO --> RESPUESTA
def api_chatgpt(nombre, genero, edad, altura, peso, agua, actividad, enfermedad):
    try:
        openai.api_key = api_key
        prompt = f"Me llamo {nombre}" \
                 f"Soy de género {genero}." \
                 f"Tengo {edad} años." \
                 f"Mido {altura} centímetros" \
                 f"Peso {peso} kilos." \
                 f"Bebo agua {agua}." \
                 f"Realizo {actividad} actividad física." \
                 f"Tengo una enfermedad {enfermedad}." \
                 "Quiero que me respondas, según los datos que te acabo de pasar, me des un consejo personalizado sobre el riesgo que tengo de sufrir un golpe de calor" \
                 "Llámame por mi nombre, y hazme una valoración según los datos que te he dado. Dame algún consejo personalizado." \
                 "Limita tu respuesta entre 100 y 150 caracteres." \
                 "Usa un lenguaje cercano."
        completion = openai.Completion.create(engine='text-davinci-003',
                                              prompt=prompt,
                                              max_tokens=2048)
        return completion.choices[0].text
    except Exception as e:
        return "Gracias por rellenar el formulario. Parece que estamos teniendo problemas técnicos. Vuelva a intentarlo más tarde, por favor."

@app.route('/chatgpt', methods=['GET'])
def chatgpt():
    nombre = request.args.get('nombre')
    genero = request.args.get('genero')
    edad = request.args.get('edad')
    altura = request.args.get('altura')
    peso = request.args.get('peso')
    agua = request.args.get('agua')
    actividad = request.args.get('actividad')
    enfermedad = request.args.get('enfermedad')
    respuesta = api_chatgpt(nombre, genero, edad, altura, peso, agua, actividad, enfermedad)
    return jsonify(respuesta)

# LOCALIZACION --> TEMPERATURA
def api_openweather(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={ow_key}&units=metric"
        res = requests.get(url)
        data = res.json()
        temp = data['main']['temp']
        return f"{temp}°"
    except Exception as e:
        return "30°"
    
@app.route('/openweather', methods=['GET'])
def openweather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    temperatura = api_openweather(lat, lon)
    return jsonify(temperatura)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)