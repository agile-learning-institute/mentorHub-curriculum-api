import unittest
from unittest.mock import patch
from src.services.topics_services import TopicService

class TestTopicsService(unittest.TestCase):
    
    @patch('src.services.topics_services.mentorhub_mongoIO')
    def test_get_topic_success(self, mock_mentorhub_mongo_io):
        # Mock the MongoIO methods
        mock_mentorhub_mongo_io.get_document.return_value = {"test": "document"}

        document = TopicService.get_topic("topic_id", {})
        self.assertEqual(document, {"test":"document"})

    @patch('src.services.topics_services.mentorhub_mongoIO')
    def test_get_topics_success(self, mock_mentorhub_mongo_io):
        
        # Mock the MongoIO methods
        mock_mentorhub_mongo_io.get_documents.return_value = [{"test": "document"}]

        documents = TopicService.get_topics("", {})
        self.assertEqual(documents, [{"test":"document"}])

if __name__ == '__main__':
    unittest.main()