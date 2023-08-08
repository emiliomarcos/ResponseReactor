import os
from flask import request
from app import app
from bots import bot1, bot2
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        response = bot2.run()
        return response

    return 'Invalid file path', 400
