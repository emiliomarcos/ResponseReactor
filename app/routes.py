import os
import tempfile
from flask import request
from app import app
from bots import bot1, bot2
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

ALLOWED_EXTENSIONS = {'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        file_descriptor, file_path = tempfile.mkstemp(suffix='.pdf')

        try:
            with os.fdopen(file_descriptor, 'wb') as temp:
                file.save(temp)

            with open(file_path, 'rb') as pdf_file:
                parser = PDFParser(pdf_file)
                PDFDocument(parser)

            response = bot2.run(file_path)

            return response

        except Exception as e:
            return 'Invalid PDF: {}'.format(str(e)), 400

        finally:
            os.remove(file_path)

    return 'Invalid file path', 400
