from src.utils import mentorhub_mongo_io
from src.config.Config import config

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
        PathsService._check_user_access(token)

        match = {} # Match all - Todo: Build match with query
        project = {"_id":1, "name": 1}
        paths = mentorhub_mongo_io.getDocuments(config.PATHS_COLLECTION_NAME, match, project)
        return paths

    @staticmethod
    def get_path(path_id, token):
        """Get the specified path"""
        PathsService._check_user_access(token)

        path = mentorhub_mongo_io.getDocument(config.PATHS_COLLECTION_NAME, path_id)
        return path
