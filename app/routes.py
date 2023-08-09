import os
import tempfile
from flask import request
from app import app
from bots import bot1, bot2
from werkzeug.utils import secure_filename
import pypdf

ALLOWED_EXTENSIONS = {'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    filename = secure_filename(filename)
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_pdf(file_stream):
    try:
        pypdf.PdfFileReader(file_stream)
        return True
    except pypdf.PdfReadError:
        return False

@app.route('/')
def root():
    return '<h1>Response Reactor</h1>'

@app.route('/bot1')
def run_bot1():
    response = bot1.run()
    return response

@app.route('/bot2', methods=['POST'])
def run_bot2():
    if 'file' not in request.files:
        return 'No file path', 400
    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        with tempfile.NamedTemporaryFile() as temp:
            file.save(temp)
            temp.seek(0)

            try:
                pypdf.PdfFileReader(temp.name)
            except:
                return 'Invalid PDF', 400

            file_path = temp.name

            os.chmod(file_path, 0o600)

            response = bot2.run(file_path)

            return response

    return 'Invalid file path', 400
