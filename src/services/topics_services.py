from src.utils import mentorhub_mongo_io
from src.config.Config import config

import logging
logger = logging.getLogger(__name__)

class TopicService:

    @staticmethod 
    def _check_user_access(token):
        """Role Based Access Control logic"""
        # everyone can read all topics
        return

    @staticmethod
    def get_topics(query, token):
        """Get a list of topics that match query"""
        TopicService._check_user_access(token)

        match = {} # TODO: Build match from query
        project = {"_id":1,"name":1}
        topics = mentorhub_mongo_io.getDocuments(config.TOPICS_COLLECTION_NAME, match, project)
        return topics

    @staticmethod
    def get_topic(path_id, token):
        """Get the specified path"""
        TopicService._check_user_access(token)

        topic = mentorhub_mongo_io.getDocument(config.TOPICS_COLLECTION_NAME, path_id)
        return topic
