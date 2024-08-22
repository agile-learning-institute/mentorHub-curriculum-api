import unittest
from src.utils.mongo_io import MongoIO

class TestMongoIO(unittest.TestCase):

    
    def setUp(self):
        # Ensuring we start with a fresh instance for each test
        MongoIO._instance = None

    def tearDown(self):
        mongo_io = MongoIO.get_instance()
        mongo_io.disconnect()
    
    def test_singleton_behavior(self):
        # Test that MongoIO is a singleton
        mongo_io1 = MongoIO.get_instance()
        mongo_io2 = MongoIO.get_instance()
        self.assertIs(mongo_io1, mongo_io2, "MongoIO should be a singleton")

    # def test_connect_method(self):
    #     # Test the connect method (assuming it's setting up a connection)
    #     mongo_io = MongoIO.get_instance()
    #     self.assertIsNotNone(mongo_io.client, "MongoIO should have a MongoClient instance after connecting")
    #     self.assertIsNotNone(mongo_io.db, "MongoIO should have a database instance after connecting")

    # def test_disconnect_method(self):
    #     # Test the disconnect method
    #     mongo_io = MongoIO.get_instance()
    #     mongo_io.disconnect()
    #     with self.assertRaises(AttributeError):
    #         _ = mongo_io.client.server_info()

    # def test_load_versions(self):
    #     # Test the load_versions method
    #     mongo_io = MongoIO.get_instance()
    #     mongo_io.load_versions()
    #     self.assertIsInstance(mongo_io.db, dict, "Versions should be loaded into config.versions as a list")

    # def test_load_enumerators(self):
    #     # Test the load_enumerators method
    #     mongo_io = MongoIO.get_instance()
    #     mongo_io.load_enumerators()
    #     self.assertIsInstance(config.enumerators, dict, "Enumerators should be loaded into config.enumerators as a dictionary")

    def test_get_curriculum(self):
        # Test get_curriculum method
        mongo_io = MongoIO.get_instance()
        curriculum = mongo_io.get_curriculum("AAAA00000000000000000001")
        self.assertEqual(curriculum["method"], "get_curriculum")

    def test_create_curriculum(self):
        # Test create_curriculum method
        mongo_io = MongoIO.get_instance()
        curriculum = mongo_io.create_curriculum("AAAA00000000000000000002")
        self.assertEqual(curriculum["method"], "create_curriculum")

    def test_add_resource_to_curriculum(self):
        # Test add_resource_to_curriculum method
        mongo_io = MongoIO.get_instance()
        resource = mongo_io.add_resource_to_curriculum("AAAA00000000000000000001", {"resource": "New Resource"})
        self.assertEqual(resource["method"], "add_resource_to_curriculum")

    def test_update_curriculum(self):
        # Test update_curriculum method
        mongo_io = MongoIO.get_instance()
        updated_resource = mongo_io.update_curriculum("AAAA00000000000000000001", 100, {"resource": "Updated Resource"})
        self.assertEqual(updated_resource["method"], "update_curriculum")

    def test_delete_resource_from_curriculum(self):
        # Test delete_resource_from_curriculum method
        mongo_io = MongoIO.get_instance()
        deletion_result = mongo_io.delete_resource_from_curriculum("AAAA00000000000000000001", 100)
        self.assertEqual(deletion_result["method"], "delete_resource_from_curriculum")

if __name__ == '__main__':
    unittest.main()