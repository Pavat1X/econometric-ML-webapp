from flask import Flask, request, redirect, url_for, session
from flask_restplus import Api, Resources, fields
import pandas as pd
import statsmodels.api 
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.csv', '.dta']
app.config['UPLOAD_PATH'] = r'E:\econ ml weba\econometric-ML-webapp\server'
name_space = app.namespace('mainpage', description = 'main user interface')


@app.route('/', methods=['POST'])
def fileUpload():
    target = os.path.join(app.config['UPLOAD_PATH'], 'test')
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.file['file']
    filename = secure_filename(file.filename)
    destination = "/".join([target, filename])
    file.save(destination)
    session['uploadFilePath'] = destination
    response = "File uploaded successfully"
    return response


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=8000)