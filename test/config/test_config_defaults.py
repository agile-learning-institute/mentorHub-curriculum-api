import unittest
from src.config.config import config

class TestConfigDefaults(unittest.TestCase):

    def setUp(self):
        """Re-initialize the config for each test."""
        config.initialize()

    def test_default_properties_in_getters(self):
        self.assertEqual(config.get_config_folder(), "/opt/mentorhub-partner-api")
        self.assertEqual(config.get_port(), 8088)
        self.assertEqual(config.get_db_name(), "mentorHub")
        self.assertEqual(config.get_curriculum_collection_name(), "curriculum")
        self.assertEqual(config.get_topics_collection_name(), "topics")
        self.assertEqual(config.get_paths_collection_name(), "paths")
        self.assertEqual(config.get_version_collection_name(), "msmCurrentVersions")
        self.assertEqual(config.get_enumerators_collection_name(), "enumerators")

    def test_default_config_items(self):
        self._test_config_default_value("PORT", "8088")
        self._test_config_default_value("BUILT_AT", "LOCAL")
        self._test_config_default_value("CONFIG_FOLDER", "/opt/mentorhub-partner-api")
        self._test_config_default_value("DB_NAME", "mentorHub")
        self._test_config_default_value("CURRICULUM_COLLECTION", "curriculum")
        self._test_config_default_value("TOPICS_COLLECTION", "topics")
        self._test_config_default_value("PATHS_COLLECTION", "paths")
        self._test_config_default_value("VERSION_COLLECTION", "msmCurrentVersions")
        self._test_config_default_value("ENUMERATORS_COLLECTION", "enumerators")

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