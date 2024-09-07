from flask import Blueprint, request, jsonify
from src.models.token import create_token
from src.services.curriculum_services import CurriculumService
from src.models.breadcrumb import create_breadcrumb

import logging
logger = logging.getLogger(__name__)

def create_curriculum_routes():
    # Define the Blueprint
    curriculum_routes = Blueprint('curriculum_routes', __name__)

    # GET /api/curriculum/{id}/ - Get or create a curriculum
    @curriculum_routes.route('/<string:id>', methods=['GET'])
    def get_or_create_curriculum(id):
        try:
            breadcrumb = create_breadcrumb()
            token = create_token()
            curriculum = CurriculumService.get_or_create_curriculum(id, token, breadcrumb)
            logger.info(f"Get Curriculum Successful {breadcrumb}")
            return jsonify(curriculum), 200
        except Exception as e:
            logger.warn(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # PATCH /api/curriculum/{id} - Update a curriculum
    @curriculum_routes.route('/<string:id>', methods=['PATCH'])
    def update_curriculum(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb()
            patch_data = request.get_json()
            curriculum = CurriculumService.update_curriculum(id, patch_data, token, breadcrumb)
            logger.info(f"Update Curriculum Successful {breadcrumb}")
            return jsonify(curriculum), 200
        except Exception as e:
            logger.warn(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # DELETE /api/curriculum/{id} - Delete a curriculum
    @curriculum_routes.route('/<string:id>', methods=['DELETE'])
    def delete_curriculum(id):
        try:
            token = create_token()
            CurriculumService.delete_curriculum(id, token)
            logger.info(f"Delete Curriculum Successful")
            return jsonify({"result": "Success"}), 200
        except Exception as e:
            logger.warn(f"Error during Delete {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # PATCH /api/curriculum/{id}/assign/{link} - Move a resource from Next to Now
    @curriculum_routes.route('/<string:id>/assign/<string:link>', methods=['PATCH'])
    def assign_resource(id, link):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb()
            curriculum = CurriculumService.assign_resource(id, link, token, breadcrumb)
            logger.info(f"Assign Resource Successful {breadcrumb}")
            return jsonify(curriculum), 200
        except Exception as e:
            logger.warn(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # PATCH /api/curriculum/{id}/complete/{link} - Move a resource from Now to Complete
    @curriculum_routes.route('/<string:id>/complete/<string:link>', methods=['PATCH'])
    def complete_resource(id, link):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb()
            review = request.get_json(silent=True) or {}
            curriculum = CurriculumService.complete_resource(id, link, review, token, breadcrumb)
            logger.info(f"Complete Resource Successful {breadcrumb}")
            return jsonify(curriculum), 200
        except Exception as e:
            logger.warn(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/curriculum/{curriculum_id}/path/{path_id} - Add a path to Next
    @curriculum_routes.route('/<string:curriculum_id>/path/<string:path_id>', methods=['POST'])
    def add_path(curriculum_id, path_id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb()
            curriculum = CurriculumService.add_path(curriculum_id, path_id, token, breadcrumb)
            logger.info(f"Add Path Successful {breadcrumb}")
            return jsonify(curriculum), 200
        except Exception as e:
            logger.warn(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return curriculum_routes