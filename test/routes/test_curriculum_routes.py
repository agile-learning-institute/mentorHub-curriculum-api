import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from src.routes.curriculum_routes import create_curriculum_routes

class TestCurriculumRoutes(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test app and register the blueprint
        self.app = Flask(__name__)
        curriculum_routes = create_curriculum_routes()
        self.app.register_blueprint(curriculum_routes, url_prefix='/api/curriculum')
        self.client = self.app.test_client()

    @patch('src.routes.curriculum_routes.CurriculumService.get_or_create_curriculum')
    def test_get_or_create_curriculum_success(self, mock_get_or_create):
        # Mock the CurriculumService's get_or_create_curriculum method
        mock_get_or_create.return_value = {"id": "AAAA00000000000000000001", "name": "Sample Curriculum"}

        response = self.client.get('/api/curriculum/AAAA00000000000000000001/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertEqual(data["id"], "AAAA00000000000000000001")
        self.assertEqual(data["name"], "Sample Curriculum")

    @patch('src.routes.curriculum_routes.CurriculumService.add_resource_to_curriculum')
    def test_add_resource_to_curriculum_success(self, mock_add_resource):
        # Mock the CurriculumService's add_resource_to_curriculum method
        mock_add_resource.return_value = {"id": "AAAA00000000000000000001", "resource": "New Resource"}

        response = self.client.post('/api/curriculum/AAAA00000000000000000001/', json={"resource": "New Resource"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertEqual(data["id"], "AAAA00000000000000000001")
        self.assertEqual(data["resource"], "New Resource")

    @patch('src.routes.curriculum_routes.CurriculumService.update_curriculum')
    def test_update_curriculum_success(self, mock_update):
        # Mock the CurriculumService's update_curriculum method
        mock_update.return_value = {"id": "AAAA00000000000000000001", "seq": 100, "resource": "Updated Resource"}

        response = self.client.patch('/api/curriculum/AAAA00000000000000000001/100/', json={"resource": "Updated Resource"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertEqual(data["id"], "AAAA00000000000000000001")
        self.assertEqual(data["seq"], 100)
        self.assertEqual(data["resource"], "Updated Resource")

    @patch('src.routes.curriculum_routes.CurriculumService.delete_resource_from_curriculum')
    def test_delete_resource_from_curriculum_success(self, mock_delete):
        # Mock the CurriculumService's delete_resource_from_curriculum method
        mock_delete.return_value = None

        response = self.client.delete('/api/curriculum/AAAA00000000000000000001/100/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        
        data = response.get_json()

    @patch('src.routes.curriculum_routes.CurriculumService.get_or_create_curriculum')
    def test_get_or_create_curriculum_failure(self, mock_get_or_create):
        # Simulate an exception in the get_or_create_curriculum method
        mock_get_or_create.side_effect = Exception("Mocked exception")

        response = self.client.get('/api/curriculum/AAAA00000000000000000001/')
        self.assertEqual(response.status_code, 500)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "A processing error occurred")

    # Additional tests for other failure scenarios can be added similarly

if __name__ == '__main__':
    unittest.main()