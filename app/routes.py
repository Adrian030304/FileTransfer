import os, tempfile, stat
import sqlalchemy as sql
from app import app, db #socketio
from app.models import UploadedFiles
from flask import render_template, redirect, url_for, request, send_from_directory, send_file, Response, flash
from werkzeug.utils import secure_filename
from .forms import FileForm
from .utils import generate_random_string
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import timedelta, datetime
# from flask_socketio import SocketIO, emit

upload_location = app.config['UPLOAD_FOLDER']

# @socketio.on('my event')
# def test_message(message):
#     emit('my response', {'data': message['data']})

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
    saving_folder = None
    form = FileForm()

    now = datetime.now()
    removable_files = db.session.scalars(sql.select(UploadedFiles).where(UploadedFiles.expiration_date < now))
    if removable_files:
        try:
            for r in removable_files:
                os.remove(os.path.join(upload_location, r.id))
        except PermissionError:
            return redirect('home')
        except FileNotFoundError:
            pass

        db.session.query(UploadedFiles).where(UploadedFiles.expiration_date < now).delete(synchronize_session=False)
        db.session.commit()     

    if request.method == 'POST':
        if form.validate_on_submit():
            # print(form.data)
            saving_folder = os.path.join(upload_location, str(generate_random_string()))
            os.makedirs(saving_folder,exist_ok=True)
            
            if saving_folder and os.path.exists(saving_folder):
                access_code = saving_folder.rsplit('\\', 1)[-1]

            for file in form.files.data:
                filename = secure_filename(file.filename)
                file.save(os.path.join(saving_folder, filename))

            exp_date = form.expiration_date.data
            if 'minutes' in exp_date:
                exp_date: str = (exp_date.split(' ')[0]).strip()
            exp_date = datetime.now() + timedelta(minutes=float(exp_date))


            if access_code:
                sql_file = UploadedFiles(
                    id=access_code,
                    file_name=secure_filename(file.filename), 
                    expiration_date=exp_date
                    )
                db.session.add(sql_file)
                db.session.commit()

                # result = db.session.scalars(sql.Select(UploadedFiles)).first()
                # print(result)

        
    return render_template('upload_page.html', form=form, access_code=access_code)

@app.route('/download_file/<download_code>', methods=['POST'])
def download_file(download_code):
    download_directory = os.path.join(upload_location, download_code)
    try:
        files_list = os.listdir(download_directory)
    except FileNotFoundError:
        return redirect(url_for('transfer'))

    if len(files_list) > 1:
        # creez fisier temporar
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        temp_zip.close()
    
        with ZipFile(temp_zip.name, 'w', ZIP_DEFLATED) as fisier_zip:
            for fisier in files_list:
                filename = os.path.join(download_directory, fisier)
                fisier_zip.write(filename, fisier) # va fi scris doar numele fisierului in zip fara sa ii apara path ul
        response = send_file(temp_zip.name, mimetype='application/zip', as_attachment=True, download_name=download_code[:6])
        return response
    else:
        try:
            response = send_from_directory(download_directory,files_list[0], as_attachment=True)
            return response
        except FileNotFoundError:
            return "File not found", 404


@app.route('/files-page/<download_code>', methods=['GET','POST'])
def files_page(download_code):
    download_directory = os.path.join(upload_location, download_code)
    try:
        files_list = os.listdir(download_directory)
    except FileNotFoundError:
        return redirect(url_for('transfer'))
    return render_template('download.html', files = files_list, download_code=download_code )


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit-contact', methods=['GET', 'POST'])
def submit_contact():
    return render_template('submit-contact.html')
