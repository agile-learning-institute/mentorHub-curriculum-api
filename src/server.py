# Initilize Logging
import logging

from src.routes.path_routes import create_path_routes
from src.routes.topic_routes import create_topic_routes
from src.utils.ejson_encoder import MongoJSONEncoder
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import sys
import signal
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from src.config.config import config
from src.utils.mongo_io import MongoIO
from src.routes.curriculum_routes import create_curriculum_routes
from src.routes.config_routes import create_config_routes

# Initilize Flask App
app = Flask(__name__)
app.json = MongoJSONEncoder(app)

# Initialize Database Connection, and load one-time data
mongo = MongoIO()
mongo.initialize()

# Apply Prometheus monitoring middleware
metrics = PrometheusMetrics(app, path='/api/health/')
metrics.info('app_info', 'Application info', version=config.api_version)

# Initialize Route Handlers
config_handler = create_config_routes()
curriculum_handler = create_curriculum_routes()
path_handler = create_path_routes()
topic_handler = create_topic_routes()

# Register routes
app.register_blueprint(curriculum_handler, url_prefix='/api/curriculum')
app.register_blueprint(path_handler, url_prefix='/api/path')
app.register_blueprint(topic_handler, url_prefix='/api/topic')
app.register_blueprint(config_handler, url_prefix='/api/config')

# Define a signal handler for SIGTERM and SIGINT
def handle_exit(signum, frame):
    logger.info(f"Received signal {signum}. Initiating shutdown...")
    mongo.disconnect()
    logger.info('MongoDB connection closed.')
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

# Expose the app object for Gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.get_port())