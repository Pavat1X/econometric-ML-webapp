from flask import Flask, request, redirect, url_for, session
from flask_wtf import Flaskform
import pandas as pd
import statsmodels.api 
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.csv', '.dta']
app.config['UPLOAD_PATH'] = r'E:/econ ml weba/econometric-ML-webapp/server/uploads'
name_space = app.namespace('mainpage', description = 'main user interface')
import os

class MyForm(Flaskform):
    info_field = StringField('please type in your regressors', validators=[DataRequired()])
    name_field = StringField('please type in the name of your file', validators=[DataRequired()])
    file_field = FileField('please upload your data file', validators=[DataRequired()])


@app.route('/upload', methods=['POST'])
def formUpload():

    form = MyForm()

    if form.validate_on_submit():
        try:
            file = request.files[file_field]
            extension = os.path.splitext(file.filename)

        if file:

            if extension not in app.config['UPLOAD_EXTENSIONS']:
                return 'File is neither a csv nor a dta stata file'

            file.save(os.path.join(
                app.config['UPLOAD_PATH'],
                secure_filename(file.filename)
            ))
        
        info = form.info_field.data
        filename = form.name_field.data

        regressors_list = info.rstrip('')
        regressors_list = regressors_list.split(',')

        filepath = r'E:/econ ml weba/econometric-ML-webapp/server/uploads'
        new_filepath = filepath + filename

        if '.csv' in filename:
            data = pd.read_csv(new_filepath)
        else:
            data = pd.read_stata(new_filepath)

        session['data'] = data
    
        return redirect('/')

@app.route('/regress', methods = ['GET', 'POST'])

def runRegression():
    data = session.get('data', None)




        

        
        
