from pymongo import MongoClient

class MongoIO:
    def __init__(self):
        self.client = None
        self.db = None
        self.versions = None
        self.enumerators = None

    def connect(self):
        """Connect to MongoDB."""
        try:
            self.client = MongoClient("mongodb://root:example@localhost:27017")
            self.db = self.client.get_database("mentorHub")
            print("Connected to MongoDB")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise

    def load_versions(self):
        """Load the versions collection into memory."""
        try:
            self.versions = list(self.db["msmCurrentVersions"].find())
            print("Loaded versions collection into memory")
        except Exception as e:
            print(f"Failed to load versions: {e}")
            raise

    def load_enumerators(self, collection_name):
        """Load the enumerators collection into memory."""
        try:
            self.enumerators = list(self.db[collection_name].find())
            print("Loaded enumerators collection into memory")
        except Exception as e:
            print(f"Failed to load enumerators: {e}")
            raise

    def get_or_create_curriculum(self, curriculum_id):
        """Retrieve or create a curriculum by ID."""
        try:
            curriculum = self.db["curriculum"].find_one({"id": curriculum_id})
            if not curriculum:
                new_curriculum = {"id": curriculum_id, "resources": []}
                self.db["curriculum"].insert_one(new_curriculum)
                return new_curriculum
            return curriculum
        except Exception as e:
            print(f"Failed to get or create curriculum: {e}")
            raise

    def add_resource_to_curriculum(self, curriculum_id, resource_data):
        """Add a new resource to the curriculum."""
        try:
            update_result = self.db["curriculum"].update_one(
                {"id": curriculum_id},
                {"$push": {"resources": resource_data}}
            )
            if update_result.matched_count == 0:
                print(f"Curriculum with ID {curriculum_id} not found")
            else:
                print(f"Resource added to curriculum {curriculum_id}")
        except Exception as e:
            print(f"Failed to add resource to curriculum: {e}")
            raise

    def update_curriculum(self, curriculum_id, seq, resource_data):
        """Update a specific resource in the curriculum."""
        try:
            update_result = self.db["curriculum"].update_one(
                {"id": curriculum_id, "resources.seq": seq},
                {"$set": {"resources.$": resource_data}}
            )
            if update_result.matched_count == 0:
                print(f"Resource with seq {seq} not found in curriculum {curriculum_id}")
            else:
                print(f"Resource with seq {seq} updated in curriculum {curriculum_id}")
        except Exception as e:
            print(f"Failed to update resource in curriculum: {e}")
            raise

    def delete_resource_from_curriculum(self, curriculum_id, seq):
        """Delete a specific resource from the curriculum."""
        try:
            update_result = self.db["curriculum"].update_one(
                {"id": curriculum_id},
                {"$pull": {"resources": {"seq": seq}}}
            )
            if update_result.matched_count == 0:
                print(f"Resource with seq {seq} not found in curriculum {curriculum_id}")
            else:
                print(f"Resource with seq {seq} deleted from curriculum {curriculum_id}")
        except Exception as e:
            print(f"Failed to delete resource from curriculum: {e}")
            raise