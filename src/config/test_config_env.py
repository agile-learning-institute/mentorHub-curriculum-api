import unittest
import os
from src.config.Config import config

class TestConfigEnvironment(unittest.TestCase):

    def setUp(self):
        """Re-initialize the config for each test."""
        # Set all environment variables to "ENV_VALUE"
        for key, default in {**config.config_strings, **config.config_string_secrets}.items():
            if key != "BUILT_AT" and key != "CONFIG_FOLDER":
                os.environ[key] = "ENV_VALUE"
            
        for key, default in config.config_ints.items():
            os.environ[key] = "1234"

        for key, default in config.config_json_secrets.items():
            os.environ[key] = '{"foo":"bar"}'

        # Initialize the Config object
        config._instance = None
        config.initialize()
        
        # Reset environment variables 
        for key, default in {**config.config_strings, **config.config_ints, **config.config_string_secrets, **config.config_json_secrets}.items():
            if key != "BUILT_AT" and key != "CONFIG_FOLDER":
                del os.environ[key]
            
    def test_env_string_properties(self):
        for key, default in {**config.config_strings, **config.config_string_secrets}.items():
            if key != "BUILT_AT" and key != "CONFIG_FOLDER":
                self.assertEqual(getattr(config, key), "ENV_VALUE")

    def test_env_int_properties(self):
        for key, default in config.config_ints.items():
            self.assertEqual(getattr(config, key), 1234)

    def test_env_json_secret_properties(self):
        for key, default in config.config_json_secrets.items():
            self.assertEqual(getattr(config, key), {"foo":"bar"})

    def test_env_string_ci(self):
        for key, default in config.config_strings.items():
            if key != "BUILT_AT" and key != "CONFIG_FOLDER":
                self._test_config_environment_value(key, "ENV_VALUE")

    def test_env_int_ci(self):
        for key, default in config.config_ints.items():
            self._test_config_environment_value(key, "1234")

    def test_env_secret_ci(self):
        for key, default in {**config.config_string_secrets, **config.config_json_secrets}.items():
            self._test_config_environment_value(key, "secret")

    def _test_config_environment_value(self, ci_name, value):
        """Helper function to check environment values."""
        items = config.config_items
        item = next((i for i in items if i['name'] == ci_name), None)
        self.assertIsNotNone(item)
        self.assertEqual(item['name'], ci_name)
        self.assertEqual(item['value'], value)
        self.assertEqual(item['from'], "environment")

if __name__ == '__main__':
    unittest.main()