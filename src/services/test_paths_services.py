import unittest
from unittest.mock import patch
from src.services.paths_services import PathsService

class TestPathsService(unittest.TestCase):
    
    @patch('src.services.paths_services.mentorhub_mongo_io')
    def test_get_path_success(self, mock_mentorhub_mongo_io):
        # Mock the MongoIO methods
        mock_mentorhub_mongo_io.getDocument.return_value = {"test": "document"}

        document = PathsService.get_path("path_id", {})
        self.assertEqual(document, {"test":"document"})

    @patch('src.services.paths_services.mentorhub_mongo_io')
    def test_get_paths_success(self, mock_mentorhub_mongo_io):
        
        # Mock the MongoIO methods
        mock_mentorhub_mongo_io.getDocuments.return_value = [{"test": "document"}]

        documents = PathsService.get_paths("", {})
        self.assertEqual(documents, [{"test":"document"}])

if __name__ == '__main__':
    unittest.main()