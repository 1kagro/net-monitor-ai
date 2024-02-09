import time
import random
from bson import json_util
from flask import Response
from config.mongodb import mongo

def create_traffic():
    transmitted_data = random.uniform(100, 500) # Transmitted data in MB
    received_data = random.uniform(100, 500) # Received data in MB
    transmitted_packets = random.randint(8000, 12000)
    lost_packets = random.randint(0, 100)
    
    packet_loss = (lost_packets / transmitted_packets) * 100 if transmitted_packets > 0 else 0
    
    timestamp = int(time.time())
    data = {
        'transmitted_data': transmitted_data,
        'received_data': received_data,
        'bandwidth': random.uniform(50, 200), # Bandwidth in Mbps
        'transmitted_packets': transmitted_packets,
        'lost_packets': lost_packets,
        'packet_loss': packet_loss,
        'timestamp': timestamp
    }
    mongo.db.traffic.insert_one(data)
    
    return {
        'success': True,
        'message': 'Traffic data created successfully',
    }

def get_traffic(limit=10):
    traffic = list(mongo.db.traffic.find().sort('timestamp', -1).limit(limit))
    traffic = json_util.dumps(traffic)
    # print(traffic)
    return Response(traffic, mimetype='application/json')

def create_alert(alert):
    alert['timestamp'] = int(time.time())
    mongo.db.alerts.insert_one(alert)
    
    return {
        'success': True,
        'message': 'Alert created successfully',
    }

def get_alerts(limit=10):
    alerts = list(mongo.db.alerts.find().sort('timestamp', -1).limit(limit))
    alerts = json_util.dumps(alerts)
    # print(alerts)
    return Response(alerts, mimetype='application/json')