import random
import unicodedata
import json

# -------------------- Ejercicio 1: Implementar Niveles de Dificultad --------------------
def seleccionar_dificultad():
    print("Selecciona el nivel de dificultad:")
    print("1. Fácil (10 intentos)")
    print("2. Medio (7 intentos)")
    print("3. Difícil (5 intentos)")
    opcion = input("Introduce el número de la opción: ")

    if opcion == '1':
        return 10
    elif opcion == '2':
        return 7
    elif opcion == '3':
        return 5
    else:
        print("Opción no válida. Se asignará dificultad fácil por defecto.")
        return 10

# -------------------- Ejercicio 2: Mostrar Gráficamente el Ahorcado --------------------
def mostrar_ahorcado(intentos_fallidos):
    etapas = [
        """
           -----
           |   |
           |   O
           |  /|\\
           |  / \\
           |
        """,
        """
           -----
           |   |
           |   O
           |  /|\\
           |  /
           |
        """,
        """
           -----
           |   |
           |   O
           |  /|
           |
           |
        """,
        """
           -----
           |   |
           |   O
           |   |
           |
           |
        """,
        """
           -----
           |   |
           |   O
           |
           |
           |
        """,
        """
           -----
           |   |
           |
           |
           |
           |
        """,
        """
           -----
           |
           |
           |
           |
           |
        """
    ]
    print(etapas[intentos_fallidos])

# -------------------- Ejercicio 3: Soportar Palabras con Acentos y Caracteres Especiales --------------------
def normalizar(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

# -------------------- Ejercicio 4: Añadir Funcionalidad de Pistas --------------------
def dar_pista(palabra, letras_adivinadas):
    letras = [letra for letra in palabra if letra not in letras_adivinadas]
    if letras:
        letra_pista = random.choice(letras)
        print(f"Pista: una letra de la palabra es '{letra_pista}'.")
        return letra_pista
    return None

# -------------------- Ejercicio 5: Guardar y Cargar el Estado del Juego --------------------
def guardar_estado(estado, filename='estado.json'):
    with open(filename, 'w') as f:
        json.dump(estado, f)

def cargar_estado(filename='estado.json'):
    with open(filename, 'r') as f:
        return json.load(f)

# -------------------- Ejercicio 6: Implementar un Sistema de Puntuación --------------------
def calcular_puntuacion(intentos_restantes, longitud_palabra):
    return intentos_restantes * 10 + (longitud_palabra * 5)

# -------------------- Ejercicio 7: Agregar Funcionalidad para Jugar Nuevamente --------------------
def jugar_nuevamente():
    respuesta = input("¿Quieres jugar de nuevo? (s/n): ")
    return respuesta.lower() == 's'

# -------------------- Ejercicio 8: Registrar Historial de Partidas --------------------
def registrar_historial(palabra, resultado):
    with open('historial.txt', 'a') as f:
        f.write(f"{palabra} - {resultado}\n")

# -------------------- Ejercicio 9: Permitir Personalización del Juego --------------------
def personalizar_juego():
    nombre_jugador = input("Introduce tu nombre: ")
    tema_palabras = "Tema: Programación"  # Tema predefinido
    return nombre_jugador, tema_palabras

# -------------------- Función para cargar palabras desde un archivo --------------------
def cargar_palabras(filename='palabras.txt'):
    with open(filename, 'r') as f:
        palabras = [linea.strip() for linea in f if linea.strip()]
    return palabras

# -------------------- Ejercicio 10: Desarrollar Pruebas Unitarias para las Funciones --------------------
def pruebas_unitarias():
    assert normalizar("canción") == "cancion"
    assert calcular_puntuacion(5, 8) == 70
    print("Todas las pruebas unitarias pasaron.")

# -------------------- Juego Principal --------------------
def juego_ahorcado():
    print("¡Bienvenido al juego del Ahorcado!")
    intentos_restantes = seleccionar_dificultad()
    
    palabras = cargar_palabras()
    palabra = normalizar(random.choice(palabras))
    
    letras_adivinadas = set()
    intentos_fallidos = 0

    while intentos_restantes > 0:
        mostrar_ahorcado(intentos_fallidos)
        print(f"Letras adivinadas: {' '.join(sorted(letras_adivinadas))}")
        print(f"Intentos restantes: {intentos_restantes}")
        
        palabra_oculta = ''.join(letra if letra in letras_adivinadas else '_' for letra in palabra)
        print(f"Palabra: {palabra_oculta}")
        
        if set(palabra) <= letras_adivinadas:
            print(f"¡Felicidades! Adivinaste la palabra: {palabra}")
            registrar_historial(palabra, "Ganado")
            puntuacion = calcular_puntuacion(intentos_restantes, len(palabra))
            print(f"Tu puntuación: {puntuacion}")
            break  # Salir del bucle si se adivina la palabra
        
        letra = input("Adivina una letra o la palabra completa (o 'p' para una pista): ").strip().lower()
        
        if letra == 'p':
            letra_pista = dar_pista(palabra, letras_adivinadas)
            if letra_pista:
                letras_adivinadas.add(letra_pista)
                intentos_restantes -= 1
        elif len(letra) == 1:  # Si se adivina una letra
            if letra in letras_adivinadas:
                print("Ya has adivinado esa letra.")
            elif letra in palabra:
                letras_adivinadas.add(letra)
            else:
                intentos_fallidos += 1
                intentos_restantes -= 1
                print(f"Letra '{letra}' no está en la palabra.")
        elif letra == palabra:  # Si se adivina la palabra completa
            print(f"¡Felicidades! Adivinaste la palabra: {palabra}")
            registrar_historial(palabra, "Ganado")
            puntuacion = calcular_puntuacion(intentos_restantes, len(palabra))
            print(f"Tu puntuación: {puntuacion}")
            break
        else:
            intentos_fallidos += 1
            intentos_restantes -= 1
            print(f"La palabra '{letra}' no es correcta.")

    # Solo mostrar el mensaje de pérdida si no se ganó
    if set(palabra) > letras_adivinadas:
        mostrar_ahorcado(intentos_fallidos)
        print(f"Perdiste. La palabra era: {palabra}")
        registrar_historial(palabra, "Perdido")

if __name__ == "__main__":
    jugador, tema = personalizar_juego()
    print(f"Bienvenido {jugador}, has elegido el tema: {tema}")
    
    while True:
        juego_ahorcado()
        if not jugar_nuevamente():
            break

    pruebas_unitarias()
