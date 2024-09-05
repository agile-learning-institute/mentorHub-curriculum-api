from datetime import datetime
from bson import ObjectId
from src.utils.mongo_io import MongoIO
import logging
logger = logging.getLogger(__name__)

class CurriculumService:

    @staticmethod 
    def _check_user_access(curriculum_id, token):
        """Role Based Access Control logic"""
        # Staff can edit all curriculums
        if "Staff" in token["roles"]: return
        
        # Members can access their own curriculum
        if "Member" in token["roles"] and curriculum_id == token["user_id"]: return
        
        # Mentors can access their apprenticeses curriculums
        if "Mentor" in token["roles"]:
            mentor = MongoIO().get_mentor(curriculum_id)
            if mentor == token["user_id"]:
                return
        
        # User has No Access! Log a warning and raise an exception
        logger.warn(f"Access Denied: {curriculum_id}, {token['user_id']}, {token['roles']}")
        raise Exception("Access Denied")

    @staticmethod
    def _encode_resource_data(document):
        """Encode ObjectId and datetime values for MongoDB"""
        id_properties = ["resource_id"]
        date_properties = ["started", "completed"]
        
        def encode_value(key, value):
            """Encode identified values"""
            if key in id_properties:
                if isinstance(value, str):
                    return ObjectId(value)
                if isinstance(value, list):
                    return [ObjectId(item) if isinstance(item, str) else item for item in value]
            if key in date_properties:
                if isinstance(value, str):
                    return datetime.fromisoformat(value)
                if isinstance(value, list):
                    return [datetime.fromisoformat(item) if isinstance(item, str) else item for item in value]
            return value

        # Traverse the document and encode relevant properties
        for key, value in document.items():
            if isinstance(value, dict):
                CurriculumService._encode_resource_data(value)  # Recursively encode nested documents
            elif isinstance(value, list):
                # Check if the list contains dictionaries (objects)
                if all(isinstance(item, dict) for item in value):
                    document[key] = [CurriculumService._encode_resource_data(item) for item in value]
                else:
                    document[key] = [encode_value(key, item) for item in value]  # Encode non-object list items
            else:
                document[key] = encode_value(key, value)  # Encode single values

        return document
        
    @staticmethod
    def _decode_mongo_types(document):
        """Convert all ObjectId and datetime values to strings"""
        if isinstance(document, dict):
            return {key: CurriculumService._decode_mongo_types(value) for key, value in document.items()}
        elif isinstance(document, list):
            return [CurriculumService._decode_mongo_types(item) for item in document]
        elif isinstance(document, ObjectId):
            return str(document)
        elif isinstance(document, datetime):
            return document.isoformat()
        else:
            return document

    @staticmethod
    def get_or_create_curriculum(curriculum_id, token, breadcrumb):
        """Get a curriculum if it exits, if not create a new one and return that"""
        CurriculumService._check_user_access(curriculum_id, token)

        mongo_io = MongoIO()
        curriculum = mongo_io.get_curriculum(curriculum_id)
        if curriculum == None:
            mongo_io.create_curriculum(curriculum_id, breadcrumb)
            curriculum = mongo_io.get_curriculum(curriculum_id)
        return CurriculumService._decode_mongo_types(curriculum)

    @staticmethod
    def add_resource_to_curriculum(curriculum_id, resource_data, token, breadcrumb):
        """Add the provied resource to the specified curriculum"""
        CurriculumService._check_user_access(curriculum_id, token)

        mongo_io = MongoIO()
        
        resource_data = CurriculumService._encode_resource_data(resource_data)
        mongo_io.add_resource_to_curriculum(curriculum_id, resource_data, breadcrumb)
        
        curriculum = mongo_io.get_curriculum(curriculum_id)
        curriculum = CurriculumService._decode_mongo_types(curriculum)
        return curriculum

    @staticmethod
    def update_curriculum(curriculum_id, seq, resource_data, token, breadcrumb):
        """Update the specified resource in a curriculum"""
        CurriculumService._check_user_access(curriculum_id, token)

        mongo_io = MongoIO()

        resource_data = CurriculumService._encode_resource_data(resource_data)
        mongo_io.update_curriculum(curriculum_id, seq, resource_data, breadcrumb)

        curriculum = mongo_io.get_curriculum(curriculum_id)
        return CurriculumService._decode_mongo_types(curriculum)

    @staticmethod
    def delete_resource_from_curriculum(curriculum_id, seq, token, breadcrumb):
        """Remove a resource from the curriculum"""
        CurriculumService._check_user_access(curriculum_id, token)

        mongo_io = MongoIO()
        mongo_io.delete_resource_from_curriculum(curriculum_id, seq, breadcrumb)

        curriculum = mongo_io.get_curriculum(curriculum_id)
        return CurriculumService._decode_mongo_types(curriculum)

    @staticmethod
    def delete_curriculum(curriculum_id, token):
        """Remove a resource from the curriculum"""
        CurriculumService._check_user_access(curriculum_id, token)

        mongo_io = MongoIO()
        mongo_io.delete_curriculum(curriculum_id)

        return 
