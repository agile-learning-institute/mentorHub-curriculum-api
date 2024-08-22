import sys
import logging
from pymongo import MongoClient
from src.config.config import config

logger = logging.getLogger(__name__)

class MongoIO:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MongoIO, cls).__new__(cls, *args, **kwargs)
            cls._instance._connect()
            cls._instance._load_versions()
            cls._instance._load_enumerators()
        return cls._instance
    
    def _connect(self):
        """Connect to MongoDB."""
        try:
            self.client = MongoClient(config.get_connection_string())
            self.db = self.client.get_database(config.get_db_name())
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.fatal(f"Failed to connect to MongoDB: {e} - exiting")
            sys.exit(1)

    def _load_versions(self):
        """Load the versions collection into memory."""
        try:
            config.versions = []  # Assuming this is correct
        except Exception as e:
            logger.fatal(f"Failed to get or load versions: {e} - exiting")
            sys.exit(1)

    def _load_enumerators(self):
        """Load the enumerators collection into memory."""
        try:
            config.enumerators = {}  # Assuming this is correct
        except Exception as e:
            logger.fatal(f"Failed to get or load enumerators: {e} - exiting")
            sys.exit(1)
    
    def disconnect(self):
        """Disconnect from MongoDB."""
        try:
            self.client.close()
            logger.info("Disconnected from MongoDB")
        except Exception as e:
            logger.fatal(f"Failed to disconnect from MongoDB: {e} - exiting")
            sys.exit(1)

    def get_curriculum(self, curriculum_id):
        """Retrieve a curriculum by ID."""
        try:
            result = {"method": "get_curriculum"}
            return result
        except Exception as e:
            logger.error(f"Failed to get curriculum: {e}")
            raise

    def create_curriculum(self, curriculum_id):
        """Create a curriculum by ID."""
        try:
            result = {"method": "create_curriculum"}
            return result
        except Exception as e:
            logger.error(f"Failed to create curriculum: {e}")
            raise

    def add_resource_to_curriculum(self, curriculum_id, resource_data):
        """Add a new resource to the curriculum."""
        try:
            result = {"method": "add_resource_to_curriculum"}
            return result
        except Exception as e:
            logger.error(f"Failed to add resource to curriculum: {e}")
            raise

    def update_curriculum(self, curriculum_id, seq, resource_data):
        """Update a specific resource in the curriculum."""
        try:
            result = {"method": "update_curriculum"}
            return result
        except Exception as e:
            logger.error(f"Failed to update resource in curriculum: {e}")
            raise

    def delete_resource_from_curriculum(self, curriculum_id, seq):
        """Delete a specific resource from the curriculum."""
        try:
            result = {"method": "delete_resource_from_curriculum"}
            return result
        except Exception as e:
            logger.error(f"Failed to delete resource from curriculum: {e}")
            raise
        
    # Singleton Getter
    @staticmethod
    def get_instance():
        """Get the singleton instance of the MongoIO class."""
        if MongoIO._instance is None:
            MongoIO()  # This calls the __new__ method and initializes the instance
        return MongoIO._instance
        
# Create a singleton instance of MongoIO
mongoIO = MongoIO.get_instance()