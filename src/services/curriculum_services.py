from datetime import datetime
from bson import ObjectId
from flask import jsonify
from src.config.MentorHub_Config import MentorHub_Config
from src.utils.mentorhub_mongo_io import mentorhub_mongoIO
import logging
logger = logging.getLogger(__name__)

class CurriculumService:
    
    @staticmethod 
    def _check_user_access(curriculum_id, token):
        """Role Based Access Control logic"""
        config = MentorHub_Config.get_instance()
        
        # Staff can edit all curriculums
        if "Staff" in token["roles"]: return
        
        # Members can access their own curriculum
        if "Member" in token["roles"] and curriculum_id == token["user_id"]: return
        
        # Mentors can access their apprentices curriculums
        if "Mentor" in token["roles"]:
            apprentice = mentorhub_mongoIO.get_document(config.PEOPLE_COLLECTION_NAME, curriculum_id)
            if apprentice["mentorId"] == token["user_id"]:
                return
        
        # User has No Access! Log a warning and raise an exception
        logger.warning(f"Access Denied: {curriculum_id}, {token['user_id']}, {token['roles']}")
        raise Exception("Access Denied")
        
    @staticmethod
    def get_or_create_curriculum(curriculum_id, token, breadcrumb):
        """Get a curriculum if it exits, if not create a new one and return that"""
        config = MentorHub_Config.get_instance()
        CurriculumService._check_user_access(curriculum_id, token)

        curriculum = mentorhub_mongoIO.get_document(config.CURRICULUM_COLLECTION_NAME, curriculum_id)
        if curriculum == None:
            document = {
                "_id": ObjectId(curriculum_id),
                "lastSaved": breadcrumb
            }
            mentorhub_mongoIO.create_document(config.CURRICULUM_COLLECTION_NAME, document)
            curriculum = mentorhub_mongoIO.get_document(config.CURRICULUM_COLLECTION_NAME, curriculum_id)
        return curriculum

    @staticmethod
    def update_curriculum(curriculum_id, patch_data, token, breadcrumb):
        """Update the specified curriculum"""
        config = MentorHub_Config.get_instance()
        CurriculumService._check_user_access(curriculum_id, token)

        # Add breadcrumb to patch_data
        patch_data["lastSaved"] = breadcrumb
        curriculum = mentorhub_mongoIO.update_document(config.CURRICULUM_COLLECTION_NAME, curriculum_id, patch_data)
        return curriculum

    @staticmethod
    def delete_curriculum(curriculum_id, token):
        """Remove a curriculum - for testing"""
        config = MentorHub_Config.get_instance()

        if not "Staff" in token["roles"]:
            logger.warning(f"Delete Access Denied, Staff only: {token['roles']}")
            raise Exception("Access Denied")
    
        mentorhub_mongoIO.delete_document(config.CURRICULUM_COLLECTION_NAME, curriculum_id)
        return 

    @staticmethod
    def assign_resource(curriculum_id, link, token, breadcrumb):
        """Promote a resource from Next to Now"""
        config = MentorHub_Config.get_instance()
        CurriculumService._check_user_access(curriculum_id, token)

        curriculum = mentorhub_mongoIO.get_document(config.CURRICULUM_COLLECTION_NAME, curriculum_id)
        
        # Initialize curriculum, we won't be changing any of these values
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
                            curriculum = mentorhub_mongoIO.update_document(config.CURRICULUM_COLLECTION_NAME, curriculum_id, curriculum)
                            return curriculum
        raise ValueError(f"Resource with link '{link}' not found in next")
    
    @staticmethod
    def complete_resource(curriculum_id, link, review, token, breadcrumb):
        """Promote a resource from Now to Completed"""
        config = MentorHub_Config.get_instance()
        CurriculumService._check_user_access(curriculum_id, token)

        curriculum = mentorhub_mongoIO.get_document(config.CURRICULUM_COLLECTION_NAME, curriculum_id)
        
        # Initialize curriculum, we won't be changing any of these values
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
                curriculum = mentorhub_mongoIO.update_document(config.CURRICULUM_COLLECTION_NAME, curriculum_id, curriculum)
                return curriculum
        raise ValueError(f"Resource with link '{link}' not found in {curriculum['now']}")
    
    @staticmethod
    def add_path(curriculum_id, path_id, token, breadcrumb):
        """Add a path to Next"""
        config = MentorHub_Config.get_instance()
        CurriculumService._check_user_access(curriculum_id, token)

        curriculum = mentorhub_mongoIO.get_document(config.CURRICULUM_COLLECTION_NAME, curriculum_id)
        path = mentorhub_mongoIO.get_document(config.PATHS_COLLECTION_NAME, path_id)
        
        # Initialize curriculum, we won't be changing any of these values
        del curriculum["_id"]
        del curriculum["completed"]
        del curriculum["now"]
        del curriculum["later"]
        
        # Set the breadcrumb
        curriculum["lastSaved"] = breadcrumb

        # Add the path
        curriculum["next"] = curriculum["next"] + [path]

        # Update the database, get the updated document        
        curriculum = mentorhub_mongoIO.update_document(config.CURRICULUM_COLLECTION_NAME, curriculum_id, curriculum)
        return curriculum
    
