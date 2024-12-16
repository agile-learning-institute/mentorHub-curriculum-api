from datetime import datetime
from bson import ObjectId


class BsonEncoder:

    @staticmethod
    def bson_encode_document(document, id_properties, date_properties):
        """Encode ObjectId and datetime values for MongoDB"""        
        def encode_value(key, value):
            """Encode identified values"""
            if key in id_properties:
                if isinstance(value, str):
                    return ObjectId(value)
                if isinstance(value, list):
                    return [ObjectId(item) if isinstance(item, str) else item for item in value]
            if key in date_properties:
                if isinstance(value, str):
                    return datetime.fromisoformat(value)
                if isinstance(value, list):
                    return [datetime.fromisoformat(item) if isinstance(item, str) else item for item in value]
            return value

        # Traverse the document and encode relevant properties
        for key, value in document.items():
            if isinstance(value, dict):
                BsonEncoder._encode_resource_data(value)  # Recursively encode nested documents
            elif isinstance(value, list):
                # Check if the list contains dictionaries (objects)
                if all(isinstance(item, dict) for item in value):
                    document[key] = [BsonEncoder._encode_resource_data(item) for item in value]
                else:
                    document[key] = [encode_value(key, item) for item in value]  # Encode non-object list items
            else:
                document[key] = encode_value(key, value)  # Encode single values

        return document