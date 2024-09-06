import json
import logging

from src.utils.mongo_io import MongoIO
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from flask import Blueprint, Response, jsonify, request
from src.config.config import config 

# Define the Blueprint for config routes
def create_path_routes():
    path_routes = Blueprint('path_routes', __name__)

    # GET /api/path - Return a list of paths that match query
    @path_routes.route('', methods=['GET'])
    def get_path():
        try:
            # Get the paths
            mongo_io = MongoIO()
            query = request.args.get('query') or ""
            paths = mongo_io.get_paths(query)
            return jsonify(paths), 200
        except Exception as e:
            logger.warn(f"Get Config Error has occured: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return path_routes