import os
import pickle


from flask import Flask, request, jsonify
from dotenv import load_dotenv

from utils.utils import api_openweather, api_chatgpt

load_dotenv()

app = Flask(__name__)

# Cargamos el modelo desde el archivo .pkl
#with open('../models/modelo_tree.pkl', 'rb') as archivo_entrada:
#    modelo_entrenado = pickle.load(archivo_entrada)

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
    try:
        data = {}
        data["genero"] = request.args.get('genero')
        data["edad"] = request.args.get('edad')
        data["peso"] = request.args.get('peso')
        data["agua"] = request.args.get('agua')
        data["enfermedad"] = request.args.get('enfermedad')
        data["medicacion"] = request.args.get('medicacion')
        data["actividad"] = request.args.get('actividad')
        data["sol"] = request.args.get('sol')
        
        respuesta = api_chatgpt(data)
        return jsonify(respuesta)
    except Exception as err:
        # If any exception occurs during the execution, return a JSON response 
        # indicating an Internal Server Error (status code 500)
        return jsonify({"error": "Internal Server Error", "status_code": 500})

    
@app.route('/openweather', methods=['GET'])
def openweather():
    try:
        lat = request.args.get('lat')  # Latitude (e.g., 51.5156177)
        lon = request.args.get('lon')  # Longitude (e.g., -0.0919983)

        # Return a JSON response indicating a Bad Request (status code 400) 
        # if latitude or longitude is missing
        if not lat or not lon:
            return jsonify({"error": "Bad Request", "status_code": 400})

        # Call the function api_openweather() to get the temperature data for the given 
        # latitude and longitude
        temperatura = api_openweather(lat, lon)

        # Return a JSON response with the temperature data
        return jsonify(temperatura)

    except Exception as err:
        # If any exception occurs during the execution, return a JSON response indicating 
        # an Internal Server Error (status code 500)
        return jsonify({"error": "Internal Server Error", "status_code": 500})



if __name__ == '__main__':
    app.run(host=os.getenv("FLASK_RUN_HOST"), port=os.getenv("FLASK_RUN_PORT"))
