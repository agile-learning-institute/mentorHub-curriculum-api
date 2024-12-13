import logging
import sys
from datetime import datetime
from bson import ObjectId 
from pymongo import MongoClient
from src.config.Config import config

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
            self.client = MongoClient(config.MONGO_CONNECTION_STRING, serverSelectionTimeoutMS=2000)
            self.client.admin.command('ping')  # Force connection
            self.db = self.client.get_database(config.MONGO_DB_NAME)
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
            versions_collection = self.db.get_collection(config.VERSION_COLLECTION_NAME)
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
                            if version['collectionName'] == config.CURRICULUM_COLLECTION_NAME]
            the_version_string = version_strings.pop() if version_strings else "0"
            the_version = int(the_version_string)

            # Query the database            
            enumerators_collection = self.db.get_collection(config.ENUMERATORS_COLLECTION_NAME)
            query = { "version": the_version }
            enumerations = enumerators_collection.find_one(query)
    
            # Fail Fast if not found - critical error
            if not enumerations:
                logger.fatal(f"Enumerators not found for version: {config.ENUMERATORS_COLLECTION_NAME}:{the_version_string}")
                sys.exit(1)
    
            config.enumerators = enumerations['enumerators']
        except Exception as e:
            logger.fatal(f"Failed to get or load enumerators: {e} - exiting")
            sys.exit(1)

    def get_mentor(self, person_id):
        """Get a person's mentor ID as a string"""
        if not self.connected:
            return None
        
        try:
            people = self.db.get_collection(config.PEOPLE_COLLECTION_NAME)
            person_object_id = ObjectId(person_id)
            person = people.find_one({ "_id": person_object_id })

            # Return the mentor_id or an empty string if not found
            mentor_id = person.get("mentorId", "") if person else ""
            return str(mentor_id)
        except Exception as e:
            logger.error(f"Failed to get person-mentor_id: {e}")
            raise
    
    def get_paths(self, query):
        """Get a list of paths"""
        if not self.connected:
            return None
        
        try:
            paths_collection = self.db.get_collection(config.PATHS_COLLECTION_NAME)
            pipeline = [
                {"$match": { "name": { "$regex": query, "$options": "i" }}},
                {"$project": {
                        "_id": { "$toString": "$_id" },
                        "name": 1  
                    }
                },
                {"$sort": { "name": 1}}
            ]
            results = list(paths_collection.aggregate(pipeline))
            return results
        except Exception as e:
            logger.error(f"Failed to get paths: {e}")
            raise
    
    def get_path(self, path_id):
        """Get a paths with topoic and resource data"""
        if not self.connected:
            return None
        
        try:
            # Get the path document
            paths_collection = self.db.get_collection(config.PATHS_COLLECTION_NAME)
            path_object_id = ObjectId(path_id)
            path = paths_collection.find_one({"_id": path_object_id})
            if not path: return {}

            # Could not get a 3-layer lookup to work, so doing it in 2 steps
            for segment in path.get("segments", []):
                for i, topic_id in enumerate(segment.get("topics", [])):
                    topic_data = self.get_topic(str(topic_id))  
                    segment["topics"][i] = topic_data  

            # Housekeep un-wanted properties
            del path["_id"]
            del path["status"]
            return path
        except Exception as e:
            logger.error(f"Failed to get path: {e}")
            raise
    
    def get_topics(self, query):
        """Get a list of topics"""
        if not self.connected:
            return None
        
        try:
            topics_collection = self.db.get_collection(config.TOPICS_COLLECTION_NAME)
            pipeline = [
                {"$match": { "name": { "$regex": query, "$options": "i" }}},
                {"$project": {
                        "_id": { "$toString": "$_id" },
                        "name": 1  
                    }
                },
                {"$sort": { "name": 1}}
            ]
            results = list(topics_collection.aggregate(pipeline))
            return results
        except Exception as e:
            logger.error(f"Failed to get paths: {e}")
            raise
    
    def get_topic(self, topic_id):
        """Get a list of topics"""
        if not self.connected:
            return None
        
        try:
            topics_collection = self.db.get_collection(config.TOPICS_COLLECTION_NAME)
            topic_object_id = ObjectId(topic_id)
            pipeline = [
                {
                    "$match": {"_id": topic_object_id}
                },
                {
                    "$project": {
                        "_id": 0,
                        "name": 1,
                        "resources": 1,
                        "skills": 1
                    }
                }
            ]
            
            # Get the Topic document
            topic = list(topics_collection.aggregate(pipeline))[0]
            
            # Replace Resource skill indexes with skill description
            for resource in topic['resources']:
                for index in range(len(resource['skills'])):
                    skill_index = resource["skills"][index]
                    resource["skills"][index] = topic['skills'][skill_index]['description']
                    
            # remove the topic skills property
            del topic['skills']
            
            return topic
        except Exception as e:
            logger.error(f"Failed to get paths: {e}")
            raise
    
    def get_curriculum(self, curriculum_id):
        """Retrieve a curriculum by ID."""
        if not self.connected:
            return None

        try:
            # Query Curriculum - Lookup resource name/link by resource_id
            paths_collection_name =  config.PATHS_COLLECTION_NAME
            curriculum_collection = self.db.get_collection(config.CURRICULUM_COLLECTION_NAME)
            curriculum_object_id = ObjectId(curriculum_id)

            pipeline = [
                {"$match": { "_id": curriculum_object_id }},
                {"$lookup": {  
                        "from": config.PATHS_COLLECTION_NAME,  
                        "localField": "later",  
                        "foreignField": "_id",  
                        "as": "later_paths"  
                }},
                {"$project": {  
                        "_id": 1,  
                        "completed": 1,
                        "now": 1,
                        "next": 1,
                        "lastSaved":1,
                        "later": {  
                            "$map": { 
                                "input": "$later_paths",
                                "as": "path",
                                "in": {
                                    "path_id": "$$path._id",
                                    "name": "$$path.name" 
                                }
                            }
                        }
                }}
            ]

            # Execute the pipeline and get the single curriculum returned.
            results = list(curriculum_collection.aggregate(pipeline))
            if not results:
                return None
            else:
                curriculum = results[0]
                return curriculum
        except Exception as e:
            logger.error(f"Failed to get curriculum: {e}")
            raise
    
    def create_curriculum(self, curriculum_id, breadcrumb):
        """Create a curriculum by ID."""
        if not self.connected: return None

        try:
            curriculum_data = {
                "_id": ObjectId(curriculum_id),
                "completed":[],
                "now":[],
                "next":[],
                "later":[],
                "lastSaved": breadcrumb
            }
            curriculum_collection = self.db.get_collection(config.CURRICULUM_COLLECTION_NAME)
            result = curriculum_collection.insert_one(curriculum_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to create curriculum: {e}")
            raise

    def update_curriculum(self, curriculum_id, data):
        """Update a curriculum."""
        if not self.connected: return None

        try:
            curriculum_collection = self.db.get_collection(config.CURRICULUM_COLLECTION_NAME)
            curriculum_object_id = ObjectId(curriculum_id)
            
            match = {"_id": curriculum_object_id}
            pipeline = {"$set": data}            
            result = curriculum_collection.update_one(match, pipeline)
        except Exception as e:
            logger.error(f"Failed to update resource in curriculum: {e}")
            raise

        return result.modified_count

    def delete_curriculum(self, curriculum_id):
        """Delete a specific curriculum."""
        if not self.connected: return None

        try:
            curriculum_collection = self.db.get_collection(config.CURRICULUM_COLLECTION_NAME)
            curriculum_collection.delete_one({"_id": ObjectId(curriculum_id)})
        except Exception as e:
            logger.error(f"Failed to delete curriculum: {e}")

    # Singleton Getter
    @staticmethod
    def get_instance():
        """Get the singleton instance of the MongoIO class."""
        if MongoIO._instance is None:
            MongoIO()  # This calls the __new__ method and initializes the instance
        return MongoIO._instance
        
# Create a singleton instance of MongoIO
mongoIO = MongoIO.get_instance()