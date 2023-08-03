def diagnostico(nombre, edad, peso, altura, vasos_agua, enfermedad=False, actividad_fisica=""):
    grupo_edad = ""
    imc = peso / (altura ** 2)
    estado_salud = ""
    hidratacion = ""
    advertencia_golpe_calor = ""
    advertencia_actividad = ""

    if edad < 18:
        grupo_edad = "joven"
    elif edad < 60:
        grupo_edad = "adulta"
    else:
        grupo_edad = "mayor"
    
    if imc < 18.5:
        estado_salud = "en bajo peso"
    elif imc < 24.9:
        estado_salud = "en un peso normal"
    elif imc < 30.0:
        estado_salud = "en sobrepeso"
    else:
        estado_salud = "en obesidad"
    
    if vasos_agua < 8:
        hidratacion = "Recuerda hidratarte más, estás bebiendo menos agua de lo recomendado."
    else:
        hidratacion = "Te estás hidratando adecuadamente."
    
    if enfermedad:
        advertencia_golpe_calor = "Debido a tu enfermedad, ten cuidado, ya que estás en mayor riesgo de sufrir un golpe de calor."
    elif not enfermedad:
        advertencia_golpe_calor = "Aunque no padeces ninguna enfermedad, existe el riesgo de que sufras un golpe de calor."

    if actividad_fisica.lower() == "mucho":
        advertencia_actividad = "Y dado que haces mucho ejercicio, asegúrate de hacerlo en las horas más frescas del día, como la mañana temprano o la noche, y asegúrate de beber agua adicional."
    elif actividad_fisica.lower() == "poco":
        advertencia_actividad = "Y aunque tu actividad física es baja, es esencial evitar el calor excesivo permaneciendo en la sombra o en interiores con aire acondicionado."

    mensaje = f"Hola {nombre}, eres una persona {grupo_edad} y te encuentras {estado_salud}. {hidratacion} {advertencia_golpe_calor} {advertencia_actividad}"
    return mensaje
