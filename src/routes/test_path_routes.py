import unittest
from flask import Flask
from src.routes.path_routes import create_path_routes
from unittest.mock import patch
from mentorhub_utils.ejson_encoder import MongoJSONEncoder

class TestPathRoutes(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test app and register the blueprint
        self.app = Flask(__name__)
        self.app.json = MongoJSONEncoder(self.app)
        path_routes = create_path_routes()
        self.app.register_blueprint(path_routes, url_prefix='/api/path')
        self.client = self.app.test_client()

    @patch('src.routes.path_routes.PathsService')
    def test_get_paths_success(self, mock_paths_services):
        # Mock the MongoIO methods
        mock_paths_services.get_paths.return_value = [{"foo":"bar"}]

        # Simulate a GET request to the /api/path endpoint
        response = self.client.get('/api/path')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"foo":"bar"}])

    @patch('src.routes.path_routes.PathsService')
    def test_get_path_success(self, mock_paths_services):
        # Mock the MongoIO methods
        mock_paths_services.get_path.return_value = {"foo":"bar"}

        # Simulate a GET request to the /api/path endpoint
        response = self.client.get('/api/path/SomeId')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"foo":"bar"})

if __name__ == '__main__':
    unittest.main()