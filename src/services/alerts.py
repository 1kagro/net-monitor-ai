import numpy as np
import requests

def check_bandwidth_overload(avg_bandwidth, threshold_bandwidth):
    if avg_bandwidth > threshold_bandwidth:
        return True, "Alerta: La velocidad promedio del ancho de banda ha superado el umbral. Posible riesgo de sobrecarga en la red."
    else:
        return False, ""


def check_packet_loss_overload(avg_packet_loss, threshold_packet_loss):
    if avg_packet_loss > threshold_packet_loss:
        return True, "Alerta: La tasa promedio de pérdida de paquetes es alta. Posible congestión en la red. Verificar el estado de la red."
    else:
        return False, ""


def check_bandwidth_variation(stdev_bandwidth, threshold_bandwidth_variation):
    if stdev_bandwidth > threshold_bandwidth_variation:
        return True, "Alerta: La variación en el ancho de banda es elevada. Posibles problemas de estabilidad en la red. Monitorear de cerca."
    else:
        return False, ""

def insert_alert(alert):
    requests.post("http://localhost:5000/network/alerts/create", json=alert)


data = requests.get("http://localhost:5000/network/get").json()

avg_bandwidth = sum(entry["bandwidth"] for entry in data) / len(data)
avg_packet_loss = sum(entry["packet_loss"] for entry in data) / len(data)
stdev_bandwidth = np.std([entry["bandwidth"] for entry in data])

threshold_bandwidth = 150
threshold_packet_loss = 0.5
threshold_bandwidth_variation = 10

# Verificar sobrecarga y generar alertas
bandwidth_overload, alert_bandwidth = check_bandwidth_overload(
    avg_bandwidth, threshold_bandwidth)
packet_loss_overload, alert_packet_loss = check_packet_loss_overload(
    avg_packet_loss, threshold_packet_loss)
bandwidth_variation_overload, alert_bandwidth_variation = check_bandwidth_variation(
    stdev_bandwidth, threshold_bandwidth_variation)

# Mostrar alertas
if bandwidth_overload:
    insert_alert({
        "message": alert_bandwidth
    })
    print(alert_bandwidth)

if packet_loss_overload:
    insert_alert({
        "message": alert_packet_loss
    })
    print(alert_packet_loss)

if bandwidth_variation_overload:
    insert_alert({
        "message": alert_bandwidth_variation
    })
    print(alert_bandwidth_variation)

