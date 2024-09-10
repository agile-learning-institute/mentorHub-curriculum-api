import unittest
from flask import Flask
from src.routes.topic_routes import create_topic_routes
from unittest.mock import patch

from src.utils.ejson_encoder import MongoJSONEncoder

class TestConfigRoutes(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test app and register the blueprint
        self.app = Flask(__name__)
        self.app.json = MongoJSONEncoder(self.app)
        topic_routes = create_topic_routes()
        self.app.register_blueprint(topic_routes, url_prefix='/api/topic')
        self.client = self.app.test_client()

    @patch('src.routes.topic_routes.MongoIO')
    def test_get_topics_success(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.get_topics.return_value = []

        # Simulate a GET request to the /api/topic endpoint
        response = self.client.get('/api/topic')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    @patch('src.routes.topic_routes.MongoIO')
    def test_get_topic_success(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.get_topic.return_value = {}

        # Simulate a GET request to the /api/topic endpoint
        response = self.client.get('/api/topic/id')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})

if __name__ == '__main__':
    unittest.main()