import json
import datetime
from bson.objectid import ObjectId

class EJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (ObjectId, datetime.datetime)):
            return str(obj)