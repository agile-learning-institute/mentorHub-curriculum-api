from copy import deepcopy
from datetime import datetime, timezone
import unittest

from bson import ObjectId
from src.config.config import config
from src.utils.mongo_io import MongoIO

class TestMongoIO(unittest.TestCase):
    
    def setUp(self):
        # Test Data - Matches test data from database
        self.completed = [{"name":"JeanBartikandtheENIACWom","link":"https://somevalidlink08.com","description":"The Description String","started":datetime.fromisoformat("2024-07-01T13:00:00"),"completed":datetime.fromisoformat("2024-07-01T14:30:00"),"rating":4,"review":"This was a great intro"},{"name":"Markdown Tutorial","link":"https://www.markdowntutorial.com/lesson/1/","description":"The Description String","started":datetime.fromisoformat("2024-07-02T13:00:00"),"completed":datetime.fromisoformat("2024-07-03T19:36:00"),"rating":3,"review":"I had to read this twice before it made sense"}]
        self.now = [{"name":"AWSStorageResource","link":"https://somevalidlink.35.com","description":"The Description String","started":datetime.fromisoformat("2024-07-15T13:00:00")},{"name":"Some Unique Resource","description":"The Description String","link":"https://some.com/resource"}]
        self.next = [{"path":"The Odin Project","segments":[{"segment":"Intermediate HTML and CSS","topics":[{"topic":"Intermediate HTML","resources":[{"name":"Howdocomputersreadcode?V","link":"https://somevalidlink.22.com","description":"The Description String","skills":[],"tags":[]},{"name":"A one-off resource","link":"https://some.com/resource","description":"The Description String","skills":[],"tags":[]}]}]}]}]
        self.later = [{"path_id":ObjectId("999900000000000000000000"),"name":"The Odin Project"},{"path_id":ObjectId("999900000000000000000001"),"name":"EngineerKit"},{"path_id":ObjectId("999900000000000000000003"),"name":"Cantrillo"}]
        self.breadcrumb = {"atTime": datetime.fromisoformat("2024-02-27T18:17:58"),"byUser": ObjectId("aaaa00000000000000000001"),"fromIp": "192.168.1.3", "correlationId": "ae078031-7de2-4519-bcbe-fbd5e72b69d3"}

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
        self.assertEqual(len(config.versions), 9)

        self.assertIsInstance(config.enumerators, dict)

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
        expected = {"name":"Cantrillo","segments":[{"name":"Fundamentals","topics":[{"name":"History of Computing","resources":[{"name":"ComputerHistoryTimelineA","description":"Computer History Timeline Article","link":"https://somevalidlink02.com","skills":["Basic use of the Unix/Linux command line and shell scripts","Vue.js concepts with design system libraries"],"tags":["$","Article","Exam","Interactive","Lesson","Tutorial","Video","Data"]},{"name":"HistoryofComputingArticl","description":"History of Computing Article","link":"https://somevalidlink03.com","skills":["Vue.js concepts with design system libraries","Python Data Structures and with Pandas"],"tags":["Article","Book","Reference","User Guide","API","Data"]},{"name":"PiratesofSiliconValleyFi","description":"Pirates of Silicon Valley Film","link":"https://somevalidlink04.com","skills":["Basic use of the Unix/Linux command line and shell scripts","Python Data Structures and with Pandas"],"tags":["Exam","Lecture","Video","API","Data"]},{"name":"Apple1984SuperBowlCommer","description":"Apple 1984 Super Bowl Commercial Video","link":"https://somevalidlink05.com","skills":["Vue.js concepts with design system libraries","Python Data Structures and with Pandas"],"tags":["Article","Book","Interactive","Lecture","Lesson","User Guide","UI/UX","API","Data"]},{"name":"BretVictorTheFutureofPro","description":"Bret Victor The Future of Programming Video","link":"https://somevalidlink06.com","skills":["Basic use of the Unix/Linux command line and shell scripts"],"tags":["Lecture","Lesson","Tutorial","User Guide","Video","API","Data"]},{"name":"AwesomeComputerHistoryRe","description":"Awesome Computer History Resource","link":"https://somevalidlink07.com","skills":["Vue.js concepts with design system libraries"],"tags":["Book","Lecture","Reference","User Guide","Video","UI/UX","Data"]},{"name":"JeanBartikandtheENIACWom","description":"Jean Bartik and the ENIAC Women Video","link":"https://somevalidlink08.com","skills":["Basic use of the Unix/Linux command line and shell scripts","Python Data Structures and with Pandas"],"tags":["Article","Exam","Interactive","Lecture","Tutorial","User Guide","UI/UX","API","Data"]}]},{"name":"Hardware","resources":[{"name":"ExploringHowComputersWor","link":"https://somevalidlink09.com","description":"Exploring How Computers Work Video","skills":["Working knowledge of Javascript / Typescript fundamentals"],"tags":["Article","Exam","Interactive","Lecture","Lesson","Tutorial","Video","UI/UX"]},{"name":"DigitalLogicSimTool","link":"https://somevalidlink10.com","description":"Digital Logic Sim Tool","skills":["Working knowledge of Javascript / Typescript fundamentals"],"tags":["$","Video","UI/UX","Data"]},{"name":"HistoryandTheoryofElectr","link":"https://somevalidlin11.com","description":"History and Theory of Electricity Video","skills":["Working knowledge of Javascript / Typescript fundamentals"],"tags":["Article","Tutorial","User Guide","Video","UI/UX","API","Data"]},{"name":"Buildingan8-bitcomputerV","link":"https://somevalidlink12.com","description":"Building an 8-bit computer Video Series","skills":["Working knowledge of Javascript / Typescript fundamentals"],"tags":["Article","Book","Lesson","Reference","Tutorial","Video","Data"]},{"name":"nand2tetris:buildingacom","link":"https://somevalidlink13.com","description":"nand2tetris: building a computer from first principles Course","skills":["Working knowledge of Javascript / Typescript fundamentals"],"tags":["Article","Book","Exam","Interactive","Lesson","Tutorial","Video","UI/UX","Data"]},{"name":"8StandardComputerCompone","link":"https://somevalidlink14.com","description":"8 Standard Computer Components Article","skills":["Working knowledge of Javascript / Typescript fundamentals"],"tags":["Interactive","Lecture","Tutorial","Video","Data"]}]}]}]}
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
        expected = {"name":"History of Computing","resources":[{"name":"ComputerHistoryTimelineA","description":"Computer History Timeline Article","link":"https://somevalidlink02.com","skills":["Basic use of the Unix/Linux command line and shell scripts","Vue.js concepts with design system libraries"],"tags":["$","Article","Exam","Interactive","Lesson","Tutorial","Video","Data"]},{"name":"HistoryofComputingArticl","description":"History of Computing Article","link":"https://somevalidlink03.com","skills":["Vue.js concepts with design system libraries","Python Data Structures and with Pandas"],"tags":["Article","Book","Reference","User Guide","API","Data"]},{"name":"PiratesofSiliconValleyFi","description":"Pirates of Silicon Valley Film","link":"https://somevalidlink04.com","skills":["Basic use of the Unix/Linux command line and shell scripts","Python Data Structures and with Pandas"],"tags":["Exam","Lecture","Video","API","Data"]},{"name":"Apple1984SuperBowlCommer","description":"Apple 1984 Super Bowl Commercial Video","link":"https://somevalidlink05.com","skills":["Vue.js concepts with design system libraries","Python Data Structures and with Pandas"],"tags":["Article","Book","Interactive","Lecture","Lesson","User Guide","UI/UX","API","Data"]},{"name":"BretVictorTheFutureofPro","description":"Bret Victor The Future of Programming Video","link":"https://somevalidlink06.com","skills":["Basic use of the Unix/Linux command line and shell scripts"],"tags":["Lecture","Lesson","Tutorial","User Guide","Video","API","Data"]},{"name":"AwesomeComputerHistoryRe","description":"Awesome Computer History Resource","link":"https://somevalidlink07.com","skills":["Vue.js concepts with design system libraries"],"tags":["Book","Lecture","Reference","User Guide","Video","UI/UX","Data"]},{"name":"JeanBartikandtheENIACWom","description":"Jean Bartik and the ENIAC Women Video","link":"https://somevalidlink08.com","skills":["Basic use of the Unix/Linux command line and shell scripts","Python Data Structures and with Pandas"],"tags":["Article","Exam","Interactive","Lecture","Tutorial","User Guide","UI/UX","API","Data"]}]}
        self.assertEqual(topic, expected)

    def test_get_curriculum(self): 
        mongo_io = MongoIO.get_instance()
        curriculum = mongo_io.get_curriculum("aaaa00000000000000000001")
        expected = {"_id":ObjectId("aaaa00000000000000000001"),"completed":self.completed,"now":self.now,"next":self.next,"later":self.later,"lastSaved":self.breadcrumb}
        self.assertEqual(curriculum, expected)
           
    def test_create_curriculum(self): # TODO
        mongo_io = MongoIO.get_instance()
        breadcrumb = {"atTime": datetime.fromisoformat("2024-01-01T12:34:56"), "byUser": ObjectId("aaaa00000000000000000001"),"fromIp": "127.0.0.1", "correlationId": "aaaa-aaaa-aaaa-aaaa"}
        empty_curriculum = {"_id":ObjectId("aaaa00000000000000000012"),"completed":[],"now":[],"next":[],"later":[],"lastSaved":breadcrumb}

        str_id = mongo_io.create_curriculum("aaaa00000000000000000012", breadcrumb)
        self.assertEqual(str_id, "aaaa00000000000000000012" )

        curriculum = mongo_io.get_curriculum("aaaa00000000000000000012")
        self.assertEqual(curriculum, empty_curriculum)
        
    def test_update_curriculum_completed1(self): 
        mongo_io = MongoIO.get_instance()
        mongo_io.create_curriculum("aaaa00000000000000000012", self.breadcrumb)

        breadcrumb = deepcopy(self.breadcrumb)
        set = {"completed": [{"name": "foo"}], "lastSaved": breadcrumb}
        count = mongo_io.update_curriculum("aaaa00000000000000000012", set)
        self.assertEqual(count, 1)
        
        curriculum = mongo_io.get_curriculum("aaaa00000000000000000012")
        expected = {"_id":ObjectId("aaaa00000000000000000012"),"completed":[{"name": "foo"}],"now":[],"next":[],"later":[],"lastSaved":breadcrumb}
        self.assertEqual(curriculum, expected)

    def test_update_curriculum_now(self): #TODO Update
        mongo_io = MongoIO.get_instance()
        mongo_io.create_curriculum("aaaa00000000000000000012", self.breadcrumb)

        breadcrumb = deepcopy(self.breadcrumb)

        breadcrumb["fromIp"] = "127.0.0.2"
        set = {"now": [{"name": "foo"}], "lastSaved": breadcrumb}
        count = mongo_io.update_curriculum("aaaa00000000000000000012", set)
        self.assertEqual(count, 1)

        curriculum = mongo_io.get_curriculum("aaaa00000000000000000012")
        expected = {"_id":ObjectId("aaaa00000000000000000012"),"completed":[],"now":[{"name":"foo"}],"next":[],"later":[],"lastSaved":breadcrumb}
        self.assertEqual(curriculum, expected)

    def test_update_curriculum_completed2(self): #TODO Update
        mongo_io = MongoIO.get_instance()
        mongo_io.create_curriculum("aaaa00000000000000000012", self.breadcrumb)

        breadcrumb = deepcopy(self.breadcrumb)
        breadcrumb["fromIp"] = "127.0.0.3"
        set = {"completed": [{"name": "foo"}, {"name":"bar"}], "lastSaved": breadcrumb}
        count = mongo_io.update_curriculum("aaaa00000000000000000012", set)
        self.assertEqual(count, 1)

        curriculum = mongo_io.get_curriculum("aaaa00000000000000000012")
        expected = {"_id":ObjectId("aaaa00000000000000000012"),"completed":[{"name":"foo"},{"name":"bar"}],"now":[],"next":[],"later":[],"lastSaved":breadcrumb}
        self.assertEqual(curriculum, expected)

    def test_update_curriculum_completed_description(self): #TODO Update
        mongo_io = MongoIO.get_instance()
        mongo_io.create_curriculum("aaaa00000000000000000012", self.breadcrumb)

        breadcrumb = deepcopy(self.breadcrumb)
        breadcrumb["fromIp"] = "127.0.0.4"
        set = {"completed": [{"description": "foo"}, {"description":"bar"}], "lastSaved": breadcrumb}
        count = mongo_io.update_curriculum("aaaa00000000000000000012", set)
        self.assertEqual(count, 1)

        curriculum = mongo_io.get_curriculum("aaaa00000000000000000012")
        expected = {"_id":ObjectId("aaaa00000000000000000012"),"completed":[{"description":"foo"},{"description":"bar"}],"now":[],"next":[],"later":[],"lastSaved":breadcrumb}
        self.assertEqual(curriculum, expected)
