from copy import deepcopy
from datetime import datetime, timezone
import unittest

from bson import ObjectId
from src.config.Config import config
from src.utils.mongo_io import MongoIO

class TestMongoSchema(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff = None

        # Test Data
        self.test_id = "123400000000000000009999"
        self.breadcrumb = {"atTime": datetime.fromisoformat("2024-02-27T18:17:58"),"byUser": ObjectId("aaaa00000000000000000001"),"fromIp": "192.168.1.3", "correlationId": "ae078031-7de2-4519-bcbe-fbd5e72b69d3"}
        self.future = datetime.fromisoformat("2100-12-31T23:59:59")
        self.max_sentence = "1234567890`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./ ~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:ZXCVBNM<>?\"\\ the quick brown fox jumped over the lzy dog! THE QUICK BROWN FOX JUMPED OVER THE LAZY DOG   12345678901234567890123456789012345678901234567890123456"
        self.long_link = "https://github.com/agile-learning-institute/mentorHub-curriculum-api/blob/Issue_17_Schema_Curriculum_3.0.1_Topic_3.0.0/src/utils/mongo_io.py"
        self.bad_sentences = [
            "Way too long 1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456",
            "No special characters like \t \n allowed!"
        ]
        self.bad_links = [
            "https://invalid url?query=value&20;",
            "http ://only-secure-links-allowed.com:808883"
        ]

        # Setup database - These are Integration tests
        MongoIO._instance = None
        mongo_io = MongoIO.get_instance()
        mongo_io.initialize()

    def tearDown(self):
        # Delete the created curriculum
        mongo_io = MongoIO.get_instance()
        mongo_io.delete_curriculum(self.test_id)
        mongo_io.disconnect()
    
    def test_update_curriculum_completed_success(self): 
        updates = [
            ["name", self.max_sentence],
            ["link", self.long_link],
            ["description", self.max_sentence],
            ["started", self.future],
            ["completed", self.future],
            ["rating", 1],
            ["review", self.max_sentence],
        ]

        mongo_io = MongoIO.get_instance()
        mongo_io.create_curriculum(self.test_id, self.breadcrumb)

        for [property, value] in updates:
            set = {"completed": [{property: value}], "lastSaved": self.breadcrumb}
            count = mongo_io.update_curriculum(self.test_id, set)
            self.assertEqual(count, 1)
            
            curriculum = mongo_io.get_curriculum(self.test_id)
            expected = {
                "_id":ObjectId(self.test_id),
                "completed":[{property: value}],
                "now":[],"next":[],"later":[],"lastSaved":self.breadcrumb}
            self.assertEqual(curriculum, expected)

    def test_update_curriculum_now_success(self): 
        updates = [
            ["name", self.max_sentence],
            ["link", self.long_link],
            ["description", self.max_sentence],
            ["started", self.future]
        ]

        mongo_io = MongoIO.get_instance()
        mongo_io.create_curriculum(self.test_id, self.breadcrumb)

        for [property, value] in updates:
            set = {"now": [{property: value}], "lastSaved": self.breadcrumb}
            count = mongo_io.update_curriculum(self.test_id, set)
            self.assertEqual(count, 1)
            
            curriculum = mongo_io.get_curriculum(self.test_id)
            expected = {
                "_id":ObjectId(self.test_id),
                "now":[{property: value}],
                "completed":[],"next":[],"later":[],"lastSaved":self.breadcrumb}
            self.assertEqual(curriculum, expected)

    def test_update_curriculum_next_success(self): 
        all_tags = ["$", "Article", "Book", "Exam", "Interactive", "Lecture", "Lesson", "Reference", "Tutorial", "User Guide", "Video", "UI/UX", "API", "Data", "SRE"]
        simple_path = {"path":"foo","segments":[{"segment":"bar","topics":[{"topic":"bat","resources":[]}]}]}
        updates = [
            ["name", self.max_sentence],
            ["link", self.long_link],
            ["description", self.max_sentence],
            ["skills", [self.max_sentence, self.max_sentence]],
            ["tags", all_tags]
        ]

        mongo_io = MongoIO.get_instance()
        mongo_io.create_curriculum(self.test_id, self.breadcrumb)

        for [property, value] in updates:
            simple_path["segments"][0]["topics"][0]["resources"] = [{property: value}]
            set = {
                "next": [simple_path], 
                "lastSaved": self.breadcrumb
            }
            expected = {
                "_id":ObjectId(self.test_id),
                "next":[simple_path],
                "completed":[],"now":[],"later":[],"lastSaved":self.breadcrumb
            }
            count = mongo_io.update_curriculum(self.test_id, set)
            self.assertEqual(count, 1)
            curriculum = mongo_io.get_curriculum(self.test_id)
            self.assertEqual(curriculum, expected)

    def test_update_curriculum_completed_fail(self): 
        updates = [
            ["name", self.bad_sentences],
            ["link", self.bad_links],
            ["description", self.bad_sentences],
            ["rating", ["0,5,-1"]],
            ["review", self.bad_sentences]
        ]

        mongo_io = MongoIO.get_instance()
        mongo_io.create_curriculum(self.test_id, self.breadcrumb)

        for [property, values] in updates:
            for value in values:
                set = {"completed": [{property: value}], "lastSaved": self.breadcrumb}
                with self.assertRaises(Exception) as context:
                    count = mongo_io.update_curriculum(self.test_id, set)
                    
    def test_update_curriculum_now_fail(self): 
        updates = [
            ["name", self.bad_sentences],
            ["link", self.bad_links],
            ["description", self.bad_sentences]
        ]

        mongo_io = MongoIO.get_instance()
        mongo_io.create_curriculum(self.test_id, self.breadcrumb)

        for [property, values] in updates:
            for value in values:
                set = {"now": [{property: value}], "lastSaved": self.breadcrumb}
                with self.assertRaises(Exception) as context:
                    count = mongo_io.update_curriculum(self.test_id, set)
                    

    def test_update_curriculum_next_fail(self): 
        all_tags = ["$", "Article", "Book", "Exam", "Interactive", "Lecture", "Lesson", "Reference", "Tutorial", "User Guide", "Video", "UI/UX", "API", "Data", "SRE"]
        simple_path = {"path":"foo","segments":[{"segment":"bar","topics":[{"topic":"bat","resources":[]}]}]}
        updates = [
            ["name", self.bad_sentences],
            ["link", self.long_link],
            ["description", self.bad_sentences],
            ["skills", self.bad_sentences],
            ["tags", ["not", "valid", "tags"]]
        ]

        mongo_io = MongoIO.get_instance()
        mongo_io.create_curriculum(self.test_id, self.breadcrumb)

        for [property, values] in updates:
            for value in values:
                simple_path["segments"][0]["topics"][0]["resources"] = [{property: value}]
                set = {
                    "next": [simple_path], 
                    "lastSaved": self.breadcrumb
                }

                with self.assertRaises(Exception) as context:
                    count = mongo_io.update_curriculum(self.test_id, set)
