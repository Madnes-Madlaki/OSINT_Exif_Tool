from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from extractScript import extractionFunc

ui = Flask(__name__)

ui.config['Upload_folder'] = 'uploads'
os.makedirs(ui.config['Upload_folder'], exist_ok=True) 
allowed_file_extensions = {'jpeg', 'jpg', 'png', 'tiff', 'bmp', 'gif'}

def isAllowedExtension(fileName):
    return '.' in fileName and fileName.rsplit('.', 1)[1].lower() in allowed_file_extensions
    #return . to check that the file does have an extension
    #rsplit splits the name into two (after the .), takes the second part of the splitted name and converts it into lowercase

@ui.route('/')
def index():
    return render_template('index.html')  
    #main ui

@ui.route('/upload', methods=['POST'])  
def uploadFile():
    if 'file' not in request.files:
        return jsonify({'upload error': 'No file has been uploaded'}), 403
    file = request.files['file']
    if file.filename == '':  
        return jsonify({'no file selected': 'no file has been selected'}), 403
    if not isAllowedExtension(file.filename):  
        return jsonify({'extension not suitable': 'extension is still not accepted by this version of the tool, use jpeg, gif, png, bmp, tiff'}), 403
    fileName = secure_filename(file.filename)
    filepath = os.path.join(ui.config['Upload_folder'], fileName)  
    file.save(filepath)

    metadata_dictionary = {}

    try:
        googleMapsLink = extractionFunc(filepath)  
        report_files = [f for f in os.listdir('.') if f.startswith('metadata_') and f.endswith('.json')]
        #takes the json file the function creates, see extractScript.py and reads it, takes only files starting with metadata_ and ending in json extension
        if report_files:
            lastReport = max(report_files, key = os.path.getctime)
            #compares creation tiem
            with open(lastReport, 'r') as filevariable:
                metadata_dictionary = json.load(filevariable) 
        
        os.remove(filepath)  
        return jsonify({
            'success': True,
            'metadata': metadata_dictionary,
            'googleMapsLink': googleMapsLink if googleMapsLink 
                                        else None
            })
        
    except Exception as e:
        if os.path.exists(filepath):  
            os.remove(filepath)
        return jsonify({'success': False, 'error': str(e)}), 405  

if __name__ == '__main__':
    ui.run(debug=True, port=2727)