import os
import tempfile
from flask import request, make_response
from app import app
from bots import bot1, bot2, bot3
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
# from flask_cors import cross_origin

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
# @cross_origin(origin='localhost',port=5173)
def run_bot2():
    # allowed_origins = ['http://localhost:5173']
    # origin = request.headers.get('Origin')

    # if origin not in allowed_origins:
    #     return 'Forbidden: Invalid Origin', 403

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

            return response, 200

        except Exception as e:
            return 'Invalid PDF: {}'.format(str(e)), 400

        finally:
            os.remove(file_path)

    return 'Invalid file path', 400

@app.route('/bot3')
def run_bot3():
    response = bot3.run()
    return response

# def make_cors_response(data, status_code):
#     response = make_response(data, status_code)
#     response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
#     response.headers['Access-Control-Allow-Methods'] = 'POST'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
#     return response
