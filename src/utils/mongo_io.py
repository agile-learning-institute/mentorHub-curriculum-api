import sys
import logging
from pymongo import MongoClient
from src.config.config import config

logger = logging.getLogger(__name__)

class MongoIO:
    def __init__(self):
        self.client = None
        self.db = None
        self.versions = None
        self.enumerators = None

    def connect(self):
        """Connect to MongoDB."""
        try:
            self.client = MongoClient(config.get_connection_string())
            self.db = self.client.get_database(config.get_db_name())
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.fatal(f"Failed to connect to MongoDB: {e} - exiting")
            sys.exit(1)

    def disconnect(self):
        """Disconnect from MongoDB."""
        try:
            self.client.close()
            logger.info("Disconnected from MongoDB")
        except Exception as e:
            logger.fatal(f"Failed to disconnect to MongoDB: {e} - exiting")
            sys.exit(1)

    def load_versions(self):
        """Load the versions collection into memory."""
        try:
            config.versions = [];
        except Exception as e:
            logger.fatal(f"Failed to get or load versions: {e} - exiting")
            sys.exit(1)

    def load_enumerators(self):
        """Load the enumerators collection into memory."""
        try:
            config.enumerators = {};
        except Exception as e:
            logger.fatal(f"Failed to get or load enumerators: {e} - exiting")
            sys.exit(1)

    def get_or_create_curriculum(self, curriculum_id):
        """Retrieve or create a curriculum by ID."""
        try:
            result = {"method": "get_or_create_curriculum"};
            return result
        except Exception as e:
            logger.error(f"Failed to get or create curriculum: {e}")
            raise

    def add_resource_to_curriculum(self, curriculum_id, resource_data):
        """Add a new resource to the curriculum."""
        try:
            result = {"method": "add_resource_to_curriculum"};
            return result
        except Exception as e:
            logger.error(f"Failed to add resource to curriculum: {e}")
            raise

    def update_curriculum(self, curriculum_id, seq, resource_data):
        """Update a specific resource in the curriculum."""
        try:
            result = {"method": "update_curriculum"};
            return result
        except Exception as e:
            logger.error(f"Failed to update resource in curriculum: {e}")
            raise

    def delete_resource_from_curriculum(self, curriculum_id, seq):
        """Delete a specific resource from the curriculum."""
        try:
            result = {"method": "delete_resource_from_curriculum"};
            return result
        except Exception as e:
            logger.error(f"Failed to delete resource from curriculum: {e}")
            raise