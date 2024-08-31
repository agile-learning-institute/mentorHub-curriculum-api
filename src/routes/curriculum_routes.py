from flask import Blueprint, request, jsonify
from src.services.curriculum_services import CurriculumService
from src.models.breadcrumb import create_breadcrumb

import logging
logger = logging.getLogger(__name__)

def create_curriculum_routes():
    # Define the Blueprint
    curriculum_routes = Blueprint('curriculum_routes', __name__)

    # GET /api/curriculum/{id}/ - Get or create a curriculum
    @curriculum_routes.route('/<string:id>/', methods=['GET'])
    def get_or_create_curriculum(id):
        try:
            curriculum = CurriculumService.get_or_create_curriculum(id)
            return jsonify(curriculum), 200
        except Exception as e:
            logger.warn(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # POST /api/curriculum/{id}/ - Add a Resource to a curriculum
    @curriculum_routes.route('/<string:id>/', methods=['POST'])
    def add_resource_to_curriculum(id):
        try:
            resource_data = request.get_json()
            breadcrumb = create_breadcrumb()
            resource = CurriculumService.add_resource_to_curriculum(id, resource_data, breadcrumb)
            return jsonify(resource), 200
        except Exception as e:
            logger.warn(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # PATCH /api/curriculum/{id}/{seq}/ - Update an existing curriculum
    @curriculum_routes.route('/<string:id>/<int:seq>/', methods=['PATCH'])
    def update_curriculum(id, seq):
        try:
            resource_data = request.get_json()
            breadcrumb = create_breadcrumb()
            updated_resource = CurriculumService.update_curriculum(id, seq, resource_data, breadcrumb)
            return jsonify(updated_resource), 200
        except Exception as e:
            logger.warn(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # DELETE /api/curriculum/{id}/{seq}/ - Delete a Resource from a curriculum
    @curriculum_routes.route('/<string:id>/<int:seq>/', methods=['DELETE'])
    def delete_resource_from_curriculum(id, seq):
        try:
            breadcrumb = create_breadcrumb()
            CurriculumService.delete_resource_from_curriculum(id, seq, breadcrumb)
            return '', 204  # No content response
        except Exception as e:
            logger.warn(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return curriculum_routes