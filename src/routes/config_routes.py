from flask import Blueprint, jsonify
from src.config.config import config 

# Define the Blueprint for config routes
config_routes = Blueprint('config_routes', __name__)

# GET /api/config - Return the current configuration as JSON
@config_routes.route('/', methods=['GET'])
def get_config():
    try:
        # Convert the config object to a dictionary and return it as JSON
        config_dict = {
            "port": config.get_port(),
            "curriculum_collection_name": config.get_curriculum_collection_name(),
            "topics_collection_name": config.get_topics_collection_name(),
            "paths_collection_name": config.get_paths_collection_name(),
            "version_collection_name": config.get_version_collection_name(),
            "enumerators_collection_name": config.get_enumerators_collection_name(),
            "config_folder": config.get_config_folder(),
            "connection_string": config.get_connection_string(),
            "db_name": config.get_db_name(),
        }
        return jsonify(config_dict), 200
    except Exception as e:
        return jsonify({"error": "A processing error occurred"}), 500