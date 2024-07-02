from flask import Flask, request, jsonify,render_template
import os
from main import process_data


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

query_engine = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({"error": "No file part or empty filename"}), 400

    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    global query_engine
    
    query_engine = process_data(file_path)
    return jsonify({"message": "File uploaded and processed successfully"}), 200



@app.route('/chat', methods=['POST'])
def chat():
    if query_engine is None:
        return jsonify({"error": "Query engine is not initialized. Please upload a file first."}), 400

    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "No query provided"}), 400

    query = data['query']
    response = query_engine.query(query)
    
    return jsonify({"response": response.response}), 200



if __name__ == '__main__':
    app.run(debug=True,port=5003)


