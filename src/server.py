from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/curriculum/<id>', methods=['GET'])
def get_or_create_curriculum(id):
    # Return a static response for now
    return jsonify({"message": "GET or create curriculum", "id": id}), 200

@app.route('/api/curriculum/<id>', methods=['POST'])
def add_resource_to_curriculum(id):
    # Return a static response for now
    return jsonify({"message": "Resource added to curriculum", "id": id}), 200

@app.route('/api/curriculum/<id>/<int:seq>', methods=['PATCH'])
def update_curriculum(id, seq):
    # Return a static response for now
    return jsonify({"message": "Curriculum updated", "id": id, "seq": seq}), 200

@app.route('/api/curriculum/<id>/<int:seq>', methods=['DELETE'])
def delete_resource_from_curriculum(id, seq):
    # Return a static response for now
    return '', 204

@app.route('/api/config/', methods=['GET'])
def get_config():
    # Return a static response for now
    return jsonify({"message": "API configuration"}), 200

@app.route('/api/health/', methods=['GET'])
def health_check():
    # Return a static response for now
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)