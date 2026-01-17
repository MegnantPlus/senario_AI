from flask import Blueprint, request, jsonify
from app import mongo
from app.models.scenario_model import Scenario
from bson import ObjectId

scenario_bp = Blueprint('scenario', __name__)

@scenario_bp.route('/api/scenario', methods=['POST'])
def create_scenario():
    data = request.get_json()
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Invalid data. Title and content are required.'}), 400
    
    new_scenario = Scenario(title=data['title'], content=data['content'])
    
    try:
        # Gửi dữ liệu lên collection 'scenarios' trong MongoDB
        result = mongo.db.scenarios.insert_one(new_scenario.to_dict())
        
        response_data = new_scenario.to_dict()
        response_data['_id'] = str(result.inserted_id)
        
        return jsonify({
            'message': 'Scenario created successfully',
            'data': response_data
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@scenario_bp.route('/api/scenario', methods=['GET'])
def get_scenarios():
    try:
        # Lấy tất cả kịch bản từ database
        scenarios_cursor = mongo.db.scenarios.find()
        output = []
        for scenario in scenarios_cursor:
            scenario_data = {
                '_id': str(scenario['_id']),
                'title': scenario.get('title'),
                'content': scenario.get('content')
            }
            output.append(scenario_data)
            
        return jsonify(output), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@scenario_bp.route('/api/scenario/<id>', methods=['DELETE'])
def delete_scenario(id):
    try:
        # Xoá kịch bản theo ID
        result = mongo.db.scenarios.delete_one({'_id': ObjectId(id)})
        
        if result.deleted_count == 1:
            return jsonify({'message': 'Scenario deleted successfully'}), 200
        else:
            return jsonify({'error': 'Scenario not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Invalid ID or database error: ' + str(e)}), 500
