import unittest
from unittest.mock import MagicMock, patch
from src.services.topics_services import TopicService

class TestTopicsService(unittest.TestCase):
    
    @patch('mentorhub_utils.MentorHubMongoIO.get_instance')
    def test_get_topic_success(self, mock_get_instance):
        # Mock the MongoIO methods
        mock_mongo_io = MagicMock()
        mock_get_instance.return_value = mock_mongo_io
        mock_mongo_io.get_document.return_value = {"test": "document"}

        document = TopicService.get_topic("topic_id", {})
        self.assertEqual(document, {"test":"document"})

    @patch('mentorhub_utils.MentorHubMongoIO.get_instance')
    def test_get_topics_success(self, mock_get_instance):
        
        # Mock the MongoIO methods
        mock_mongo_io = MagicMock()
        mock_get_instance.return_value = mock_mongo_io
        mock_mongo_io.get_documents.return_value = [{"test": "document"}]

        documents = TopicService.get_topics("", {})
        self.assertEqual(documents, [{"test":"document"}])

if __name__ == '__main__':
    unittest.main()