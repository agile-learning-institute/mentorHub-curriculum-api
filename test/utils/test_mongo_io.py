from datetime import datetime, timezone
import unittest

from bson import ObjectId
from src.config.config import config
from src.utils.mongo_io import MongoIO

class TestMongoIO(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff = None
        MongoIO._instance = None
        mongo_io = MongoIO.get_instance()
        mongo_io.initialize()

    def tearDown(self):
        mongo_io = MongoIO.get_instance()
        mongo_io.delete_curriculum("aaaa00000000000000000012")
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

    def test_get_mentor(self):
        mongo_io = MongoIO.get_instance()
        mentor = mongo_io.get_mentor("aaaa00000000000000000001")
        self.assertEqual(mentor, "aaaa00000000000000000007")

    def test_get_all_paths(self):
        mongo_io = MongoIO.get_instance()
        paths = mongo_io.get_paths("")
        expected = [{"_id":"999900000000000000000003","name":"Cantrillo"},{"_id":"999900000000000000000001","name":"EngineerKit"},{"_id":"999900000000000000000004","name":"SRE Speciality"},{"_id":"999900000000000000000002","name":"Salesforce"},{"_id":"999900000000000000000000","name":"The Odin Project"}]
        self.assertEqual(paths, expected)

    def test_get_SRE_paths(self):
        mongo_io = MongoIO.get_instance()
        paths = mongo_io.get_paths("SRE")
        expected = [{"_id":"999900000000000000000004","name":"SRE Speciality"}]
        self.assertEqual(paths, expected)

    def test_get_some_paths(self):
        mongo_io = MongoIO.get_instance()
        paths = mongo_io.get_paths("l")
        expected = [{"_id":"999900000000000000000003","name":"Cantrillo"},{"_id":"999900000000000000000004","name":"SRE Speciality"},{"_id":"999900000000000000000002","name":"Salesforce"}]
        self.assertEqual(paths, expected)

    def test_get_path(self):
        mongo_io = MongoIO.get_instance()
        path = mongo_io.get_path("999900000000000000000003")
        expected = {"name":"Cantrillo","segments":[{"name":"Fundamentals","topics":[{"name":"History of Computing","resources":[{"name":"ComputerHistoryTimelineA","link":"https://somevalidlink02.com"},{"name":"HistoryofComputingArticl","link":"https://somevalidlink03.com"},{"name":"PiratesofSiliconValleyFi","link":"https://somevalidlink04.com"},{"name":"Apple1984SuperBowlCommer","link":"https://somevalidlink05.com"},{"name":"BretVictorTheFutureofPro","link":"https://somevalidlink06.com"},{"name":"AwesomeComputerHistoryRe","link":"https://somevalidlink07.com"},{"name":"JeanBartikandtheENIACWom","link":"https://somevalidlink08.com"}]},{"name":"Hardware","resources":[{"name":"ExploringHowComputersWor","link":"https://somevalidlink09.com"},{"name":"DigitalLogicSimTool","link":"https://somevalidlink10.com"},{"name":"HistoryandTheoryofElectr","link":"https://somevalidlin11.com"},{"name":"Buildingan8-bitcomputerV","link":"https://somevalidlink12.com"},{"name":"nand2tetris:buildingacom","link":"https://somevalidlink13.com"},{"name":"8StandardComputerCompone","link":"https://somevalidlink14.com"}]}]}]}
        self.assertEqual(path, expected)

    def test_get_all_topics(self):
        mongo_io = MongoIO.get_instance()
        toipcs = mongo_io.get_topics("")
        expected = [{"_id":"aaaa00000000000000000009","name":"Data Manipulation"},{"_id":"aaaa00000000000000000008","name":"Data Storage"},{"_id":"aaaa00000000000000000010","name":"Data Wrangling"},{"_id":"aaaa00000000000000000014","name":"GitBasics"},{"_id":"aaaa00000000000000000003","name":"Hardware"},{"_id":"aaaa00000000000000000002","name":"History of Computing"},{"_id":"aaaa00000000000000000016","name":"Intermediate CSS"},{"_id":"aaaa00000000000000000015","name":"Intermediate HTML"},{"_id":"aaaa00000000000000000011","name":"Managing State"},{"_id":"aaaa00000000000000000012","name":"OdinIntro"},{"_id":"aaaa00000000000000000004","name":"Operating Systems"},{"_id":"aaaa00000000000000000005","name":"Runtimes"},{"_id":"aaaa00000000000000000006","name":"Spectrum of Platforms"},{"_id":"aaaa00000000000000000007","name":"Types of Data"},{"_id":"aaaa00000000000000000013","name":"WebDevSetup"}]
        self.assertEqual(toipcs, expected)

    def test_get_some_topiocs(self):
        mongo_io = MongoIO.get_instance()
        toipcs = mongo_io.get_topics("data")
        self.assertEqual(len(toipcs), 4)

    def test_get_a_topic(self):
        mongo_io = MongoIO.get_instance()
        topic = mongo_io.get_topic("aaaa00000000000000000002")
        expected = {"name":"History of Computing","resources":[{"name":"ComputerHistoryTimelineA","link":"https://somevalidlink02.com"},{"name":"HistoryofComputingArticl","link":"https://somevalidlink03.com"},{"name":"PiratesofSiliconValleyFi","link":"https://somevalidlink04.com"},{"name":"Apple1984SuperBowlCommer","link":"https://somevalidlink05.com"},{"name":"BretVictorTheFutureofPro","link":"https://somevalidlink06.com"},{"name":"AwesomeComputerHistoryRe","link":"https://somevalidlink07.com"},{"name":"JeanBartikandtheENIACWom","link":"https://somevalidlink08.com"}]}
        self.assertEqual(topic, expected)

    def test_get_curriculum(self): # TODO
        # Test Data - Matches test data from database
        breadcrumb = {"atTime": datetime.fromisoformat("2024-02-27T18:17:58"),"byUser": ObjectId("aaaa00000000000000000001"),"fromIp": "192.168.1.3", "correlationId": "ae078031-7de2-4519-bcbe-fbd5e72b69d3"}
        resource1 = {"sequence":1,"roadmap":"Completed","path":"The Odin Project","segment":"Foundations","topic":"OdinIntro","type":"Resource","resource_id":ObjectId("cccc00000000000000000008"), "name": "JeanBartikandtheENIACWom", "link": "https://somevalidlink08.com", "started":datetime.fromisoformat("2024-07-01T13:00:00"),"completed":datetime.fromisoformat("2024-07-01T14:30:00"),"rating":4,"review":"This was a great intro"}
        resource2 = {"sequence":2,"roadmap":"Completed","path":"The Odin Project","segment":"Foundations","topic":"OdinIntro","type":"Adhoc","resource_name":"Markdown Tutorial","resource_url":"https://www.markdowntutorial.com/lesson/1/","started":datetime.fromisoformat("2024-07-02T13:00:00"),"completed":datetime.fromisoformat("2024-07-03T19:36:00"),"rating":3,"review":"I had to read this twice before it made sense"}
        resource7 = {"sequence":7,"roadmap":"Later","path":"EngineerKit","segment":"Craftsmanship","type":"Resource","resource_id":ObjectId("cccc00000000000000000010"), "name": "DigitalLogicSimTool", "link": "https://somevalidlink10.com"}
        
        mongo_io = MongoIO.get_instance()
        curriculum = mongo_io.get_curriculum("aaaa00000000000000000001")
        self.assertEqual(curriculum.get("_id"), ObjectId("aaaa00000000000000000001"))
        self.assertEqual(curriculum.get("lastSaved"), breadcrumb)
        self.assertIsInstance(curriculum.get("resources"), list)
        self.assertEqual(len(curriculum["resources"]), 7)
        
        self.assertEqual(curriculum.get("resources")[0], resource1)
        self.assertEqual(curriculum.get("resources")[1], resource2)
        self.assertEqual(curriculum.get("resources")[6], resource7)
           
    def test_create_curriculum(self): # TODO
        mongo_io = MongoIO.get_instance()
        breadcrumb = {"atTime": datetime.fromisoformat("2024-01-01T12:34:56"), "byUser": ObjectId("aaaa00000000000000000001"),"fromIp": "127.0.0.1", "correlationId": "aaaa-aaaa-aaaa-aaaa"}
        mongo_io.create_curriculum("aaaa00000000000000000012", breadcrumb)

        expected = {"_id": ObjectId("aaaa00000000000000000012"), "resources": [], "lastSaved": breadcrumb}
        curriculum = mongo_io.get_curriculum("aaaa00000000000000000012")
        self.assertEqual(curriculum, expected)
        
    def test_update_curriculum(self): #TODO Update
        mongo_io = MongoIO.get_instance()
        breadcrumb = {"atTime": datetime.fromisoformat("2024-01-01T12:00:00"), "byUser": ObjectId("aaaa00000000000000000001"),"fromIp": "127.0.0.1", "correlationId": "aaaa-aaaa-aaaa-aaaa"}
        mongo_io.create_curriculum("aaaa00000000000000000012", breadcrumb)

        breadcrumb["fromIp"] = "127.0.0.2"
        mongo_io.add_resource_to_curriculum("aaaa00000000000000000012", {"sequence": 1},breadcrumb)

        # Test update_curriculum method
        breadcrumb["fromIp"] = "127.0.0.3"
        resource = mongo_io.update_curriculum(
            "aaaa00000000000000000012", 
             1,
            {"type":"Adhoc"},
            breadcrumb
        )

        expected = {"_id": ObjectId("aaaa00000000000000000012"), "resources": [{"sequence": 1, "type":"Adhoc"}], "lastSaved": breadcrumb}
        curriculum = mongo_io.get_curriculum("aaaa00000000000000000012")
        self.assertEqual(curriculum, expected)
        
