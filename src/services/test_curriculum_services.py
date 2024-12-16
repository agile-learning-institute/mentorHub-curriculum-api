import copy
from datetime import datetime, timezone
import unittest
from unittest.mock import patch

from bson import ObjectId
from mentorhub_config.MentorHub_Config import MentorHub_Config
from src.services.curriculum_services import CurriculumService

class TestCurriculumService(unittest.TestCase):
    
    def setUp(self):    
        self.maxDiff = None

        # Setup Test Data
        self.token = {"user_id":"ObjectID", "roles":["Staff"]}
        self.breadcrumb = {"atTime":datetime.fromisoformat("2024-08-01T12:00:00"),"byUser":ObjectId("aaaa00000000000000000001"),"fromIp":"127.0.0.1","correlationId":"aaaa-aaaa-aaaa-aaaa"}
        
    @patch('src.services.curriculum_services.mentorhub_mongoIO')
    def test_token_staff(self, mock_mentorhub_mongo_io):
        config = MentorHub_Config.get_instance()
        mock_mentorhub_mongo_io.get_document.return_value = {"foo": "bar"}

        curriculum = CurriculumService.get_or_create_curriculum("curriculum_id", self.token, self.breadcrumb)
        mock_mentorhub_mongo_io.get_document.assert_called_once_with(config.CURRICULUM_COLLECTION_NAME, "curriculum_id")
        self.assertEqual(curriculum, {"foo": "bar"})

    @patch('src.services.curriculum_services.mentorhub_mongoIO')
    def test_token_member_pass(self, mock_mentorhub_mongo_io):
        config = MentorHub_Config.get_instance()
        token = {"user_id":"000000000000000000000000", "roles":["Member"]}
        mock_mentorhub_mongo_io.get_document.return_value = {"foo": "bar"}

        curriculum = CurriculumService.get_or_create_curriculum("000000000000000000000000", token, self.breadcrumb)
        mock_mentorhub_mongo_io.get_document.assert_called_once_with(config.CURRICULUM_COLLECTION_NAME, "000000000000000000000000")
        self.assertEqual(curriculum, {"foo": "bar"})

    @patch('src.services.curriculum_services.mentorhub_mongoIO')
    def test_token_member_fail(self, mock_mentorhub_mongo_io):
        token = {"user_id":"000000000000000000000001", "roles":["Member"]}
        mock_mentorhub_mongo_io.get_document.return_value = {"foo": "bar"}

        with self.assertRaises(Exception) as context:
            CurriculumService.get_or_create_curriculum("", {}, {})

    @patch('src.services.curriculum_services.mentorhub_mongoIO')
    def test_token_mentor_pass(self, mock_mentorhub_mongo_io):
        config = MentorHub_Config.get_instance()
        token = {"user_id":"000000000000000000000012", "roles":["Mentor"]}
        mock_mentorhub_mongo_io.get_document.side_effect = [
            {"mentorId": "000000000000000000000012"},
            {"foo": "bar"}
        ]

        curriculum = CurriculumService.get_or_create_curriculum("000000000000000000000000", token, self.breadcrumb)
        mock_mentorhub_mongo_io.get_document.assert_has_calls([
            unittest.mock.call(config.PEOPLE_COLLECTION_NAME, "000000000000000000000000"),
            unittest.mock.call(config.CURRICULUM_COLLECTION_NAME, "000000000000000000000000")
        ])
        self.assertEqual(curriculum, {"foo": "bar"})

    @patch('src.services.curriculum_services.mentorhub_mongoIO')
    def test_token_mentor_fail(self, mock_mentorhub_mongo_io):
        token = {"user_id":"000000000000000000000012", "roles":["Mentor"]}
        mock_mentorhub_mongo_io.get_document.return_value = {"mentorId": "000000000000000000001234"}

        with self.assertRaises(Exception) as context:
            CurriculumService.get_or_create_curriculum("", {}, {})

    @patch('src.services.curriculum_services.mentorhub_mongoIO')
    def test_get_or_create_curriculum_new_success(self, mock_mentorhub_mongo_io):
        config = MentorHub_Config.get_instance()
        return_curriculum = {"_id":ObjectId("aaaa00000000000000000999"),"completed":[],"now":[],"next":[],"later":[],"lastSaved":self.breadcrumb}
        mock_mentorhub_mongo_io.get_document.side_effect = [None, return_curriculum]
        mock_mentorhub_mongo_io.create_document.return_value = {}

        
        # Call get_or_create_curriculum and test results
        curriculum = CurriculumService.get_or_create_curriculum("000000000000000000000000", self.token, self.breadcrumb)
        
        # Assert new document and downstream calls
        self.assertEqual(curriculum, return_curriculum)
        mock_mentorhub_mongo_io.create_document.assert_called_once_with(
            config.CURRICULUM_COLLECTION_NAME, {
                "_id": ObjectId("000000000000000000000000"),
                "lastSaved": self.breadcrumb
            }
        )
        
        mock_mentorhub_mongo_io.get_document.assert_has_calls([
            unittest.mock.call(config.CURRICULUM_COLLECTION_NAME, "000000000000000000000000"),
            unittest.mock.call(config.CURRICULUM_COLLECTION_NAME, "000000000000000000000000")
        ])
            
    @patch('src.services.curriculum_services.mentorhub_mongoIO')
    def test_get_or_create_curriculum_existing_success(self, mock_mentorhub_mongo_io):
        config = MentorHub_Config.get_instance()
        return_curriculum = {"_id":ObjectId("aaaa00000000000000000999"),"completed":[],"now":[],"next":[],"later":[],"lastSaved":self.breadcrumb}
        mock_mentorhub_mongo_io.get_document.return_value = return_curriculum
        
        # Call get_or_create_curriculum and test results
        curriculum = CurriculumService.get_or_create_curriculum("000000000000000000000000", self.token, self.breadcrumb)
        
        # Assert new document and downstream calls
        self.assertEqual(curriculum, return_curriculum)
        mock_mentorhub_mongo_io.get_document.assert_called_once_with(config.CURRICULUM_COLLECTION_NAME, "000000000000000000000000")
            
    @patch('src.services.curriculum_services.mentorhub_mongoIO')
    def test_update_curriculum_success(self, mock_mentorhub_mongo_io):
        config = MentorHub_Config.get_instance()
        return_curriculum = {"_id":ObjectId("aaaa00000000000000000999"),"completed":[],"now":[],"next":[],"later":[],"lastSaved":self.breadcrumb}
        mock_mentorhub_mongo_io.update_document.return_value = return_curriculum

        curriculum = CurriculumService.update_curriculum("aaaa00000000000000000001", {"now": []}, self.token, self.breadcrumb)
        mock_mentorhub_mongo_io.update_document.assert_called_once_with(config.CURRICULUM_COLLECTION_NAME, "aaaa00000000000000000001",{"now": [], "lastSaved": self.breadcrumb})

    @patch('src.services.curriculum_services.mentorhub_mongoIO')
    def test_delete_curriculum_success(self, mock_mentorhub_mongo_io):
        config = MentorHub_Config.get_instance()
        mock_mentorhub_mongo_io.delete_document.return_value = {}

        curriculum = CurriculumService.delete_curriculum("aaaa00000000000000000001", self.token)
        mock_mentorhub_mongo_io.delete_document.assert_called_once_with(config.CURRICULUM_COLLECTION_NAME, "aaaa00000000000000000001")

    @patch('src.services.curriculum_services.mentorhub_mongoIO')
    def test_assign_resource_simple_success(self, mock_mentorhub_mongo_io):
        # Setup test data
        config = MentorHub_Config.get_instance()
        before_update = {"_id": ObjectId("aaaa00000000000000000001"), "completed": [], "later": [], "now":[{"name":"AWSStorageResource","link":"https://somevalidlink.35.com","description":"foo","started":datetime.fromisoformat("2024-07-15T13:00:00")},{"name":"Some Unique Resource","link":"https://some.com/resource","description":"bar"}],"next":[{"path":"The Odin Project","segments":[{"segment":"Intermediate HTML and CSS","topics":[{"topic":"Intermediate HTML","resources":[{"name":"A one-off resource","link":"https://some.com/resource","description":"test-it2"},{"name":"Howdocomputersreadcode?V","link":"https://somevalidlink.22.com","description":"test-it1"}]}]}]}],"lastSaved":self.breadcrumb}
        expected_after = {"now":[{"name":"AWSStorageResource","link":"https://somevalidlink.35.com","description":"foo","started":datetime.fromisoformat("2024-07-15T13:00:00")},{"name":"Some Unique Resource","link":"https://some.com/resource","description":"bar"},{"name":"Howdocomputersreadcode?V","link":"https://somevalidlink.22.com","description":"test-it1"}],"next":[{"path":"The Odin Project","segments":[{"segment":"Intermediate HTML and CSS","topics":[{"topic":"Intermediate HTML","resources":[{"name":"A one-off resource","link":"https://some.com/resource","description":"test-it2"}]}]}]}],"lastSaved":self.breadcrumb}
        
        # Mock the MongoIO methods
        mock_mentorhub_mongo_io.get_document.return_value = before_update
        mock_mentorhub_mongo_io.update_document.return_value = {"foo":"bar"}

        # Promote one of two resources, no containers removed
        curriculum = CurriculumService.assign_resource("aaaa00000000000000000001", "https://somevalidlink.22.com", self.token, self.breadcrumb)
        self.assertEqual(curriculum, {"foo":"bar"})
        mock_mentorhub_mongo_io.get_document.assert_called_once_with(config.CURRICULUM_COLLECTION_NAME, "aaaa00000000000000000001")
        mock_mentorhub_mongo_io.update_document.assert_called_once_with(config.CURRICULUM_COLLECTION_NAME, "aaaa00000000000000000001", expected_after)

    @patch('src.services.curriculum_services.mentorhub_mongoIO')
    def test_assign_resource_cleaning_success(self, mock_mentorhub_mongo_io):
        # Setup test data
        config = MentorHub_Config.get_instance()
        before_update = {"_id": ObjectId("aaaa00000000000000000001"), "completed": [], "later": [], "now":[{"name":"AWSStorageResource","link":"https://somevalidlink.35.com","description":"foo","started":datetime.fromisoformat("2024-07-15T13:00:00")},{"name":"Some Unique Resource","link":"https://some-other.com/resource","description":"bar"}],"next":[{"path":"The Odin Project","segments":[{"segment":"Intermediate HTML and CSS","topics":[{"topic":"Intermediate HTML","resources":[{"name":"A one-off resource","description":"test","link":"https://some.com/resource"}]}]}]}],"lastSaved":self.breadcrumb}
        expected_after = {"now":[{"name":"AWSStorageResource","link":"https://somevalidlink.35.com","description":"foo","started":datetime.fromisoformat("2024-07-15T13:00:00")},{"name":"Some Unique Resource","link":"https://some-other.com/resource","description":"bar"},{"name":"A one-off resource","description":"test","link":"https://some.com/resource"}],"next":[],"lastSaved":self.breadcrumb}
        
        # Mock the MongoIO methods
        mock_mentorhub_mongo_io.get_document.return_value = before_update
        mock_mentorhub_mongo_io.update_document.return_value = {"foo":"bar"}

        # Promote one of one resources containers removed
        curriculum = CurriculumService.assign_resource("aaaa00000000000000000001", "https://some.com/resource", self.token, self.breadcrumb)
        self.assertEqual(curriculum, {"foo":"bar"})
        mock_mentorhub_mongo_io.get_document.assert_called_once_with(config.CURRICULUM_COLLECTION_NAME, "aaaa00000000000000000001")
        mock_mentorhub_mongo_io.update_document.assert_called_once_with(config.CURRICULUM_COLLECTION_NAME, "aaaa00000000000000000001", expected_after)

    @patch('src.services.curriculum_services.datetime')
    @patch('src.services.curriculum_services.mentorhub_mongoIO')
    def test_complete_resource_with_rating_success(self, mock_mentorhub_mongo_io, mock_datetime):
        # Setup test data
        config = MentorHub_Config.get_instance()
        before_update = {"_id":ObjectId("aaaa00000000000000000001"),"next":[],"later":[],"completed":[],"now":[{"name":"AWSStorageResource","link":"https://somevalidlink.35.com","description":"foo","started":datetime.fromisoformat("2024-07-15T13:00:00")},{"name":"Some Unique Resource","link":"https://some-other.com/resource","description":"bar"}],"lastSaved":self.breadcrumb}
        expected_after = {"completed":[{"name":"AWSStorageResource","link":"https://somevalidlink.35.com","description":"foo","started":datetime.fromisoformat("2024-07-15T13:00:00"),"completed":datetime.fromisoformat("2024-01-01T12:34:56"),"rating":4,"review":"Nice"}],"now":[{"name":"Some Unique Resource","link":"https://some-other.com/resource","description":"bar"}],"lastSaved":self.breadcrumb}

        # Mock the MongoIO methods
        mock_mentorhub_mongo_io.get_document.return_value = before_update.copy()
        mock_mentorhub_mongo_io.update_document.return_value = {"foo": "bar"}
        mock_datetime.now.return_value = datetime.fromisoformat("2024-01-01T12:34:56")

        # Call complete_resource
        curriculum = CurriculumService.complete_resource(
            "aaaa00000000000000000001", 
            "https://somevalidlink.35.com", 
            {"rating": 4, "review": "Nice"}, 
            self.token, 
            self.breadcrumb
        )

        # Assertions
        self.assertEqual(curriculum, {"foo": "bar"})
        mock_mentorhub_mongo_io.get_document.assert_called_once_with(config.CURRICULUM_COLLECTION_NAME, "aaaa00000000000000000001")
        mock_mentorhub_mongo_io.update_document.assert_called_once_with(config.CURRICULUM_COLLECTION_NAME, "aaaa00000000000000000001", expected_after)
    
    @patch('src.services.curriculum_services.datetime')
    @patch('src.services.curriculum_services.mentorhub_mongoIO')
    def test_complete_resource_without_rating_success(self, mock_mentorhub_mongo_io, mock_datetime):
        # Setup test data
        config = MentorHub_Config.get_instance()
        before_update = {"_id":ObjectId("aaaa00000000000000000001"),"next":[],"later":[],"completed":[],"now":[{"name":"AWSStorageResource","link":"https://somevalidlink.35.com","description":"foo","started":datetime.fromisoformat("2024-07-15T13:00:00")},{"name":"Some Unique Resource","link":"https://some-other.com/resource","description":"bar"}],"lastSaved":self.breadcrumb}
        expected_after = {"completed":[{"name":"AWSStorageResource","link":"https://somevalidlink.35.com","description":"foo","started":datetime.fromisoformat("2024-07-15T13:00:00"),"completed":datetime.fromisoformat("2024-01-01T12:34:56")}],"now":[{"name":"Some Unique Resource","link":"https://some-other.com/resource","description":"bar"}],"lastSaved":self.breadcrumb}

        # Mock the MongoIO methods
        mock_mentorhub_mongo_io.get_document.return_value = before_update.copy()
        mock_mentorhub_mongo_io.update_document.return_value = {"foo": "bar"}
        mock_datetime.now.return_value = datetime.fromisoformat("2024-01-01T12:34:56")

        # Call complete_resource
        curriculum = CurriculumService.complete_resource("aaaa00000000000000000001", "https://somevalidlink.35.com", {}, self.token, self.breadcrumb)

        # Assertions
        self.assertEqual(curriculum, {"foo": "bar"})
        mock_mentorhub_mongo_io.get_document.assert_called_once_with(config.CURRICULUM_COLLECTION_NAME, "aaaa00000000000000000001")
        mock_mentorhub_mongo_io.update_document.assert_called_once_with(config.CURRICULUM_COLLECTION_NAME, "aaaa00000000000000000001", expected_after)

    @patch('src.services.curriculum_services.mentorhub_mongoIO')
    def test_add_path_success(self, mock_mentorhub_mongo_io):
        # Setup Test Data
        config = MentorHub_Config.get_instance()
        curriculum = {"_id": "", "completed": [], "now": [], "next": [], "later": []}
        path = {"path":"The Odin Project","segments":[{"segment":"Intermediate HTML and CSS","topics":[{"topic":"Intermediate HTML","resources":[{"name":"Howdocomputersreadcode?V","link":"https://somevalidlink.22.com","description":"test-it1"},{"name":"A one-off resource","link":"https://some.com/resource","description":"test-it2"}]}]}]}
        expected_update = {"next":[path], "lastSaved":self.breadcrumb}
        
        # Mock the MongoIO methods
        mock_mentorhub_mongo_io.get_document.side_effect = [curriculum,path]
        mock_mentorhub_mongo_io.update_document.return_value = {"foo":"bar"}
        
        curriculum = CurriculumService.add_path("aaaa00000000000000000001", "cccc00000000000000000001", self.token, self.breadcrumb)
        self.assertEqual(curriculum, {"foo":"bar"})
        mock_mentorhub_mongo_io.update_document.assert_called_once_with(config.CURRICULUM_COLLECTION_NAME, "aaaa00000000000000000001", expected_update)
        mock_mentorhub_mongo_io.get_document.assert_has_calls([
            unittest.mock.call(config.CURRICULUM_COLLECTION_NAME, "aaaa00000000000000000001"),
            unittest.mock.call(config.PATHS_COLLECTION_NAME, "cccc00000000000000000001")
        ])

if __name__ == '__main__':
    unittest.main()