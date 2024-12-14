from datetime import datetime
import json
from pathlib import Path
import os
import logging

from bson import ObjectId
logger = logging.getLogger(__name__)

class Config:
    _instance = None  # Singleton instance

    def __init__(self):
        if Config._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Config._instance = self
            self.config_items = []
            self.versions = []
            self.enumerators = {}
            self.CONFIG_FOLDER = "./"
            self.config_strings = {
                "BUILT_AT": "LOCAL",
                "CONFIG_FOLDER": "./",
                "MONGO_DB_NAME": "mentorHub",
                "CURRICULUM_COLLECTION_NAME": "curriculum",
                "ENCOUNTERS_COLLECTION_NAME": "encounters",
                "PARTNERS_COLLECTION_NAME": "partners",
                "PATHS_COLLECTION_NAME": "paths",
                "PEOPLE_COLLECTION_NAME": "people",
                "PLANS_COLLECTION_NAME": "plans",
                "RATINGS_COLLECTION_NAME": "ratings",
                "REVIEWS__COLLECTION_NAME": "reviews",
                "TOPICS_COLLECTION_NAME": "topics",
                "VERSION_COLLECTION_NAME": "msmCurrentVersions",
                "ENUMERATORS_COLLECTION_NAME": "enumerators",
                "CURRICULUM_UI_URI": "http://localhost:8089/",
                "ENCOUNTER_UI_URI": "http://localhost:8091/",
                "PARTNERS_UI_URI": "http://localhost:8085/",
                "PEOPLE_UI_URI": "http://localhost:8083/",
                "TOPICS_UI_URI": "http://localhost:8087/",
                "SEARCH_UI_URI": "http://localhost:8080/"
            }
            self.config_ints = {
                "CURRICULUM_API_PORT": "8088",
                "ENCOUNTER_API_PORT": "8090",
                "PARTNERS_API_PORT": "8084",
                "PEOPLE_API_PORT": "8082",
                "TOPICS_API_PORT": "8086",
                "SEARCH_API_PORT": "8081"
            }
            self.config_string_secrets = {
                "ELASTIC_INDEX_NAME": "mentorhub", 
                "MONGO_CONNECTION_STRING": "mongodb://mongodb:27017/?replicaSet=rs0",
            }
            self.config_json_secrets = {
                "ELASTIC_CLIENT_OPTIONS": '{"node":"http://localhost:9200"}',
            }

            # Initialize configuration
            self.initialize()

    def initialize(self):
        """Initialize configuration values."""
        self.config_items = []
        self.versions = []
        self.enumerators = {}

        for key, default in self.config_strings.items():
            value = self._get_config_value(key, default, False)
            setattr(self, key, value)
            
        for key, default in self.config_ints.items():
            value = int(self._get_config_value(key, default, False))
            setattr(self, key, value)
            
        for key, default in self.config_string_secrets.items():
            value = self._get_config_value(key, default, True)
            setattr(self, key, value)

        for key, default in self.config_json_secrets.items():
            value = json.loads(self._get_config_value(key, default, True))
            setattr(self, key, value)

        logger.info(f"Configuration Initialized: {self.config_items}")
            
    def _get_config_value(self, name, default_value, is_secret):
        """Retrieve a configuration value, first from a file, then environment variable, then default."""
        value = default_value
        from_source = "default"

        # Check for config file first
        file_path = Path(self.CONFIG_FOLDER) / name
        if file_path.exists():
            value = file_path.read_text().strip()
            from_source = "file"
            
        # If no file, check for environment variable
        elif os.getenv(name):
            value = os.getenv(name)
            from_source = "environment"

        # Record the source of the config value
        self.config_items.append({
            "name": name,
            "value": "secret" if is_secret else value,
            "from": from_source
        })
        return value

    # Serializer
    def to_dict(self, token):
        """Convert the Config object to a dictionary with the required fields."""
        return {
            "config_items": self.config_items,
            "versions": self.versions,
            "enumerators": self.enumerators,
            "token": token
        }    

    # Singleton Getter
    @staticmethod
    def get_instance():
        """Get the singleton instance of the Config class."""
        if Config._instance is None:
            Config()
        return Config._instance
        
# Create a singleton instance of Config and export it
config = Config.get_instance()