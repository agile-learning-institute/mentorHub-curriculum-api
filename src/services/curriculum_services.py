from config import config

class CurriculumService:

    @staticmethod
    def get_or_create_curriculum(curriculum_id):
        mongo_io = config.get_mongo_io()
        # Business logic, encoding, RBAC, etc. can be added here
        return mongo_io.get_or_create_curriculum(curriculum_id)

    @staticmethod
    def add_resource_to_curriculum(curriculum_id, resource_data):
        mongo_io = config.get_mongo_io()
        # Business logic, encoding, RBAC, etc. can be added here
        return mongo_io.add_resource_to_curriculum(curriculum_id, resource_data)

    @staticmethod
    def update_curriculum(curriculum_id, seq, resource_data):
        mongo_io = config.get_mongo_io()
        # Business logic, encoding, RBAC, etc. can be added here
        return mongo_io.update_curriculum(curriculum_id, seq, resource_data)

    @staticmethod
    def delete_resource_from_curriculum(curriculum_id, seq):
        mongo_io = config.get_mongo_io()
        # Business logic, encoding, RBAC, etc. can be added here
        mongo_io.delete_resource_from_curriculum(curriculum_id, seq)
        