from flask import Blueprint, request, jsonify
from werkzeug.exceptions import InternalServerError

def create_curriculum_routes(mongo_io):
    # Define the Blueprint
    curriculum_routes = Blueprint('curriculum_routes', __name__)

    # GET /api/curriculum/{id} - Get or create a curriculum
    @curriculum_routes.route('/<string:id>', methods=['GET'])
    def get_or_create_curriculum(id):
        try:
            # Call service to get or create the curriculum by ID
            curriculum = mongo_io.get_or_create_curriculum(id)
            return jsonify(curriculum), 200
        except Exception as e:
            # Handle the error and return a 500 status code
            return jsonify({"error": "A processing error occurred"}), 500

    # POST /api/curriculum/{id} - Add a Resource to a curriculum
    @curriculum_routes.route('/<string:id>', methods=['POST'])
    def add_resource_to_curriculum(id):
        try:
            resource_data = request.get_json()
            # Call service to add the resource to the curriculum
            resource = mongo_io.add_resource_to_curriculum(id, resource_data)
            return jsonify(resource), 200
        except Exception as e:
            # Handle the error and return a 500 status code
            return jsonify({"error": "A processing error occurred"}), 500

    # PATCH /api/curriculum/{id}/{seq} - Update an existing curriculum
    @curriculum_routes.route('/<string:id>/<int:seq>', methods=['PATCH'])
    def update_curriculum(id, seq):
        try:
            resource_data = request.get_json()
            # Call service to update the curriculum resource
            updated_resource = mongo_io.update_curriculum(id, seq, resource_data)
            return jsonify(updated_resource), 200
        except Exception as e:
            # Handle the error and return a 500 status code
            return jsonify({"error": "A processing error occurred"}), 500

    # DELETE /api/curriculum/{id}/{seq} - Delete a Resource from a curriculum
    @curriculum_routes.route('/<string:id>/<int:seq>', methods=['DELETE'])
    def delete_resource_from_curriculum(id, seq):
        try:
            # Call service to delete the resource from the curriculum
            mongo_io.delete_resource_from_curriculum(id, seq)
            return '', 204  # No content response
        except Exception as e:
            # Handle the error and return a 500 status code
            return jsonify({"error": "A processing error occurred"}), 500