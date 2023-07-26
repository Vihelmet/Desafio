from flask import Flask, jsonify
import openai
import requests


app = Flask(__name__)

# FORMULARIO --> RESPUESTA
def api_chatgpt(api_key, genero, edad, peso, agua, enfermedad, medicacion, actividad, sol):
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
    respuesta = api_chatgpt()
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
    temperatura = api_openweather()
    return jsonify(temperatura)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)