import unittest
from src.config.config import config
from src.utils.mongo_io import MongoIO

class TestMongoIO(unittest.TestCase):
    
    def setUp(self):
        # Ensuring we start with a fresh instance for each test
        MongoIO._instance = None
        mongo_io = MongoIO.get_instance()
        mongo_io.initialize()

    def tearDown(self):
        mongo_io = MongoIO.get_instance()
        mongo_io.disconnect()
    
    def test_singleton_behavior(self):
        # Test that MongoIO is a singleton
        mongo_io1 = MongoIO.get_instance()
        mongo_io2 = MongoIO.get_instance()
        self.assertIs(mongo_io1, mongo_io2, "MongoIO should be a singleton")

    def test_config_loaded(self):
        # Test that MongoIO is a singleton
        self.assertIsInstance(config.versions, list)
        self.assertEqual(len(config.versions), 11)

        self.assertIsInstance(config.enumerators, dict)
        self.assertIsInstance(config.enumerators.get("roadmap"), dict)
        roadmaps = config.enumerators.get("roadmap")
        self.assertEqual(roadmaps.get("Completed"), "A resource that has been marked as completed")
        self.assertEqual(roadmaps.get("Now"), "A resources that an apprentice is currently assigned")
        self.assertEqual(roadmaps.get("Next"), "Resources we think we may do next")
        self.assertEqual(roadmaps.get("Later"), "Resources that might come later")

    def test_get_curriculum(self):
        # Test get_curriculum method
        mongo_io = MongoIO.get_instance()
        curriculum = mongo_io.get_curriculum("AAAA00000000000000000001")
        self.assertIsInstance(curriculum, dict)
        self.assertEqual(curriculum.get("_id"), "AAAA00000000000000000001")        
        self.assertIsInstance(curriculum.get("lastSaved"), dict)
        lastSaved = curriculum["lastSaved"]
        self.assertEqual(lastSaved.get("atTime"), "2/27/2024 18:17:58")
        self.assertEqual(lastSaved.get("byUser"), "AAAA00000000000000000001")
        self.assertEqual(lastSaved.get("fromIp"), "192.168.1.3")
        self.assertEqual(lastSaved.get("correlationId"), "ae078031-7de2-4519-bcbe-fbd5e72b69d3")

        self.assertIsInstance(curriculum.get("resources"), list)
        self.assertEqual(len(curriculum["resources"]), 7)
        
        resources = curriculum["resources"]
        self.assertEqual(resources[0].sequence, 1)
        self.assertEqual(resources[0].roadmap, "Completed")
        self.assertEqual(resources[0].path, "The Odin Project")
        self.assertEqual(resources[0].segment, "Foundations")
        self.assertEqual(resources[0].topic, "OdinIntro")
        self.assertEqual(resources[0].type, "Resource")
        self.assertEqual(resources[0].resourceid, "CCCC00000000000000000008")
        self.assertEqual(resources[1].name, "JeanBartikandtheENIACWom")
        self.assertEqual(resources[1].link, "https://www.markdowntutorial.com/lesson/1/")
        self.assertEqual(resources[0].started, "2024-07-01 1:00PM")
        self.assertEqual(resources[0].completed, "2024-07-01 4:30PM")
        self.assertEqual(resources[0].rating, 4)
        self.assertEqual(resources[0].review, "This was a great intro")
        
        self.assertEqual(resources[1].sequence, 2)
        self.assertEqual(resources[1].roadmap, "Completed")
        self.assertEqual(resources[1].path, "The Odin Project")
        self.assertEqual(resources[1].segment, "Foundations")
        self.assertEqual(resources[1].topic, "OdinIntro")
        self.assertEqual(resources[1].type, "Adhoc")
        self.assertEqual(resources[1].resource_name, "Markdown Tutorial")
        self.assertEqual(resources[1].resource_url, "https://www.markdowntutorial.com/lesson/1/")
        self.assertEqual(resources[1].started, "2024-07-02 1:00 PM")
        self.assertEqual(resources[1].completed, "2024-07-03 7:36 PM")
        self.assertEqual(resources[1].rating, 3)
        self.assertEqual(resources[1].review, "I had to read this twice before it made sense")
        
        self.assertEqual(resources[6].sequence, 7)
        self.assertEqual(resources[6].roadmap, "Later")
        self.assertEqual(resources[6].path, "EngineerKit")
        self.assertEqual(resources[6].segment, "Craftsmanship")
        self.assertEqual(resources[6].type, "Resource")
        self.assertEqual(resources[0].resourceid, "CCCC00000000000000000010")   
        self.assertEqual(resources[1].name, "DigitalLogicSimTool")
        self.assertEqual(resources[1].link, "https://somevalidlink10.com")
     
        
    def test_create_curriculum(self):
        # Test create_curriculum method
        mongo_io = MongoIO.get_instance()
        curriculum = mongo_io.create_curriculum("AAAA00000000000000000002")
        self.assertIsInstance(curriculum, dict)
        self.assertEqual(curriculum.get("_id"), "AAAA00000000000000000002")
        self.assertIsInstance(curriculum.get("resources"), list)
        self.assertEqual(len(curriculum["resources"]), 0)
        self.assertIsInstance(curriculum.get("lastSaved"), dict)
        self.assertIsInstance(curriculum.get("lastSaved").get("atTime"), str)
        self.assertIsInstance(curriculum.get("lastSaved").get("byUser"), str)
        self.assertIsInstance(curriculum.get("lastSaved").get("fromIp"), str)
        self.assertIsInstance(curriculum.get("lastSaved").get("correlationId"), str)

    def test_add_resource_to_curriculum(self):
        # Test add_resource_to_curriculum method
        mongo_io = MongoIO.get_instance()
        resource = mongo_io.add_resource_to_curriculum("AAAA00000000000000000002", 
            {
                "sequence": 1,
                "roadmap": "Completed",
                "path": "The Odin Project",
                "segment": "Foundations",
                "topic": "OdinIntro",
                "type": "Adhoc",
                "resource_name": "Markdown Tutorial",
                "resource_url": "https://www.markdowntutorial.com/lesson/1/",
                "started": "2024-07-02 1:00 PM",
                "completed": "2024-07-03 7:36 PM",
                "rating": 3,
                "review": "I had to read this twice before it made sense"
            })

        self.assertIsInstance(resource, dict)
        self.assertNotIn('method', resource)  #Rule out Mock Data
        self.assertEqual(resource.get("roadmap"), "Completed")
        self.assertEqual(resource.get("path"), "The Odin Project")
        self.assertEqual(resource.get("segment"), "Foundations")
        self.assertEqual(resource.get("topic"), "OdinIntro")
        self.assertEqual(resource.get("type"), "Adhoc")
        self.assertEqual(resource.get("resource_name"), "Markdown Tutorial")
        self.assertEqual(resource.get("resource_url"), "https://www.markdowntutorial.com/lesson/1/")
        self.assertEqual(resource.get("started"), "2024-07-02 1:00 PM")
        self.assertEqual(resource.get("completed"), "2024-07-03 7:36 PM")
        self.assertEqual(resource.get("rating"), 3)
        self.assertEqual(resource.get("review"), "I had to read this twice before it made sense")

    def test_update_curriculum(self):
        # Test update_curriculum method
        mongo_io = MongoIO.get_instance()
        resource = mongo_io.update_curriculum("AAAA00000000000000000002", 1, 
            {
                "rating": "1"
            })
        
        self.assertIsInstance(resource, dict)
        self.assertNotIn('method', resource)  #Rule out Mock Data
        self.assertEqual(resource.get("method"), "add_resource_to_curriculum")
        self.assertEqual(resource.get("roadmap"), "Completed")
        self.assertEqual(resource.get("path"), "The Odin Project")
        self.assertEqual(resource.get("segment"), "Foundations")
        self.assertEqual(resource.get("topic"), "OdinIntro")
        self.assertEqual(resource.get("type"), "Adhoc")
        self.assertEqual(resource.get("resource_name"), "Markdown Tutorial")
        self.assertEqual(resource.get("resource_url"), "https://www.markdowntutorial.com/lesson/1/")
        self.assertEqual(resource.get("started"), "2024-07-02 1:00 PM")
        self.assertEqual(resource.get("completed"), "2024-07-03 7:36 PM")
        self.assertEqual(resource.get("rating"), 1)
        self.assertEqual(resource.get("review"), "I had to read this twice before it made sense")


    def test_delete_resource_from_curriculum(self):
        # Test delete_resource_from_curriculum method
        mongo_io = MongoIO.get_instance()
        curriculum = mongo_io.delete_resource_from_curriculum("AAAA00000000000000000002", 1)
        self.assertIsInstance(curriculum, dict)
        self.assertNotIn('method', curriculum)  #Rule out Mock Data
        self.assertEqual(curriculum.get("_id"), "AAAA00000000000000000002")
        self.assertIsInstance(curriculum.get("resources"), list)
        self.assertEqual(len(curriculum.get("resources")), 0)
        self.assertIsInstance(curriculum.get("lastSaved"), dict)
        
if __name__ == '__main__':
    unittest.main()
    
