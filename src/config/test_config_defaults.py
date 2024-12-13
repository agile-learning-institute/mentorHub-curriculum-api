import json
import unittest
from src.config.Config import config

class TestConfigDefaults(unittest.TestCase):

    def setUp(self):
        """Re-initialize the config for each test."""
        config.initialize()

    def test_default_string_properties(self):
        for key, default in config.config_strings.items():
            self.assertEqual(getattr(config, key), default)

    def test_default_int_properties(self):
        for key, default in config.config_ints.items():
            self.assertEqual(getattr(config, key), int(default))

    def test_default_string_secret_properties(self):
        for key, default in config.config_string_secrets.items():
            self.assertEqual(getattr(config, key), default)

    def test_default_json_secret_properties(self):
        for key, default in config.config_json_secrets.items():
            self.assertEqual(getattr(config, key), json.loads(default))

    def test_to_dict(self):
        """Test the to_dict method of the Config class."""
        # Convert the config object to a dictionary
        result_dict = config.to_dict({})
        self.assertIsInstance(result_dict["config_items"], list)
        self.assertIsInstance(result_dict["versions"], list)
        self.assertIsInstance(result_dict["enumerators"], dict)
        self.assertIsInstance(result_dict["token"], dict)
        
    def test_default_string_ci(self):
        for key, default in {**config.config_strings, **config.config_ints}.items():
            self._test_config_default_value(key, default)

    def test_default_secret_ci(self):
        for key, default in {**config.config_string_secrets, **config.config_json_secrets}.items():
            self._test_config_default_value(key, "secret")

    def _test_config_default_value(self, config_name, expected_value):
        """Helper function to check default values."""
        items = config.config_items
        item = next((i for i in items if i['name'] == config_name), None)
        self.assertIsNotNone(item)
        self.assertEqual(item['name'], config_name)
        self.assertEqual(item['from'], "default")
        self.assertEqual(item['value'], expected_value)

if __name__ == '__main__':
    unittest.main()