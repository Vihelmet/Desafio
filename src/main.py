import os

from flask import Flask, request, jsonify
from dotenv import load_dotenv

from utils.utils import api_openweather, api_chatgpt
from utils.sql import save_answer

load_dotenv()

app = Flask(__name__)

@app.route('/chatgpt', methods=['GET', 'POST'])
def chatgpt():
    """
    Function to handle the chatbot API endpoint for receiving user questions and providing responses.

    Returns:
    JSON response containing the chatbot's answer to the user's question.

    This function is designed to be called when a client sends a POST request to the '/chatgpt' endpoint.
    It expects a JSON payload containing a 'question' field with the user's question.

    The function retrieves the JSON data from the request using 'request.get_json()'.
    If the JSON payload contains a 'question' field, it calls the 'api_chatgpt()' function to obtain
    the chatbot's answer to the user's question.

    If the 'user_id' field is present in the JSON payload, it saves the chatbot's answer to the database
    for the corresponding user using the 'save_answer()' function.

    Finally, the function returns a JSON response containing the chatbot's answer.
    If any exception occurs during the execution, the function catches the exception and returns a JSON
    response indicating an Internal Server Error (status code 500).
    """
    try:
        data = request.json  #get_json()

        # Check if the JSON payload contains a 'question' field
        if "question" in data:
            # Call the 'api_chatgpt()' function to obtain the chatbot's answer to the user's question
            answer = api_chatgpt(data["question"])
        else:
            # If the 'question' field is not present in the JSON payload, return a Bad Request JSON response
            return jsonify({"error": "Bad Request !!TETO!!"}), 400 # , "status_code": 400

        # Check if the 'user_id' field is present in the JSON payload
        if "user_id" in data:
            # Save the chatbot's answer to the database for the corresponding user
            save_answer(data["user_id"], answer)

        # Return a JSON response containing the chatbot's answer
        return jsonify(answer)

    except Exception as err:
        # If any exception occurs during the execution, return a JSON response indicating an Internal Server Error (status code 500)
        return jsonify({"answer": "Gracias por rellenar el formulario. Parece que estamos teniendo problemas técnicos. Vuelva a intentarlo más tarde, por favor."}), 500 # "Internal Server Error" , "status_code": 500


    
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
