from app import app
from flask import render_template, redirect, url_for

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/main-page')
def index():
    return render_template('main_page.html')

@app.route('/transfer-page', methods=['POST','GET'])
def transfer():
    return render_template('upload_page.html')

@app.route('/download-file')
def download_file():
    pass