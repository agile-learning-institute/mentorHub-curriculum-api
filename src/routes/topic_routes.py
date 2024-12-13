import json
import logging

from src.utils.mongo_io import MongoIO
logging.basicConfig(level=logging.INFO)
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
            mongo_io = MongoIO()
            query = request.args.get('query') or ""
            topics = mongo_io.get_topics(query)
            logger.info(f"Get Topics Success")
            return jsonify(topics), 200
        except Exception as e:
            logger.warn(f"Get Topic Error has occured: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # GET /api/topic/{id} - Return a list of topics that match query
    @topic_routes.route('/<string:id>', methods=['GET'])
    def get_topic(id):
        try:
            # Get the topic
            mongo_io = MongoIO()
            topic = mongo_io.get_topic(id)
            logger.info(f"Get Topic Success")
            return jsonify(topic), 200
        except Exception as e:
            logger.warn(f"Get Topic Error has occured: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return topic_routes