from flask import Flask, render_template
from dotenv import load_dotenv
import os

from config.mongodb import mongo
from routes.traffic import traffic

load_dotenv()

app = Flask(__name__)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)

# fetch_alerts()

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(traffic, url_prefix='/network')



if __name__ == '__main__':
    app.run(debug=True)