from flask import Flask, request, jsonify
import atexit
import signal
from prometheus_flask_exporter import PrometheusMetrics
from config.config import config
from routes.curriculum_routes import create_curriculum_routes
from routes.config_routes import create_config_routes
from utils.mongo_io import MongoIO

class Server:
    def __init__(self, mongo_io):
        self.mongo_io = mongo_io
        self.app = Flask(__name__)
        self.server = None

    def serve(self):
        # Initialize Flask app
        app = self.app

        # Apply Prometheus monitoring middleware
        metrics = PrometheusMetrics(self.app, path='/api/health/')
        metrics.info('app_info', 'Application info', version=config.api_version)

        # Initilize Route Handlers
        config_handler = create_config_routes()
        curriculum_handler = create_curriculum_routes(self.mongo_io)
        
        # Register routes
        self.app.register_blueprint(curriculum_handler, url_prefix='/api/curriculum')
        self.app.register_blueprint(config_handler, url_prefix='/api/config')

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
    try:
        mongo = MongoIO()
        mongo.connect()
        mongo.load_versions()
        mongo.load_enumerators()
        server = Server(mongo)
        server.serve()
    except Exception as e:
        print(f"Server Failed!: {e}")