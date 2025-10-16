from app import app
from flask import render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
from .forms import FileForm
from .utils import generate_random_string
import os

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/main-page')
def index():
    return render_template('main_page.html')

@app.route('/transfer-page', methods=['POST','GET'])
def transfer():
    upload_location = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_location, exist_ok=True)
    
    form = FileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            folder_name = str(generate_random_string())
            os.makedirs(os.path.join(upload_location, folder_name),exist_ok=True)
            
            for file in form.files.data:
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_location, folder_name, filename))
            return redirect()
    return render_template('upload_page.html', form=form)

@app.route('/download-file')
def download_file():
    pass