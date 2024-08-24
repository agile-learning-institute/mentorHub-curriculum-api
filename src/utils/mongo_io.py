import logging
import sys
from datetime import datetime
from bson import ObjectId 
from pymongo import MongoClient
from src.config.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoIO:
    _instance = None

    def __new__(cls, *args, **kwargs):
        config.get_instance()   # Ensure the config is constructed first
        if cls._instance is None:
            cls._instance = super(MongoIO, cls).__new__(cls, *args, **kwargs)
            cls._instance.connected = False
            cls._instance.client = None
            cls._instance.db = None
        return cls._instance

    def initialize(self):
        """Initialize MongoDB connection and load configurations."""
        self._connect()
        self._load_versions()
        self._load_enumerators()

    def _connect(self):
        """Connect to MongoDB."""
        try:
            self.client = MongoClient(config.get_connection_string(), serverSelectionTimeoutMS=2000)
            self.client.admin.command('ping')  # Force connection
            self.db = self.client.get_database(config.get_db_name())
            self.connected = True
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.fatal(f"Failed to connect to MongoDB: {e} - exiting")
            sys.exit(1)

    def disconnect(self):
        """Disconnect from MongoDB."""
        if not self.connected: return
            
        try:
            if self.client:
                self.client.close()
                logger.info("Disconnected from MongoDB")
        except Exception as e:
            logger.fatal(f"Failed to disconnect from MongoDB: {e} - exiting")
            sys.exit(1)
      
    def _load_versions(self):
        """Load the versions collection into memory."""
        try:
            versions_collection = self.db.get_collection(config.get_version_collection_name())
            versions_cursor = versions_collection.find({})
            versions = list(versions_cursor) 
            config.versions = versions
            logger.info(f"{len(versions)} Versions Loaded.")
        except Exception as e:
            logger.fatal(f"Failed to get or load versions: {e} - exiting")
            sys.exit(1)

    def _load_enumerators(self):
        """Load the enumerators collection into memory."""
        if len(config.versions) == 0:
            logger.fatal("No Versions to load Enumerators from - exiting")
            sys.exit(1)
        
        try: 
            # Get the enumerators version from the curricumum version number.
            version_strings = [version['currentVersion'].split('.').pop() or "0" 
                            for version in config.versions 
                            if version['collectionName'] == config.get_curriculum_collection_name()]
            the_version_string = version_strings.pop() if version_strings else "0"
            the_version = int(the_version_string)

            # Query the database            
            enumerators_collection = self.db.get_collection(config.get_enumerators_collection_name())
            query = { "version": the_version }
            enumerations = enumerators_collection.find_one(query)
    
            # Fail Fast if not found - critical error
            if not enumerations:
                logger.fatal(f"Enumerators not found for version: {config.get_curriculum_collection_name()}:{the_version_string}")
                sys.exit(1)
    
            config.enumerators = enumerations['enumerators']
        except Exception as e:
            logger.fatal(f"Failed to get or load enumerators: {e} - exiting")
            sys.exit(1)

    def _stringify_mongo_types(self, document):
        """Recursively convert ObjectId and datetime values to strings in a dictionary."""
        if isinstance(document, dict):
            return {
                key: self._stringify_mongo_types(value) for key, value in document.items()
            }
        elif isinstance(document, list):
            return [self._stringify_mongo_types(item) for item in document]
        elif isinstance(document, ObjectId):
            return str(document)
        elif isinstance(document, datetime):
            return document.isoformat()
        else:
            return document        
    
    def get_curriculum(self, curriculum_id):
        """Retrieve a curriculum by ID."""
        if not self.connected:
            return None

        try:
            # Query Curriculum
            curriculum_object_id = ObjectId(curriculum_id)
            curriculum_collection = self.db.get_collection(config.get_curriculum_collection_name())
            curriculum = curriculum_collection.find_one({"_id": curriculum_object_id})
            
            # Stringify Object ID's and Dates
            curriculum = self._stringify_mongo_types(curriculum)
            return curriculum
        except Exception as e:
            logger.error(f"Failed to get curriculum: {e}")
            raise
    
    def create_curriculum(self, curriculum_id, curriculum_data):
        """Create a curriculum by ID."""
        if not self.connected: return None

        try:
            curriculum_collection = self.db.get_collection(config.get_curriculum_collection_name())
            result = curriculum_collection.insert_one(curriculum_data)
            return result.inserted_id
        except Exception as e:
            logger.error(f"Failed to create curriculum: {e}")
            raise

    def add_resource_to_curriculum(self, curriculum_id, resource_data):
        """Add a new resource to the curriculum."""
        if not self.connected: return None

        try:
            curriculum_collection = self.db.get_collection(config.get_curriculum_collection_name())
            result = curriculum_collection.update_one(
                {"curriculum_id": curriculum_id},
                {"$push": {"resources": resource_data}}
            )
            return result.modified_count
        except Exception as e:
            logger.error(f"Failed to add resource to curriculum: {e}")
            raise

    def update_curriculum(self, curriculum_id, seq, resource_data):
        """Update a specific resource in the curriculum."""
        if not self.connected: return None

        try:
            curriculum_collection = self.db.get_collection(config.get_curriculum_collection_name())
            result = curriculum_collection.update_one(
                {"curriculum_id": curriculum_id, "resources.seq": seq},
                {"$set": {"resources.$": resource_data}}
            )
            return result.modified_count
        except Exception as e:
            logger.error(f"Failed to update resource in curriculum: {e}")
            raise

    def delete_resource_from_curriculum(self, curriculum_id, seq):
        """Delete a specific resource from the curriculum."""
        if not self.connected: return None

        try:
            curriculum_collection = self.db.get_collection(config.get_curriculum_collection_name())
            result = curriculum_collection.update_one(
                {"curriculum_id": curriculum_id},
                {"$pull": {"resources": {"seq": seq}}}
            )
            return result.modified_count
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