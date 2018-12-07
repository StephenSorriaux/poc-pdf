import pdf_needs
import xls_inventory
import config

import pandas
from flask import Blueprint, render_template, abort, Flask, request, redirect, flash, send_from_directory
from jinja2 import TemplateNotFound
from flask_bootstrap import Bootstrap

import math
import os

app = Flask(__name__)

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)

@app.route('/handle_data', methods=['POST'])
def generate_output():
    if len(request.files) < 2:
        return redirect(request.url)

    pdf = request.files['pdf']
    xls = request.files['xls']
    messages = []
    inventory = xls_inventory.generate_inventory_for_file(xls, messages)
    needs = pdf_needs.generate_needs_for_file(pdf, messages)

    # soustraire stock a inventaire
    try:
        final_result = needs.sub(inventory, fill_value=0)
        final_result.fillna(value=0, inplace=True)
    except Exception as e:
        final_result = None
        messages.append('Impossible de calculer la diff entre le fichier pdf et le fichier excel: ' + str(e))
    
    # generation du fichier csv
    csv_available=False
    try:
        final_result.to_csv(
            path_or_buf=os.path.join(app.config['UPLOAD_FOLDER'], 'output.csv')
        )
        csv_available=True
    except Exception as e:
        messages.append('Impossible de generer le fichier csv de resultats: ' + str(e))
    # afficher resultat
    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
        return render_template(
            'results.html',
            result=final_result,
            messages=messages,
            csv=csv_available
        )

@app.route('/file/<filename>')
def get_csv_file(filename):
    if filename == 'output.csv':
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename
        )
    else:
        return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


if __name__ == '__main__':
    Bootstrap(app)
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    app.secret_key = 'OMG_OMG_OMG'
    app.config['SESSION_TYPE'] = 'filesystem'
    host = os.environ.get('HOST', '0.0.0.0') 
    port = os.environ.get('PORT', '5000') 
    app.run(debug=True, port=port, host=host)