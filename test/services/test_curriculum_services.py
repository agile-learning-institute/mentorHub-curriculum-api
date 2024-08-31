import unittest
from unittest.mock import patch, MagicMock
from src.services.curriculum_services import CurriculumService
from src.utils.mongo_io import MongoIO

class TestCurriculumService(unittest.TestCase):

    @patch('src.services.curriculum_services.MongoIO')
    def test_get_or_create_curriculum_existing(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.get_curriculum.return_value = {"id": "AAAA00000000000000000001", "name": "Sample Curriculum"}

        curriculum = CurriculumService.get_or_create_curriculum("AAAA00000000000000000001")
        self.assertEqual(curriculum["id"], "AAAA00000000000000000001")
        self.assertEqual(curriculum["name"], "Sample Curriculum")
        mock_instance.get_curriculum.assert_called_once_with("AAAA00000000000000000001")
        mock_instance.create_curriculum.assert_not_called()

    @patch('src.services.curriculum_services.MongoIO')
    def test_get_or_create_curriculum_new(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.get_curriculum.return_value = None
        mock_instance.create_curriculum.return_value = {"id": "AAAA00000000000000000002", "name": "New Curriculum"}

        curriculum = CurriculumService.get_or_create_curriculum("AAAA00000000000000000002")
        self.assertEqual(curriculum["id"], "AAAA00000000000000000002")
        self.assertEqual(curriculum["name"], "New Curriculum")
        mock_instance.get_curriculum.assert_called_once_with("AAAA00000000000000000002")
        mock_instance.create_curriculum.assert_called_once_with("AAAA00000000000000000002")

    @patch('src.services.curriculum_services.MongoIO')
    def test_add_resource_to_curriculum(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.add_resource_to_curriculum.return_value = {"id": "AAAA00000000000000000001", "resource": "New Resource"}

        resource_data = {"resource": "New Resource"}
        resource = CurriculumService.add_resource_to_curriculum("AAAA00000000000000000001", resource_data, {})
        self.assertEqual(resource["id"], "AAAA00000000000000000001")
        self.assertEqual(resource["resource"], "New Resource")
        mock_instance.add_resource_to_curriculum.assert_called_once_with("AAAA00000000000000000001", resource_data)

    @patch('src.services.curriculum_services.MongoIO')
    def test_update_curriculum(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.update_curriculum.return_value = {"id": "AAAA00000000000000000001", "seq": 100, "resource": "Updated Resource"}

        resource_data = {"resource": "Updated Resource"}
        updated_resource = CurriculumService.update_curriculum("AAAA00000000000000000001", 100, resource_data)
        self.assertEqual(updated_resource["id"], "AAAA00000000000000000001")
        self.assertEqual(updated_resource["seq"], 100)
        self.assertEqual(updated_resource["resource"], "Updated Resource")
        mock_instance.update_curriculum.assert_called_once_with("AAAA00000000000000000001", 100, resource_data)

    @patch('src.services.curriculum_services.MongoIO')
    def test_delete_resource_from_curriculum(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value

        CurriculumService.delete_resource_from_curriculum("AAAA00000000000000000001", 100)
        mock_instance.delete_resource_from_curriculum.assert_called_once_with("AAAA00000000000000000001", 100)

if __name__ == '__main__':
    unittest.main()