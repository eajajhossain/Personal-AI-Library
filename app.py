from flask import Flask, render_template, request, jsonify
from engine.document_mgr import process_pdf_smartly
from engine.core import ai_handler
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files.get('file')
        if not file: 
            return jsonify({"status": "error", "message": "No file selected"}), 400
        
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        print(f"--- File saved to: {path} ---")
        
        # 1. Process PDF into chunks
        chunks = process_pdf_smartly(path)
        
        # 2. Ingest into Vector DB
        if chunks:
            ai_handler.ingest_documents(chunks)
            print(f"--- Successfully indexed {file.filename} ---")
            return jsonify({
                "status": "success", 
                "message": f"'{file.filename}' has been added to your library."
            })
        else:
            return jsonify({"status": "error", "message": "Failed to process PDF content."}), 500

    except Exception as e:
        print(f"Upload Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_query = data.get("message")
        
        if not user_query: 
            return jsonify({"reply": "Please enter a question."}), 400
        
        # Get answer from the RAG engine
        response = ai_handler.get_answer(user_query)
        return jsonify({"reply": response})

    except Exception as e:
        print(f"Chat Error: {str(e)}")
        return jsonify({"reply": "Sorry, I encountered an error processing your request."}), 500

if __name__ == '__main__':
    # Running on port 5000 - Ensure Ollama is running first!
    app.run(debug=True, port=5000)