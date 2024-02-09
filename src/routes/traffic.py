from flask import Blueprint, request
from services.traffic import create_traffic, get_traffic, create_alert, get_alerts 

traffic = Blueprint('traffic', __name__)

@traffic.route('/', methods=['GET'])
def index():
    return 'Traffic index'

@traffic.route('/create', methods=['POST'])
def create():
    return create_traffic()

@traffic.route('/get', methods=['GET'])
def get():
    return get_traffic()

@traffic.route('/alerts/create', methods=['POST'])
def create_alert_():
    try:
        alert = request.json
        return create_alert(alert)
    except Exception as e:
        return {
            'success': False,
            'message': 'Error: {}'.format(e)
        }

@traffic.route('/alerts/get', methods=['GET'])
def get_alerts_():
    return get_alerts()