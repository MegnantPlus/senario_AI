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
