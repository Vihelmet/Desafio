import openai


def api_chatgpt(api_key, nombre, genero, edad, altura, peso, agua, actividad, enfermedad):

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
        
        return print(completion.choices[0].text)
    
    except Exception as e:

        return print("Gracias por rellenar el formulario. Parece que estamos teniendo problemas técnicos. Vuelva a intentarlo más tarde, por favor.")