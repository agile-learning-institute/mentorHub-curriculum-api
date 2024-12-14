from datetime import datetime
from bson import ObjectId
from flask import jsonify
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
        
        # Mentors can access their apprentices curriculums
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
        id_properties = ["later"]
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
    def get_or_create_curriculum(curriculum_id, token, breadcrumb):
        """Get a curriculum if it exits, if not create a new one and return that"""
        CurriculumService._check_user_access(curriculum_id, token)

        mongo_io = MongoIO()
        curriculum = mongo_io.get_curriculum(curriculum_id)
        if curriculum == None:
            mongo_io.create_curriculum(curriculum_id, breadcrumb)
            curriculum = mongo_io.get_curriculum(curriculum_id)
        return curriculum

    @staticmethod
    def update_curriculum(curriculum_id, patch_data, token, breadcrumb):
        """Update the specified curriculum"""
        CurriculumService._check_user_access(curriculum_id, token)

        # Add breadcrumb to patch_data
        patch_data["lastSaved"] = breadcrumb
        mongo_io = MongoIO()
        mongo_io.update_curriculum(curriculum_id, patch_data)
        curriculum = mongo_io.get_curriculum(curriculum_id)
        return curriculum

    @staticmethod
    def delete_curriculum(curriculum_id, token):
        """Remove a resource from the curriculum"""
        if not "Staff" in token["roles"]:
            logger.warn(f"Delete Access Denied, Staff only: {token['roles']}")
            raise Exception("Access Denied")
    
        CurriculumService._check_user_access(curriculum_id, token)

        mongo_io = MongoIO()
        mongo_io.delete_curriculum(curriculum_id)
        return 

    @staticmethod
    def assign_resource(curriculum_id, link, token, breadcrumb):
        """Promote a resource from Next to Now"""
        # Check if the user has access
        CurriculumService._check_user_access(curriculum_id, token)

        mongo_io = MongoIO()
        curriculum = mongo_io.get_curriculum(curriculum_id)
        
        # Initilize curriculum, we won't be changing any of these values
        del curriculum["_id"]
        del curriculum["completed"]
        del curriculum["later"]
        
        # Set the breadcrumb
        curriculum["lastSaved"] = breadcrumb

        # Find the resource in curriculum.next by link
        for path in curriculum.get('next', []):
            for segment in path.get('segments', []):
                for topic in segment.get('topics', []):
                    for resource in topic.get('resources', []):
                        if resource.get('link') == link:
                            # Add resource to curriculum.now 
                            curriculum.get('now').append({
                                'name': resource.get('name'),
                                'link': resource.get('link'),
                                'description': resource.get('description')
                            })

                            # Remove the resource from curriculum.next
                            topic['resources'].remove(resource)

                            # Remove empty containers (topic, segment, path) from next
                            if not topic['resources']:
                                segment['topics'].remove(topic)
                            if not segment['topics']:
                                path['segments'].remove(segment)
                            if not path['segments']:
                                curriculum['next'].remove(path)
                                
                            # Update the curriculum and return
                            mongo_io.update_curriculum(curriculum_id, curriculum)
                            curriculum = mongo_io.get_curriculum(curriculum_id)
                            return curriculum
        raise ValueError(f"Resource with link '{link}' not found in next")
    
    @staticmethod
    def complete_resource(curriculum_id, link, review, token, breadcrumb):
        """Promote a resource from Now to Completed"""
        CurriculumService._check_user_access(curriculum_id, token)

        mongo_io = MongoIO()
        curriculum = mongo_io.get_curriculum(curriculum_id)
        
        # Initilize curriculum, we won't be changing any of these values
        del curriculum["_id"]
        del curriculum["next"]
        del curriculum["later"]
        
        # Set the breadcrumb
        curriculum["lastSaved"] = breadcrumb
        
        # Find the resource in curriculum.now by link
        for resource in curriculum['now']:
            if resource.get('link') == link:
                # Remove the resource from curriculum.now
                curriculum['now'].remove(resource)

                # Add resource to curriculum.completed
                resource["completed"] = datetime.now()
                resource = {**resource, **review}
                curriculum.get('completed').append(resource)

                # Update the curriculum and return
                mongo_io.update_curriculum(curriculum_id, curriculum)
                curriculum = mongo_io.get_curriculum(curriculum_id)
                return curriculum
        raise ValueError(f"Resource with link '{link}' not found in {curriculum['now']}")
    
    @staticmethod
    def add_path(curriculum_id, path_id, token, breadcrumb):
        """Add a path to Next"""
        CurriculumService._check_user_access(curriculum_id, token)

        mongo_io = MongoIO()
        curriculum = mongo_io.get_curriculum(curriculum_id)
        path = mongo_io.get_path(path_id)
        
        # Initilize curriculum, we won't be changing any of these values
        del curriculum["_id"]
        del curriculum["completed"]
        del curriculum["now"]
        del curriculum["later"]
        
        # Set the breadcrumb
        curriculum["lastSaved"] = breadcrumb

        # Add the path
        curriculum["next"] = curriculum["next"] + path

        # Update the database, get the updated document        
        mongo_io.update_curriculum(curriculum_id, curriculum)
        curriculum = mongo_io.get_curriculum(curriculum_id)
        return curriculum
    
