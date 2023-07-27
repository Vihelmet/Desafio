import os
import pickle


from flask import Flask, request, jsonify, make_response
from dotenv import load_dotenv

from utils.utils import api_openweather, api_chatgpt

load_dotenv()

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

    
@app.route('/openweather', methods=['GET'])
def openweather():
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        temperatura = api_openweather(lat, lon)
        return jsonify(temperatura)
    except Exception as err:
        return make_response(err, 500)


if __name__ == '__main__':
    app.run(host=os.getenv("FLASK_RUN_HOST"), port=os.getenv("FLASK_RUN_PORT"))
