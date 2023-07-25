import openai

def golpe_calor(api_key, genero, edad, peso, agua, enfermedad, medicacion, actividad, sol):

    try:

        openai.api_key = api_key

        prompt = f"Soy de género {genero}. Tengo {edad} años. Peso {peso} kilos. Bebo agua {agua}. {enfermedad} tengo enfermedad preexistente. {medicacion} tomo medicación. Realizo {actividad} actividad física. Estoy expuesto al sol {sol}." \
                "Quiero que según mis datos, me hagas un análisis personalizado de entre 50 y 100 caracteres, sobre la probabilidad que tengo de sufrir un golpe de calor. Usa un lenguaje formal."
        
        completion = openai.Completion.create(engine='text-davinci-003',
                                            prompt=prompt,
                                            max_tokens=2048)
        return print(completion.choices[0].text)
    
    except Exception as e:

        return print("ERROR")