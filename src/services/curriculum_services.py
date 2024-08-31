from datetime import datetime
from bson import ObjectId
from src.utils.mongo_io import MongoIO
import logging
logger = logging.getLogger(__name__)

class CurriculumService:

    @staticmethod 
    def _check_user_access():
        # Role Based Access logic
        # if user.roles contains Admin, Mentor or
        # if user.roles contains Member and id = user_id
        return 
        #
        # logger.warn("Access Denied")
        # raise Exception("Access Denied")

    @staticmethod
    def _encode_resource_data(resource_data):
        # Example encoding logic (this could be any transformation you need)
        # Encode ID
        # Encode Breadcrumb
        # Encode Dates
        return resource_data
    
    @staticmethod
    def _stringify_mongo_types(document):
        """Recursively convert ObjectId and datetime values to strings in a dictionary."""
        if isinstance(document, dict):
            return {
                key: CurriculumService._stringify_mongo_types(value) for key, value in document.items()
            }
        elif isinstance(document, list):
            return [CurriculumService._stringify_mongo_types(item) for item in document]
        elif isinstance(document, ObjectId):
            return str(document)
        elif isinstance(document, datetime):
            return document.isoformat()
        else:
            return document        
    


    @staticmethod
    def get_or_create_curriculum(curriculum_id):
        CurriculumService._check_user_access()

        mongo_io = MongoIO()
        curriculum = mongo_io.get_curriculum(curriculum_id)
        if curriculum == None:
            curriculum = mongo_io.create_curriculum(curriculum_id)
        return CurriculumService._stringify_mongo_types(curriculum)

    @staticmethod
    def add_resource_to_curriculum(curriculum_id, resource_data, breadcrumb):
        CurriculumService._check_user_access()

        resource_data = CurriculumService._encode_resource_data(resource_data)
        mongo_io = MongoIO()
        return mongo_io.add_resource_to_curriculum(curriculum_id, resource_data, breadcrumb)

    @staticmethod
    def update_curriculum(curriculum_id, seq, resource_data, breadcrumb):
        CurriculumService._check_user_access()

        resource_data = CurriculumService._encode_resource_data(resource_data)
        mongo_io = MongoIO()
        return mongo_io.update_curriculum(curriculum_id, seq, resource_data, breadcrumb)

    @staticmethod
    def delete_resource_from_curriculum(curriculum_id, seq, breadcrumb):
        CurriculumService._check_user_access()

        mongo_io = MongoIO()
        mongo_io.delete_resource_from_curriculum(curriculum_id, seq, breadcrumb)
        
