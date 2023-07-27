import pickle
import openai
import requests
from flask import Flask, request, jsonify

api_key = 'API_KEY'

app = Flask(__name__)

# Cargamos el modelo desde el archivo .pkl
with open('../models/modelo_tree.pkl', 'rb') as archivo_entrada:
    modelo_entrenado = pickle.load(archivo_entrada)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()  # Recibimos los datos del cliente en formato JSON

    # Asegurémonos de que recibimos los datos correctos
    if "features" not in data:
        return jsonify({"error": "Los datos deben contener un atributo 'features'"}), 400

    # Recuperamos las características para hacer la predicción
    features = data["features"]

    # Asegurémonos de que las características son del tipo adecuado y en el orden correcto
    if not isinstance(features, list) or len(features) != 3:
        return jsonify({"error": "Las características deben ser una lista con {} elementos".format(3)}), 400

    # Realizamos la predicción
    try:
        prediction = modelo_entrenado.predict([features])[0]
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Devolvemos la predicción como resultado
    return jsonify({"prediction": prediction})



# FORMULARIO --> RESPUESTA
def api_chatgpt(genero, edad, peso, agua, enfermedad, medicacion, actividad, sol):
    try:
        openai.api_key = api_key
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

@app.route('/chatgpt', methods=['GET'])
def chatgpt():
    genero = request.args.get('genero')
    edad = request.args.get('edad')
    peso = request.args.get('peso')
    agua = request.args.get('agua')
    enfermedad = request.args.get('enfermedad')
    medicacion = request.args.get('medicacion')
    actividad = request.args.get('actividad')
    sol = request.args.get('sol')
    respuesta = api_chatgpt(genero, edad, peso, agua, enfermedad, medicacion, actividad, sol)
    return jsonify(respuesta)

# LOCALIZACION --> TEMPERATURA
def api_openweather(ciudad):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=bb3d32afaf3faac9ed88f681a557f98d&units=metric".format(ciudad)
        res = requests.get(url)
        data = res.json()
        temp = data['main']['temp']
        return f'{ciudad}: {temp}°'
    except Exception as e:
        return f"ERROR {e}"
    
@app.route('/openweather', methods=['GET'])
def openweather():
    ciudad = request.args.get('ciudad')
    temperatura = api_openweather()
    return jsonify(temperatura)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
