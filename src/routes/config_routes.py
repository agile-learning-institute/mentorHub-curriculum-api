from flask import Blueprint, jsonify
from src.config.config import config 

# Define the Blueprint for config routes
def create_config_routes():
    config_routes = Blueprint('config_routes', __name__)

    # GET /api/config - Return the current configuration as JSON
    @config_routes.route('/', methods=['GET'])
    def get_config():
        try:
            # Return the JSON representation of the config object
            return jsonify(config.to_dict()), 200
        except Exception as e:
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return config_routes        