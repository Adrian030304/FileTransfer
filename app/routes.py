from app import app
from flask import render_template, redirect, url_for, request, send_from_directory, send_file
from werkzeug.utils import secure_filename
from .forms import FileForm
from .utils import generate_random_string
from zipfile import ZipFile, ZIP_DEFLATED
import os, tempfile

upload_location = app.config['UPLOAD_FOLDER']

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/main-page')
def index():
    return render_template('main_page.html')

@app.route('/transfer-page', methods=['POST','GET'])
def transfer():
    
    os.makedirs(upload_location, exist_ok=True)
    
    access_code = None

    form = FileForm()
    saving_folder = None
    if request.method == 'POST':
        if form.validate_on_submit():
            saving_folder = os.path.join(upload_location, str(generate_random_string()))
            os.makedirs(saving_folder,exist_ok=True)
            
            if saving_folder and os.path.exists(saving_folder):
                access_code = saving_folder.rsplit('\\', 1)[-1]

            for file in form.files.data:
                filename = secure_filename(file.filename)
                file.save(os.path.join(saving_folder, filename))
        
        
    return render_template('upload_page.html', form=form, access_code=access_code)

@app.route('/download_file/<download_code>', methods=['POST'])
def download_file(download_code):
    download_directory = os.path.join(upload_location, download_code)
    files_list = os.listdir(download_directory)
    # print(os.path.join(download_directory, files_list[0]))

    if len(files_list) > 1:
        # creez fisier temporar
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        temp_zip.close()
    
        with ZipFile(temp_zip.name, 'w', ZIP_DEFLATED) as fisier_zip:
            for fisier in files_list:
                filename = os.path.join(download_directory, fisier)
                fisier_zip.write(filename, fisier) # va fi scris doar numele fisierului in zip fara sa ii apara path ul
        response = send_file(temp_zip.name, mimetype='application/zip', as_attachment=True, download_name=download_code[:6])

        @response.call_on_close
        def delete_zip():
            os.remove(temp_zip.name)

        return response
    else:
        try:
            return send_from_directory(download_directory,files_list[0], as_attachment=True)
        except FileNotFoundError:
            return "File not found", 404
    

@app.route('/files-page/<download_code>', methods=['GET','POST'])
def files_page(download_code):
    download_directory = os.path.join(upload_location, download_code)
    files_list = os.listdir(download_directory)

    return render_template('download.html', files = files_list )


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit-contact', methods=['GET', 'POST'])
def submit_contact():
    return render_template('submit-contact.html')
