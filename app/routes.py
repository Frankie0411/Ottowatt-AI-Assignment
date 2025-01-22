from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from app.utils.pdf_processor import PDFProcessor
from app.utils.agent import Agent
from config import Config

main = Blueprint('main', __name__)

# Store agent as a global variable to persist between requests
_agent = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/set-api-key', methods=['POST'])
def set_api_key():
    global _agent
    data = request.json
    key_type = data.get('keyType')

    if key_type == 'test':
        # Use predefined test key from config
        api_key = Config.TEST_API_KEY
    else:
        # Use custom key provided by user
        api_key = data.get('apiKey')
        if not api_key:
            return jsonify({'error': 'No API key provided'}), 400

    try:
        _agent = Agent(api_key)
        return jsonify({'message': f'{key_type.capitalize()} API key set successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/upload', methods=['POST'])
def upload_file():
    global _agent

    if not _agent:
        return jsonify({'error': 'Please set an API key first'}), 400

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        try:
            os.makedirs('uploads', exist_ok=True)

            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)

            # Process PDF
            pdf_processor = PDFProcessor()
            extracted_text = pdf_processor.extract_text(filepath)
            chunks = pdf_processor.semantic_chunking(extracted_text)

            # Process chunks with existing agent
            _agent.process_pdf_chunks(chunks)

            # Clean up
            os.remove(filepath)

            return jsonify({
                'message': 'File processed successfully',
                'full_text': extracted_text
            })

        except Exception as e:
            # Clean up on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid file type'}), 400


@main.route('/query', methods=['POST'])
def query():
    global _agent

    if not _agent:
        return jsonify({'error': 'Please set an API key first'}), 400

    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    try:
        answer = _agent.get_answer(question)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
