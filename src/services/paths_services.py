from pymongo import ASCENDING
from mentorhub_utils import mentorhub_mongoIO
from mentorhub_config.MentorHub_Config import MentorHub_Config

import logging
logger = logging.getLogger(__name__)

class PathsService:

    @staticmethod 
    def _check_user_access(token):
        """Role Based Access Control logic"""
        # everyone can read all paths
        return

    @staticmethod
    def get_paths(query, token):
        """Get a list of paths that match query"""
        config = MentorHub_Config.get_instance()
        PathsService._check_user_access(token)

        match = {"name": {"$regex": query}}
        order = [('name', ASCENDING)]
        project = {"_id":1,"name":1}
        paths = mentorhub_mongoIO.get_documents(config.PATHS_COLLECTION_NAME, match, project, order)
        return paths

    @staticmethod
    def get_path(path_id, token):
        """Get the specified path"""
        config = MentorHub_Config.get_instance()
        PathsService._check_user_access(token)

        path = mentorhub_mongoIO.get_document(config.PATHS_COLLECTION_NAME, path_id)
        return path
