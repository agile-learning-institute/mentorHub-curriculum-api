from copy import deepcopy
from datetime import datetime, timezone
import unittest

from bson import ObjectId
from src.config.Config import config
from src.utils.mentorhub_mongo_io import MentorHubMongoIO

class TestMentorhubMongoIO(unittest.TestCase):
    
    def setUp(self):       
        self.test_id = "eeee00000000000000009999"
        
        MentorHubMongoIO._instance = None
        mongo_io = MentorHubMongoIO.get_instance()
        mongo_io.initialize("curriculum")
        print(f"Setup Connected: {mongo_io.connected}")

    def tearDown(self):
        mongo_io = MentorHubMongoIO.get_instance()
        mongo_io.delete_document("encounter", self.test_id)
        mongo_io.disconnect()
    
    def test_singleton_behavior(self):
        # Test that MentorHubMongoIO is a singleton
        mongo_io1 = MentorHubMongoIO.get_instance()
        mongo_io2 = MentorHubMongoIO.get_instance()
        self.assertIs(mongo_io1, mongo_io2, "MentorHubMongoIO should be a singleton")

    def test_config_loaded(self):
        # Test that Config loaded version and enumerators
        self.assertIsInstance(config.versions, list)
        self.assertEqual(len(config.versions), 9)

        self.assertIsInstance(config.enumerators, dict)

    def test_CRUD_document(self):
        # Create a Test Document
        test_data = {
            "personId": ObjectId("aaaa00000000000000000004"),
            "mentorId": ObjectId("aaaa00000000000000000027"),
            "planId": ObjectId("eeff00000000000000000002"),
            "status": "Active"
        }
        mongo_io = MentorHubMongoIO.get_instance()
        self.test_id = mongo_io.create_document("encounters", test_data)
        encounter_id_str = str(self.test_id)
        
        self.assertEqual(encounter_id_str, str(self.test_id))

        # Retrieve the document
        encounter = mongo_io.get_document("encounters", encounter_id_str)
        self.assertIsInstance(encounter, dict)
        self.assertIsInstance(encounter["_id"], ObjectId)
        self.assertEqual(encounter["personId"], ObjectId("aaaa00000000000000000004"))
        self.assertEqual(encounter["mentorId"], ObjectId("aaaa00000000000000000027"))
        self.assertEqual(encounter["planId"],  ObjectId("eeff00000000000000000002"))
        
        # Update the document
        test_update = {
            "personId": ObjectId("aaaa00000000000000011111")
        }
        encounter = mongo_io.update_document("encounters", encounter_id_str, test_update)
        print(f"Update Returned {encounter}")
        self.assertIsInstance(encounter, dict)
        self.assertIsInstance(encounter["_id"], ObjectId)
        self.assertEqual(encounter["personId"], ObjectId("aaaa00000000000000011111"))
        
    def test_get_all_full_documents(self):
        mongo_io = MentorHubMongoIO.get_instance()
        result = mongo_io.get_documents("enumerators")
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["name"], "Enumerations")
        self.assertEqual(result[0]["version"], 0)
        self.assertEqual(result[0]["status"], "Depricated")

    def test_get_some_full_documents(self):
        mongo_io = MentorHubMongoIO.get_instance()
        match = {"version":1}
        result = mongo_io.get_documents("enumerators", match)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Enumerations")
        self.assertEqual(result[0]["version"], 1)
        self.assertEqual(result[0]["status"], "Active")
        
    def test_get_all_partial_documents(self):
        mongo_io = MentorHubMongoIO.get_instance()
        project = {"name":1, "version": 1}
        result = mongo_io.get_documents("enumerators", project=project)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["name"], "Enumerations")
        self.assertEqual(result[0]["version"], 0)
        self.assertNotIn("status", result[0])
        self.assertNotIn("enumerators", result[0])
        
    def test_get_some_partial_documents(self):
        mongo_io = MentorHubMongoIO.get_instance()
        match = {"version":1}
        project = {"name":1, "_id": 1}
        result = mongo_io.get_documents("enumerators", match, project)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Enumerations")
        self.assertIn("_id", result[0])
        self.assertNotIn("version", result[0])
        self.assertNotIn("status", result[0])
        self.assertNotIn("enumerators", result[0])
        
        
if __name__ == '__main__':
    unittest.main()