from datetime import datetime
import unittest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from flask import Flask
from src.routes.curriculum_routes import create_curriculum_routes
from mentorhub_utils.ejson_encoder import MongoJSONEncoder

class TestCurriculumRoutes(unittest.TestCase):

    def setUp(self):
        # Test Data
        self.sample_curriculum_decoded = {"_id":"aaaa00000000000000000001", "date": "2024-07-01 14:30:00", "name": "A sample document"}
        self.sample_curriculum_encoded = {"_id": ObjectId("aaaa00000000000000000001"), "date": datetime.fromisoformat("2024-07-01T14:30:00"), "name": "A sample document"}
        
        # Set up the Flask test app and register the blueprint
        self.app = Flask(__name__)
        self.app.json = MongoJSONEncoder(self.app)        
        curriculum_routes = create_curriculum_routes()
        self.app.register_blueprint(curriculum_routes, url_prefix='/api/curriculum')
        self.client = self.app.test_client()

    @patch('src.routes.curriculum_routes.CurriculumService.get_or_create_curriculum')
    def test_get_or_create_curriculum_success(self, mock_get_or_create):
        # Mock the CurriculumService's get_or_create_curriculum method
        mock_get_or_create.return_value = self.sample_curriculum_encoded

        response = self.client.get('/api/curriculum/AAAA00000000000000000001')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertEqual(data, self.sample_curriculum_decoded)

    @patch('src.routes.curriculum_routes.CurriculumService.update_curriculum')
    def test_update_curriculum_success(self, mock_update):
        # Mock the CurriculumService's update_curriculum method
        mock_update.return_value = self.sample_curriculum_encoded

        response = self.client.patch('/api/curriculum/AAAA00000000000000000001', json={"resource": "Updated Resource"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertEqual(data, self.sample_curriculum_decoded)

    @patch('src.routes.curriculum_routes.CurriculumService.delete_curriculum')
    def test_delete_curriculum_success(self, mock_update):
        # Mock the CurriculumService's delete_curriculum method
        mock_update.delete_curriculum.return_value = {"result": "Success"}

        response = self.client.delete('/api/curriculum/AAAA00000000000000000001')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data, {"result": "Success"})

    @patch('src.routes.curriculum_routes.CurriculumService.assign_resource')
    def test_assign_resource_success(self, mock_update):
        # Mock the CurriculumService's update_curriculum method
        mock_update.return_value = self.sample_curriculum_encoded

        response = self.client.patch('/api/curriculum/AAAA00000000000000000001/assign/link')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertEqual(data, self.sample_curriculum_decoded)

    @patch('src.routes.curriculum_routes.CurriculumService.complete_resource')
    def test_complete_resource_success(self, mock_update):
        # Mock the CurriculumService's update_curriculum method
        mock_update.return_value = self.sample_curriculum_encoded

        response = self.client.patch('/api/curriculum/AAAA00000000000000000001/complete/link')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertEqual(data, self.sample_curriculum_decoded)

    @patch('src.routes.curriculum_routes.CurriculumService.add_path')
    def test_add_path_success(self, mock_update):
        # Mock the CurriculumService's update_curriculum method
        mock_update.return_value = self.sample_curriculum_encoded

        response = self.client.post('/api/curriculum/AAAA00000000000000000001/path/cccc00000000000000000001')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertEqual(data, self.sample_curriculum_decoded)

if __name__ == '__main__':
    unittest.main()