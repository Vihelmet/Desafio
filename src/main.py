import pickle
from flask import Flask, request, jsonify

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
