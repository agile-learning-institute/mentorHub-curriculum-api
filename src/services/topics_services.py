from pymongo import ASCENDING
from src.utils.mentorhub_mongo_io import mentorhub_mongoIO
from mentorhub_config.MentorHub_Config import MentorHub_Config

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
        config = MentorHub_Config.get_instance()
        TopicService._check_user_access(token)

        match = {"name": {"$regex": query}}
        order = [('name', ASCENDING)]
        project = {"_id":1,"name":1}
        topics = mentorhub_mongoIO.get_documents(config.TOPICS_COLLECTION_NAME, match, project, order)
        return topics

    @staticmethod
    def get_topic(path_id, token):
        """Get the specified path"""
        config = MentorHub_Config.get_instance()
        TopicService._check_user_access(token)

        topic = mentorhub_mongoIO.get_document(config.TOPICS_COLLECTION_NAME, path_id)
        return topic
