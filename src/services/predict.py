# import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

data = [
    {
        "_id": {
            "$oid": "6567f19424bf417be3c7ebf6"
        },
        "transmitted_data": 246.94456434210164,
        "received_data": 290.17393800268144,
        "bandwidth": 130.19618572020858,
        "transmitted_packets": 10185,
        "lost_packets": 0,
        "packet_loss": 0.0,
        "timestamp": 1701310868
    },
    {
        "_id": {
            "$oid": "6567f19424bf417be3c7ebf8"
        },
        "transmitted_data": 214.27263845608212,
        "received_data": 488.2533614731509,
        "bandwidth": 168.57402127544265,
        "transmitted_packets": 10511,
        "lost_packets": 100,
        "packet_loss": 0.9513842641042717,
        "timestamp": 1701310868
    },
    {
        "_id": {
            "$oid": "6567f19424bf417be3c7ebf7"
        },
        "transmitted_data": 399.37751468184103,
        "received_data": 261.3819337291829,
        "bandwidth": 105.61644995351332,
        "transmitted_packets": 10822,
        "lost_packets": 4,
        "packet_loss": 0.036961744594344856,
        "timestamp": 1701310868
    },
    {
        "_id": {
            "$oid": "6567f19424bf417be3c7ebfa"
        },
        "transmitted_data": 364.89400929878053,
        "received_data": 447.4937023508901,
        "bandwidth": 140.0062722341167,
        "transmitted_packets": 8595,
        "lost_packets": 75,
        "packet_loss": 0.8726003490401396,
        "timestamp": 1701310868
    },
    {
        "_id": {
            "$oid": "6567f19424bf417be3c7ebf9"
        },
        "transmitted_data": 349.5815859971011,
        "received_data": 446.1993307494696,
        "bandwidth": 87.41293977557393,
        "transmitted_packets": 9184,
        "lost_packets": 79,
        "packet_loss": 0.8601916376306621,
        "timestamp": 1701310868
    },
    {
        "_id": {
            "$oid": "6567f19324bf417be3c7ebf3"
        },
        "transmitted_data": 488.2528298285027,
        "received_data": 450.04383069551716,
        "bandwidth": 100.26172427866358,
        "transmitted_packets": 10952,
        "lost_packets": 62,
        "packet_loss": 0.5661066471877283,
        "timestamp": 1701310867
    },
    {
        "_id": {
            "$oid": "6567f19324bf417be3c7ebf2"
        },
        "transmitted_data": 270.8522478975207,
        "received_data": 343.28909611750845,
        "bandwidth": 197.2810910779067,
        "transmitted_packets": 11881,
        "lost_packets": 70,
        "packet_loss": 0.589175995286592,
        "timestamp": 1701310867
    },
    {
        "_id": {
            "$oid": "6567f19324bf417be3c7ebf1"
        },
        "transmitted_data": 366.6255534088843,
        "received_data": 294.2779361865961,
        "bandwidth": 165.69374827193136,
        "transmitted_packets": 9804,
        "lost_packets": 39,
        "packet_loss": 0.397796817625459,
        "timestamp": 1701310867
    },
    {
        "_id": {
            "$oid": "6567f19324bf417be3c7ebf5"
        },
        "transmitted_data": 279.28379596947536,
        "received_data": 131.9620701690646,
        "bandwidth": 69.58073722343565,
        "transmitted_packets": 8907,
        "lost_packets": 4,
        "packet_loss": 0.04490849893342315,
        "timestamp": 1701310867
    },
    {
        "_id": {
            "$oid": "6567f19324bf417be3c7ebf4"
        },
        "transmitted_data": 331.4054454376885,
        "received_data": 131.6239291813111,
        "bandwidth": 179.2273390734983,
        "transmitted_packets": 10904,
        "lost_packets": 37,
        "packet_loss": 0.3393250183418929,
        "timestamp": 1701310867
    }
]

# Transformar los datos en un DataFrame de Pandas
df = pd.DataFrame(data)

# Calcular la variación en el ancho de banda y la pérdida de paquetes
df['var_bandwidth'] = df['bandwidth'].diff()
df['var_packet_loss'] = df['packet_loss'].diff()

# Eliminar las filas con valores NaN resultantes de calcular la diferencia
df = df.dropna()

# Preparar los datos para el modelo
X = df[['var_bandwidth', 'var_packet_loss']]
y = df['bandwidth']  # o podrías usar 'packet_loss' según tus necesidades

# Escalar los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42)

# Construir el modelo de regresión lineal con TensorFlow y Keras
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(2,)),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

# Entrenar el modelo
model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0)

# Evaluar el modelo en el conjunto de prueba
y_pred = model.predict(X_test)

# Calcular el error cuadrático medio
mse = mean_squared_error(y_test, y_pred)
print(f'Error Cuadrático Medio en el conjunto de prueba: {mse}')
