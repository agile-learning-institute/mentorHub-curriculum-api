from mentorhub_utils import create_breadcrumb, create_token
from src.services.topics_services import TopicService

import logging
logger = logging.getLogger(__name__)

from flask import Blueprint, Response, jsonify, request

# Define the Blueprint for config routes
def create_topic_routes():
    topic_routes = Blueprint('topic_routes', __name__)

    # GET /api/topic - Return a list of topics that match query
    @topic_routes.route('', methods=['GET'])
    def get_topics():
        try:
            # Get the topics
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            query = request.args.get('query') or ""
            topics = TopicService.get_topics(query, token)
            logger.info(f"Get Topics Success {breadcrumb}")
            return jsonify(topics), 200
        except Exception as e:
            logger.warning(f"Get Topic Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # GET /api/topic/{id} - Return a list of topics that match query
    @topic_routes.route('/<string:id>', methods=['GET'])
    def get_topic(id):
        try:
            # Get the topic
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            topic = TopicService.get_topic(id, token)
            logger.info(f"Get Topic Success {breadcrumb}")
            return jsonify(topic), 200
        except Exception as e:
            logger.warn(f"Get Topic Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return topic_routes