import unittest
from unittest.mock import MagicMock, patch
from src.services.paths_services import PathsService

class TestPathsService(unittest.TestCase):
    
    @patch('mentorhub_utils.MentorHubMongoIO.get_instance')
    def test_get_path_success(self, mock_get_instance):
        # Mock the MongoIO methods
        mock_mongo_io = MagicMock()
        mock_get_instance.return_value = mock_mongo_io
        mock_mongo_io.get_document.return_value = {"test": "document"}

        document = PathsService.get_path("000000000000000000000000", {})
        self.assertEqual(document, {"test":"document"})

    @patch('mentorhub_utils.MentorHubMongoIO.get_instance')
    def test_get_paths_success(self, mock_get_instance):
        
        # Mock the MongoIO methods
        mock_mongo_io = MagicMock()
        mock_get_instance.return_value = mock_mongo_io
        mock_mongo_io.get_documents.return_value = [{"test": "document"}]

        documents = PathsService.get_paths("", {})
        self.assertEqual(documents, [{"test":"document"}])

if __name__ == '__main__':
    unittest.main()