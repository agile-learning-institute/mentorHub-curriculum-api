import json
import logging

from mentorhub_flask_utils import create_breadcrumb, create_token
from src.services.paths_services import PathsService
logger = logging.getLogger(__name__)

from flask import Blueprint, Response, jsonify, request

# Define the Blueprint for config routes
def create_path_routes():
    path_routes = Blueprint('path_routes', __name__)

    # GET /api/path - Return a list of paths that match query
    @path_routes.route('', methods=['GET'])
    def get_paths():
        try:
            # Get the paths
            breadcrumb = create_breadcrumb()
            token = create_token()
            query = request.args.get('query') or ""
            paths = PathsService.get_paths(query, token)
            logger.info(f"Get Path Success {breadcrumb}")
            return jsonify(paths), 200
        except Exception as e:
            logger.warn(f"Get Path Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # GET /api/path/id - Return a specific path
    @path_routes.route('/<string:id>', methods=['GET'])
    def get_path(id):
        try:
            # Get the specified path
            breadcrumb = create_breadcrumb()
            token = create_token()
            path = PathsService.get_path(id, token)
            logger.info(f"Get Path Success {breadcrumb}")
            return jsonify(path), 200
        except Exception as e:
            logger.warn(f"Get Path Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # Ensure the Blueprint is returned correctly
    return path_routes