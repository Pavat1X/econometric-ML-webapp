from flask import Flask, request, redirect, render_template, session
import os
import pandas as pd
import statsmodels.api as sm

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.csv', '.dta']

#index route
@app.route('/')
def index():
	return render_template('index.html')



@app.route('/upload', methods=["GET", "POST"])
def upload():
	try:
		file = request.files['dataset']
		regressors = request.text['regressors_list']
		response_var = request.text['response']
		session['response'] = response_var
		session['regressors'] = regressors
		extension = os.path.splitext(file.filename)
		session['ext'] = extension

	if file:
	    if extension not in app.config['UPLOAD_EXTENSIONS']:
        	return 'File is neither a csv nor a dta stata file'
        
        if 'csv' in extension:
        	data = pd.read_csv(file)
        else:
        	data = pd.read_stata(file)
	    
        session['data'] = data

        return "uploaded"
    return redirect('/')

@app.route('/regress', methods=["POST"])
def regress():
	data = session.get('data', None)
	regressors = session.get('regressors', None)
	extension = session.get('ext', None)
	response = session.get('response_var', None)

	regressors = regressors.rstrip('')
	regressors = regressors.split(',')

	if 'csv' in extension:
		data = pd.read_csv(file)
	else:
		data = pd.read_stata(file)

	regressors_data = data[data.columns.intersection(regressors)]
	response_data = data[data.columns.intersection(response)]

	X = sm.add_constant(regressors_data)
	estimate = sm.OLS.(response_data, X).fit_regularized()

	return 		

	

