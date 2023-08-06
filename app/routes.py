from flask import render_template, request
from app import app
from bots import bot1, bot2

@app.route('/bot1')
def run_bot1():
    response = bot1.run()
    return response

@app.route('/bot2')
def run_bot2():
    response = bot2.run()
    return response
