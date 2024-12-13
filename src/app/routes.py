
from flask import render_template 
from flask import current_app
from flask import Blueprint
from flask import jsonify
from flask import request
from src.app.database import db
from src.app.models import APIEntry
from src.app.utils import purge_and_load_csv
from src.app.agents.ideation import run_ideation
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    # Serve the index.html template
    return render_template('index.html')

@main_bp.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if file:
        csv_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'apis.csv')
        file.save(csv_path)
        purge_and_load_csv(csv_path)
        return jsonify({"message": "CSV uploaded and DB reloaded"}), 200
    return jsonify({"error": "File save error"}), 500

@main_bp.route('/entries', methods=['GET'])
def get_entries():
    entries = APIEntry.query.all()
    data = []
    for e in entries:
        data.append({
            "id": e.id,
            "name": e.name,
            "category": e.category,
            "base_url": e.base_url,
            "endpoint": e.endpoint,
            "description": e.description,
            "query_parameters": e.query_parameters,
            "example_request": e.example_request,
            "example_response": e.example_response
        })
    return jsonify(data)

@main_bp.route('/ideate', methods=['POST'])
def ideate():
    logs = run_ideation()
    return jsonify({"logs": logs}), 200
