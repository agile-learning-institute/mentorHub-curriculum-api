from flask import Flask, request, jsonify
import atexit
import signal
from prometheus_flask_exporter import PrometheusMetrics
from src.config.config import config
from routes.curriculum_routes import create_curriculum_routes
from routes.config_routes import config_routes
from src.utils.mongo_io import MongoIO

class Server:
    def __init__(self, mongo_io):
        self.mongo_io = mongo_io
        self.app = Flask(__name__)
        self.server = None

    def serve(self):
        # Initialize Flask app
        app = self.app

        # Apply Prometheus monitoring middleware
        metrics = PrometheusMetrics(app)
        metrics.info('app_info', 'Application info', version='1.0')

        # Register routes
        self.app.register_blueprint(create_curriculum_routes(self.mongo_io), url_prefix='/api/curriculum')
        app.register_blueprint(config_routes, url_prefix='/api/config')

        # Start Server
        port = config.get_port()
        self.server = app.run(host='0.0.0.0', port=port)
        print(f"Server running on port {port}")

        # Register exit handler
        print("Registering Exit Handler")
        atexit.register(self.on_exit_handler)
        signal.signal(signal.SIGTERM, lambda sig, frame: self.on_exit_handler())
        signal.signal(signal.SIGINT, lambda sig, frame: self.on_exit_handler())
        signal.signal(signal.SIGUSR1, lambda sig, frame: self.on_exit_handler())
        signal.signal(signal.SIGUSR2, lambda sig, frame: self.on_exit_handler())
        signal.signal(signal.SIGTERM, lambda sig, frame: self.on_exit_handler())
        signal.signal(signal.SIGINT, lambda sig, frame: self.on_exit_handler())

    def on_exit_handler(self):
        print('Server is shutting down...')
        if self.server:
            print('HTTP server closed.')
        self.mongo_io.disconnect()
        print('MongoDB connection closed.')
        exit()

# Start the server
if __name__ == "__main__":
    mongo = MongoIO()
    mongo.connect()
    mongo.load_versions()
    mongo.load_enumerators(config.get_curriculum_collection_name())
    server = Server(mongo)
    server.serve()