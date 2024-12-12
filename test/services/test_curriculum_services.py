import copy
from datetime import datetime, timezone
import unittest
from unittest.mock import patch

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
        
        self.breadcrumb = {"atTime":datetime.fromisoformat("2024-08-01T12:00:00"),"byUser":ObjectId("aaaa00000000000000000001"),"fromIp":"127.0.0.1","correlationId":"aaaa-aaaa-aaaa-aaaa"}
        self.completed = [{"name":"JeanBartikandtheENIACWom","link":"https://somevalidlink08.com","description":"test description1","started":datetime.fromisoformat("2024-07-01T13:00:00"),"completed":datetime.fromisoformat("2024-07-01T14:30:00"),"rating":4,"review":"This was a great intro"},{"name":"Markdown Tutorial","link":"https://www.markdowntutorial.com/lesson/1/","description":"test description2","started":datetime.fromisoformat("2024-07-02T13:00:00"),"completed":datetime.fromisoformat("2024-07-03T19:36:00"),"rating":3,"review":"I had to read this twice before it made sense"}]
        self.now = [{"name":"AWSStorageResource","link":"https://somevalidlink.35.com","description":"foo","started":datetime.fromisoformat("2024-07-15T13:00:00")},{"name":"Some Unique Resource","link":"https://some.com/resource","description":"bar"}]
        self.next_one = [{"path":"The Odin Project","segments":[{"segment":"Intermediate HTML and CSS","topics":[{"topic":"Intermediate HTML","resources":[{"name":"A one-off resource","description":"test","link":"https://some.com/resource"}]}]}]}]
        self.later = [ObjectId("999900000000000000000000"),ObjectId("999900000000000000000001"),ObjectId("999900000000000000000003")]
        self.test_curriculum_one = {"_id":ObjectId("aaaa00000000000000000001"),"completed":self.completed,"now":self.now,"next":self.next_one,"later":self.later,"lastSaved":self.breadcrumb}
        
        self.empty_curriculum = {"_id":ObjectId("aaaa00000000000000000999"),"completed":[],"now":[],"next":[],"later":[],"lastSaved":self.breadcrumb}
        self.next_two = [{"path":"The Odin Project","segments":[{"segment":"Intermediate HTML and CSS","topics":[{"topic":"Intermediate HTML","resources":[{"name":"Howdocomputersreadcode?V","link":"https://somevalidlink.22.com","description":"test-it1"},{"name":"A one-off resource","link":"https://some.com/resource","description":"test-it2"}]}]}]}]
        self.test_curriculum_two = {"_id":ObjectId("aaaa00000000000000000001"),"completed":self.completed,"now":self.now,"next":self.next_two,"later":self.later,"lastSaved":self.breadcrumb}
        
    @patch('src.services.curriculum_services.MongoIO')
    def test_get_or_create_curriculum_existing_success(self, mock_mongo_io):
        # Test with passing tokens
        
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.get_curriculum.return_value = self.test_curriculum_one
        mock_instance.get_mentor.return_value = "aaaa00000000000000000012"

        for token in self.goodTokens:
            curriculum = CurriculumService.get_or_create_curriculum("aaaa00000000000000000001", token, self.breadcrumb)
            mock_instance.get_curriculum.assert_called_once_with("aaaa00000000000000000001")
            self.assertEqual(curriculum, self.test_curriculum_one)
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_get_or_create_curriculum_new_success(self, mock_mongo_io):
        mock_instance = mock_mongo_io.return_value

        # Test with passing tokens
        for token in self.goodTokens:
            # Initilize the MongoIO mock methods
            mock_instance.get_curriculum.side_effect = [None, self.empty_curriculum]
            mock_instance.create_curriculum.return_value = self.empty_curriculum
            mock_instance.get_mentor.return_value = "aaaa00000000000000000012"
            
            # Call get_or_create_curriculum and test results
            curriculum = CurriculumService.get_or_create_curriculum("aaaa00000000000000000001", token, self.breadcrumb)
            self.assertEqual(mock_instance.get_curriculum.call_count, 2)
            mock_instance.create_curriculum.assert_called_once_with("aaaa00000000000000000001", self.breadcrumb)
            self.assertEqual(curriculum, self.empty_curriculum)
            mock_instance.get_curriculum.reset_mock()
            mock_instance.create_curriculum.reset_mock()
            
    @patch('src.services.curriculum_services.MongoIO')
    def test_update_curriculum_success(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.update_curriculum.return_value = True
        mock_instance.get_curriculum.side_effect = lambda *args, **kwargs: copy.deepcopy(self.test_curriculum_one)
        mock_instance.get_mentor.return_value = "aaaa00000000000000000012"

        # Test with passing tokens
        for token in self.goodTokens:
            curriculum = CurriculumService.update_curriculum("aaaa00000000000000000001", {"now": []}, token,self.breadcrumb)
            mock_instance.update_curriculum.assert_called_once_with("aaaa00000000000000000001",{"now": [], "lastSaved": self.breadcrumb})
            mock_instance.get_curriculum.assert_called_once_with("aaaa00000000000000000001")
            self.assertEqual(curriculum, self.test_curriculum_one)
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_delete_curriculum_success(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.delete_curriculum.return_value = True
        mock_instance.get_mentor.return_value = "aaaa00000000000000000012"

        # Test with passing token (Staff Only)
        goodToken = {"user_id":"000000000000000000000000", "roles":["Staff"]}
        CurriculumService.delete_curriculum("aaaa00000000000000000001", goodToken)
        mock_instance.delete_curriculum.assert_called_once_with("aaaa00000000000000000001")

    @patch('src.services.curriculum_services.MongoIO')
    def test_assign_resource_simple_success(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.update_curriculum.return_value = True
        mock_instance.get_mentor.return_value = "aaaa00000000000000000012"
        mock_instance.get_curriculum.side_effect = lambda *args, **kwargs: copy.deepcopy(self.test_curriculum_two)

        # Test with passing tokens
        for token in self.goodTokens:
            # Promote one of two resources, no containers removed
            curriculum = CurriculumService.assign_resource("aaaa00000000000000000001", "https://somevalidlink.22.com", token, self.breadcrumb)
            expected = {"now":[{"name":"AWSStorageResource","link":"https://somevalidlink.35.com","description":"foo","started":datetime.fromisoformat("2024-07-15T13:00:00")},{"name":"Some Unique Resource","link":"https://some.com/resource","description":"bar"},{"name":"Howdocomputersreadcode?V","link":"https://somevalidlink.22.com","description":"test-it1"}],"next":[{"path":"The Odin Project","segments":[{"segment":"Intermediate HTML and CSS","topics":[{"topic":"Intermediate HTML","resources":[{"name":"A one-off resource","link":"https://some.com/resource","description":"test-it2"}]}]}]}],"lastSaved":self.breadcrumb}
            
            mock_instance.update_curriculum.assert_called_once_with("aaaa00000000000000000001", expected)
            self.assertEqual(mock_instance.get_curriculum.call_count, 2)
            self.assertEqual(curriculum, self.test_curriculum_two)
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_assign_resource_cleaning_success(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.update_curriculum.return_value = True
        mock_instance.get_mentor.return_value = "aaaa00000000000000000012"
        mock_instance.get_curriculum.side_effect = lambda *args, **kwargs: copy.deepcopy(self.test_curriculum_one)

        # Test with passing tokens
        for token in self.goodTokens:
            # Promote one of one resources containers removed
            curriculum = CurriculumService.assign_resource("aaaa00000000000000000001", "https://some.com/resource", token,self.breadcrumb)
            expected = {"now":[{"name":"AWSStorageResource","link":"https://somevalidlink.35.com","description":"foo","started":datetime.fromisoformat("2024-07-15T13:00:00")},{"name":"Some Unique Resource","link":"https://some.com/resource","description":"bar"},{"name":"A one-off resource","description":"test","link":"https://some.com/resource"}],"next":[],"lastSaved":self.breadcrumb}
            mock_instance.update_curriculum.assert_called_once_with("aaaa00000000000000000001", expected)
            self.assertEqual(mock_instance.get_curriculum.call_count, 2)
            self.assertEqual(curriculum, self.test_curriculum_one)
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.datetime')
    @patch('src.services.curriculum_services.MongoIO')
    def test_complete_resource_with_rating_success(self, mock_mongo_io, mock_datetime):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_datetime.now.return_value = datetime.fromisoformat("2024-01-01T12:34:56")
        mock_instance.get_mentor.return_value = "aaaa00000000000000000012"
        mock_instance.get_curriculum.side_effect = lambda *args, **kwargs: copy.deepcopy(self.test_curriculum_one)

        # Test with passing tokens
        for token in self.goodTokens:        
            curriculum = CurriculumService.complete_resource("aaaa00000000000000000001", "https://somevalidlink.35.com", {"rating": 4, "review": "Nice"},token,self.breadcrumb)
            self.assertEqual(curriculum, self.test_curriculum_one)
            expected = {"completed":[{"name":"JeanBartikandtheENIACWom","link":"https://somevalidlink08.com","description":"test description1","started":datetime.fromisoformat("2024-07-01T13:00:00"),"completed":datetime.fromisoformat("2024-07-01T14:30:00"),"rating":4,"review":"This was a great intro"},{"name":"Markdown Tutorial","link":"https://www.markdowntutorial.com/lesson/1/","description":"test description2","started":datetime.fromisoformat("2024-07-02T13:00:00"),"completed":datetime.fromisoformat("2024-07-03T19:36:00"),"rating":3,"review":"I had to read this twice before it made sense"},{"name":"AWSStorageResource","link":"https://somevalidlink.35.com","description":"foo","started":datetime.fromisoformat("2024-07-15T13:00:00"),"completed":datetime.fromisoformat("2024-01-01T12:34:56"),"rating":4,"review":"Nice"}],"now":[{"name":"Some Unique Resource","link":"https://some.com/resource","description":"bar"}],"lastSaved":self.breadcrumb}
            mock_instance.update_curriculum.assert_called_once_with("aaaa00000000000000000001", expected)
            self.assertEqual(mock_instance.get_curriculum.call_count, 2)
            self.assertEqual(curriculum, self.test_curriculum_one)
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.datetime')
    @patch('src.services.curriculum_services.MongoIO')
    def test_complete_resource_without_rating_success(self, mock_mongo_io, mock_datetime):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_datetime.now.return_value = datetime.fromisoformat("2024-01-01T12:34:56")
        mock_instance.get_mentor.return_value = "aaaa00000000000000000012"
        mock_instance.get_curriculum.side_effect = lambda *args, **kwargs: copy.deepcopy(self.test_curriculum_one)

        # Test with passing tokens
        for token in self.goodTokens:        
            curriculum = CurriculumService.complete_resource("aaaa00000000000000000001", "https://some.com/resource", {},token,self.breadcrumb)
            self.assertEqual(mock_instance.get_curriculum.call_count, 2)
            self.assertEqual(curriculum, self.test_curriculum_one)
            expected = {"completed":[{"name":"JeanBartikandtheENIACWom","link":"https://somevalidlink08.com","description":"test description1","started":datetime.fromisoformat("2024-07-01T13:00:00"),"completed":datetime.fromisoformat("2024-07-01T14:30:00"),"rating":4,"review":"This was a great intro"},{"name":"Markdown Tutorial","link":"https://www.markdowntutorial.com/lesson/1/","description":"test description2","started":datetime.fromisoformat("2024-07-02T13:00:00"),"completed":datetime.fromisoformat("2024-07-03T19:36:00"),"rating":3,"review":"I had to read this twice before it made sense"},{"name":"Some Unique Resource","link":"https://some.com/resource","description":"bar","completed":datetime.fromisoformat("2024-01-01T12:34:56")}],"now":[{"name":"AWSStorageResource","link":"https://somevalidlink.35.com","description":"foo","started":datetime.fromisoformat("2024-07-15T13:00:00")}],"lastSaved":self.breadcrumb}
            mock_instance.update_curriculum.assert_called_once_with("aaaa00000000000000000001", expected)
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_add_path_success(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.update_curriculum.return_value = True
        mock_instance.get_path.return_value = self.next_two
        mock_instance.get_mentor.return_value = "aaaa00000000000000000012"
        mock_instance.get_curriculum.side_effect = lambda *args, **kwargs: copy.deepcopy(self.empty_curriculum)

        # Test with passing tokens
        for token in self.goodTokens:
            curriculum = CurriculumService.add_path("aaaa00000000000000000001", "cccc00000000000000000001", token,self.breadcrumb)
            self.assertEqual(mock_instance.get_curriculum.call_count, 2)
            self.assertEqual(curriculum, self.empty_curriculum)
            expected = {"next":self.next_two,"lastSaved":self.breadcrumb}
            mock_instance.update_curriculum.assert_called_once_with("aaaa00000000000000000001", expected)
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_get_or_create_curriculum_existing_access_denied(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value

        # Test with failing tokens
        for token in self.rejectTokens:
            with self.assertRaises(Exception) as context:
                CurriculumService.get_or_create_curriculum("", {}, {})
            mock_instance.reset_mock()
                    
    @patch('src.services.curriculum_services.MongoIO')
    def test_get_or_create_curriculum_new_access_denied(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value

        # Test with failing tokens
        for token in self.rejectTokens:
            with self.assertRaises(Exception) as context:
                CurriculumService.get_or_create_curriculum("", {}, {})
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_update_curriculum_access_denied(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value

        # Test with failing tokens
        for token in self.rejectTokens:
            with self.assertRaises(Exception) as context:
                CurriculumService.update_curriculum("", {}, {}, {})
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_delete_curriculum_access_denied(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.delete_curriculum.return_value = True
        mock_instance.get_mentor.return_value = "aaaa00000000000000000012"

        # Test with failing token
        badToken = {"user_id":"000000000000000000000000", "roles":["Member", "Mentor"]}
        with self.assertRaises(Exception) as context:
                CurriculumService.delete_curriculum("aaaa00000000000000000001", badToken)
    
    @patch('src.services.curriculum_services.MongoIO')
    def test_assign_resource_access_denied(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value

        # Test with failing tokens
        for token in self.rejectTokens:
            with self.assertRaises(Exception) as context:
                CurriculumService.assign_resource("", "", {}, {})
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_complete_resource_access_denied(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value

        # Test with failing tokens
        for token in self.rejectTokens:
            with self.assertRaises(Exception) as context:
                CurriculumService.complete_resource("", "", {}, {}, {})
            mock_instance.reset_mock()

    @patch('src.services.curriculum_services.MongoIO')
    def test_add_path_access_denied(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value

        # Test with failing tokens
        for token in self.rejectTokens:
            with self.assertRaises(Exception) as context:
                CurriculumService.add_path("", "", {}, {})
            mock_instance.reset_mock()

if __name__ == '__main__':
    unittest.main()