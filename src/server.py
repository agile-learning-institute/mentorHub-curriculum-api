import sys
import atexit
import signal
from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from config.config import config
from routes.curriculum_routes import create_curriculum_routes
from routes.config_routes import create_config_routes
from utils.mongo_io import MongoIO

app = Flask(__name__)
mongo = None

# Initilize Configuration
mongo = MongoIO()
mongo.connect()
mongo.load_versions()
mongo.load_enumerators()
        
# Apply Prometheus monitoring middleware
metrics = PrometheusMetrics(app, path='/api/health/')
metrics.info('app_info', 'Application info', version=config.api_version)

# Initilize Route Handlers
config_handler = create_config_routes()
curriculum_handler = create_curriculum_routes(mongo)
        
# Register routes
app.register_blueprint(curriculum_handler, url_prefix='/api/curriculum')
app.register_blueprint(config_handler, url_prefix='/api/config')

# Expose the app object for Gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.get_port())