import copy
from datetime import datetime, timezone
import unittest
from unittest.mock import patch, MagicMock

from bson import ObjectId
from src.services.curriculum_services import CurriculumService
from src.utils.mongo_io import MongoIO

class TestCurriculumService(unittest.TestCase):
    
    def setUp(self):    
        self.maxDiff = None

        # Setup Test Data
        self.goodTokens = [
            {"user_id":"000000000000000000000000", "roles":["Staff"]},
            {"user_id":"aaaa00000000000000000001", "roles":["Member"]},
            {"user_id":"aaaa00000000000000000012", "roles":["Mentor"]}        
        ]
        self.rejectTokens = [
            {"user_id":"000000000000000000000000", "roles":["Member"]},
            {"user_id":"aaaa00000000000000000001", "roles":["Mentor"]}
        ]
        
        self.mongoBreadcrumb = {"atTime":datetime.fromisoformat("2024-08-01T12:00:00"),"byUser":ObjectId("aaaa00000000000000000001"),"fromIp":"127.0.0.1","correlationId":"aaaa-aaaa-aaaa-aaaa"}
        self.mongoEmptyCurriculum = {"id":ObjectId("aaaa00000000000000000001"),"resources":[],"lastSaved":self.mongoBreadcrumb}
        self.mongoTestResource1 = {"sequence":1,"roadmap":"Completed","path":"The Odin Project","segment":"Foundations","topic":"OdinIntro","type":"Resource","resource_id":ObjectId("cccc00000000000000000008"),"started":datetime.fromisoformat("2024-07-01T13:00:00"),"completed":datetime.fromisoformat("2024-07-01T14:30:00"),"rating":4,"review":"This was a great intro"}
        self.mongoTestResource2 = {"sequence":2,"roadmap":"Completed","path":"The Odin Project","segment":"Foundations","topic":"OdinIntro","type":"Adhoc","resource_name":"Markdown Tutorial","resource_url":"https://www.markdowntutorial.com/lesson/1/","started":datetime.fromisoformat("2024-07-02T13:00:00"),"completed":datetime.fromisoformat("2024-07-03T19:36:00"),"rating":3,"review":"I had to read this twice before it made sense"}
        self.mongoTestData = {"id": ObjectId("aaaa00000000000000000001"),"resources": [ self.mongoTestResource1, self.mongoTestResource2 ],"lastSaved": self.mongoBreadcrumb}

        self.stringBreadcrumb = {"atTime":"2024-08-01T12:00:00","byUser":"aaaa00000000000000000001","fromIp":"127.0.0.1","correlationId":"aaaa-aaaa-aaaa-aaaa"}
        self.stringEmptyCurriculum = {"id":"aaaa00000000000000000001","resources":[],"lastSaved":self.stringBreadcrumb}
        self.stringTestResource1 = {"sequence":1,"roadmap":"Completed","path":"The Odin Project","segment":"Foundations","topic":"OdinIntro","type":"Resource","resource_id":"cccc00000000000000000008","started":"2024-07-01T13:00:00","completed":"2024-07-01T14:30:00","rating":4,"review":"This was a great intro"}
        self.stringTestResource2 = {"sequence":2,"roadmap":"Completed","path":"The Odin Project","segment":"Foundations","topic":"OdinIntro","type":"Adhoc","resource_name":"Markdown Tutorial","resource_url":"https://www.markdowntutorial.com/lesson/1/","started":"2024-07-02T13:00:00","completed":"2024-07-03T19:36:00","rating":3,"review":"I had to read this twice before it made sense"}
        self.stringTestData = {"id": "aaaa00000000000000000001","resources": [ self.stringTestResource1, self.stringTestResource2 ],"lastSaved": self.stringBreadcrumb}
        
    @patch('src.services.curriculum_services.MongoIO')
    def test_get_or_create_curriculum_existing_success(self, mock_mongo_io):
        # Test with passing tokens
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.get_curriculum.return_value = self.mongoTestData
        mock_instance.getMentor.return_value = "aaaa00000000000000000012"

        for token in self.goodTokens:
            curriculum = CurriculumService.get_or_create_curriculum("aaaa00000000000000000001", token, self.mongoBreadcrumb)
            mock_instance.get_curriculum.assert_called_once_with("aaaa00000000000000000001")
            self.assertEqual(curriculum, self.stringTestData)
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_get_or_create_curriculum_existing_access_error(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.get_curriculum.return_value = self.mongoTestData
        mock_instance.getMentor.return_value = "aaaa00000000000000000012"

        # Test with failing tokens
        for token in self.rejectTokens:
            with self.assertRaises(Exception) as context:
                CurriculumService.get_or_create_curriculum("aaaa00000000000000000001", token, self.mongoBreadcrumb)
            mock_instance.reset_mock()
                    
    @patch('src.services.curriculum_services.MongoIO')
    def test_get_or_create_curriculum_new_success(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.get_curriculum.return_value = None
        mock_instance.create_curriculum.return_value = self.mongoEmptyCurriculum
        mock_instance.getMentor.return_value = "aaaa00000000000000000012"

        # Test with passing tokens
        for token in self.goodTokens:
            curriculum = CurriculumService.get_or_create_curriculum("aaaa00000000000000000001", token, self.mongoBreadcrumb)
            mock_instance.get_curriculum.assert_called_once_with("aaaa00000000000000000001")
            mock_instance.create_curriculum.assert_called_once_with("aaaa00000000000000000001", self.mongoBreadcrumb)
            self.assertEqual(curriculum, self.stringEmptyCurriculum)
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_get_or_create_curriculum_new_access_error(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.get_curriculum.return_value = None
        mock_instance.create_curriculum.return_value = self.mongoEmptyCurriculum
        mock_instance.getMentor.return_value = "aaaa00000000000000000012"

        # Test with failing tokens
        for token in self.rejectTokens:
            with self.assertRaises(Exception) as context:
                CurriculumService.get_or_create_curriculum("aaaa00000000000000000001", token, self.mongoBreadcrumb)
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_add_resource_to_curriculum_success(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.add_resource_to_curriculum.return_value = True
        mock_instance.get_curriculum.return_value = self.mongoTestData
        mock_instance.getMentor.return_value = "aaaa00000000000000000012"

        print(f"STARTING TEST_STRING {self.stringTestData}")

        # Test with passing tokens
        for token in self.goodTokens:
            curriculum = CurriculumService.add_resource_to_curriculum(
                "aaaa00000000000000000001", 
                copy.deepcopy(self.stringTestResource1),
                token, 
                self.mongoBreadcrumb
            )
            mock_instance.add_resource_to_curriculum.assert_called_once_with(
                "aaaa00000000000000000001",
                self.mongoTestResource1,
                self.mongoBreadcrumb
            )
            mock_instance.get_curriculum.assert_called_once_with("aaaa00000000000000000001")
            self.assertEqual(curriculum, self.stringTestData)
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_add_resource_to_curriculum_access_denied(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.add_resource_to_curriculum.return_value = True
        mock_instance.get_curriculum.return_value = self.mongoTestData
        mock_instance.getMentor.return_value = "aaaa00000000000000000012"

        # Test with failing tokens
        for token in self.rejectTokens:
            with self.assertRaises(Exception) as context:
                CurriculumService.add_resource_to_curriculum(
                    "aaaa00000000000000000001", 
                    copy.deepcopy(self.stringTestResource1),
                    token, 
                    self.mongoBreadcrumb
                )
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_update_curriculum_success(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.update_curriculum.return_value = True
        mock_instance.get_curriculum.return_value = self.mongoTestData
        mock_instance.getMentor.return_value = "aaaa00000000000000000012"

        # Test with passing tokens
        for token in self.goodTokens:
            curriculum = CurriculumService.update_curriculum(
                "aaaa00000000000000000001", 
                100, 
                copy.deepcopy(self.stringTestResource1), 
                token,
                self.mongoBreadcrumb
            )
            mock_instance.update_curriculum.assert_called_once_with(
                "aaaa00000000000000000001",
                100,
                self.mongoTestResource1,
                self.mongoBreadcrumb
            )
            mock_instance.get_curriculum.assert_called_once_with("aaaa00000000000000000001")
            self.assertEqual(curriculum, self.stringTestData)
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_update_curriculum_access_denied(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.update_curriculum.return_value = True
        mock_instance.get_curriculum.return_value = self.mongoTestData
        mock_instance.getMentor.return_value = "aaaa00000000000000000012"

        # Test with failing tokens
        for token in self.rejectTokens:
            with self.assertRaises(Exception) as context:
                CurriculumService.update_curriculum(
                    "aaaa00000000000000000001", 
                    100,
                    copy.deepcopy(self.stringTestResource1),
                    token, 
                    self.mongoBreadcrumb
                )
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_delete_resource_from_curriculum_success(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.delete_resource_from_curriculum.return_value = True
        mock_instance.get_curriculum.return_value = self.mongoTestData
        mock_instance.getMentor.return_value = "aaaa00000000000000000012"

        # Test with passing tokens
        for token in self.goodTokens:
            curriculum = CurriculumService.delete_resource_from_curriculum(
                "aaaa00000000000000000001", 
                100,
                token,
                self.mongoBreadcrumb
            )
            mock_instance.delete_resource_from_curriculum.assert_called_once_with(
                "aaaa00000000000000000001",
                100,
                self.mongoBreadcrumb
            )
            mock_instance.get_curriculum.assert_called_once_with("aaaa00000000000000000001")
            self.assertEqual(curriculum, self.stringTestData)
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_delete_resource_from_curriculum_access_denied(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.delete_resource_from_curriculum.return_value = True
        mock_instance.get_curriculum.return_value = self.mongoTestData
        mock_instance.getMentor.return_value = "aaaa00000000000000000012"

        # Test with failing tokens
        for token in self.rejectTokens:
            with self.assertRaises(Exception) as context:
                CurriculumService.delete_resource_from_curriculum(
                    "aaaa00000000000000000001", 
                    100,
                    token, 
                    self.mongoBreadcrumb
                )
            mock_instance.reset_mock()

if __name__ == '__main__':
    unittest.main()