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
    def get_or_create_curriculum(curriculum_id):
        CurriculumService._check_user_access()

        mongo_io = MongoIO()
        curriculum = mongo_io.get_curriculum(curriculum_id)
        if curriculum == None:
            curriculum = mongo_io.create_curriculum(curriculum_id)
        return curriculum

    @staticmethod
    def add_resource_to_curriculum(curriculum_id, resource_data):
        CurriculumService._check_user_access()

        resource_data = CurriculumService._encode_resource_data(resource_data)
        mongo_io = MongoIO()
        return mongo_io.add_resource_to_curriculum(curriculum_id, resource_data)

    @staticmethod
    def update_curriculum(curriculum_id, seq, resource_data):
        CurriculumService._check_user_access()

        resource_data = CurriculumService._encode_resource_data(resource_data)
        mongo_io = MongoIO()
        return mongo_io.update_curriculum(curriculum_id, seq, resource_data)

    @staticmethod
    def delete_resource_from_curriculum(curriculum_id, seq):
        CurriculumService._check_user_access()

        mongo_io = MongoIO()
        mongo_io.delete_resource_from_curriculum(curriculum_id, seq)        