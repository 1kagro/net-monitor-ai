import requests
import threading
import time


alerts_data = {
    "number": 0,
    "details": []
}


def fetch_alerts():
    global alerts_data

    while True:
        try:
            # Consumir la API externa
            response = requests.get("http://localhost:5000/network/alerts/get")
            data = response.json()

            # Actualizar los datos de alertas
            alerts_data["number"] = len(data)
            alerts_data["details"] = data

            # Esperar 2 minutos antes de la próxima actualización
            time.sleep(120)

        except Exception as e:
            print(f"Error al obtener datos de la API: {e}")
            # Esperar 1 minuto antes de volver a intentar en caso de error
            time.sleep(60)


# Iniciar el hilo para la obtención periódica de alertas
thread = threading.Thread(target=fetch_alerts)
thread.daemon = True
thread.start()
