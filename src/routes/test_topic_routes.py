import unittest
from flask import Flask
from src.routes.topic_routes import create_topic_routes
from unittest.mock import patch

from mentorhub_utils.ejson_encoder import MongoJSONEncoder

class TestTopicRoutes(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test app and register the blueprint
        self.app = Flask(__name__)
        self.app.json = MongoJSONEncoder(self.app)
        topic_routes = create_topic_routes()
        self.app.register_blueprint(topic_routes, url_prefix='/api/topic')
        self.client = self.app.test_client()

    @patch('src.routes.path_routes.PathsService')
    def test_get_paths_success(self, mock_paths_services):
        # Mock the MongoIO methods
        mock_paths_services.get_paths.return_value = [{"foo":"bar"}]

    @patch('src.routes.topic_routes.TopicService')
    def test_get_topics_success(self, mock_topics_service):
        # Mock the MongoIO methods
        mock_topics_service.get_topics.return_value = [{"foo":"bar"}]

        # Simulate a GET request to the /api/topic endpoint
        response = self.client.get('/api/topic')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"foo":"bar"}])

    @patch('src.routes.topic_routes.TopicService')
    def test_get_topic_success(self, mock_topics_service):
        # Mock the MongoIO methods
        mock_topics_service.get_topic.return_value = {"foo":"bar"}

        # Simulate a GET request to the /api/topic endpoint
        response = self.client.get('/api/topic/id')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"foo":"bar"})

if __name__ == '__main__':
    unittest.main()