import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
# from rapidfuzz import process, fuzz
from thefuzz import fuzz, process, StringMatcher
import sys
import re
# import cv2 
import pytesseract
from ocr_test import ocr_test_bp


# import easyocr
# import matplotlib.pyplot as plt
# import keras_ocr

from flask_mysqldb import MySQL
import MySQLdb.cursors

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FILE_DIR = 'files'

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'sail'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'ingredients'

mysql = MySQL(app)

app.register_blueprint(ocr_test_bp)


if not os.path.exists(FILE_DIR):
    os.makedirs(FILE_DIR)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processTesseract(filename):
    # img = cv2.imread(filename)

    custom_config = r'--oem 3 --psm 11'
    return pytesseract.image_to_string(filename, lang='eng', config=custom_config)

def processEasyOCR(filename):
    easyReader = easyocr.Reader(['en', 'ru'], True, None, False)
    parsed = easyReader.readtext(filename)
    # output = "EasyOCR:\n------------------------\n"
    return '\n'.join(map(lambda x: x[1], parsed))

def processKerasOCR(filename):
    # keras-ocr will automatically download pretrained
    # weights for the detector and recognizer.
    pipeline = keras_ocr.pipeline.Pipeline()

    images = [
        keras_ocr.tools.read(img) for img in [filename]
    ]

    # Each list of predictions in prediction_groups is a list of
    # (word, box) tuples.
    prediction_groups = pipeline.recognize(images)

    # Plot the predictions
    # fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
    # for ax, image, predictions in zip(axs, images, prediction_groups):
    #     keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)

    
    output = "\n-----------------------\nKerasOCR:\n-----------------------"
    ocr_img = prediction_groups[0]
    for text, box in ocr_img:
        output = output + '\n' + text

    return output

@app.route('/api/v1/ocr', methods=['GET', 'POST'])
def upload_file():
    if request.method != 'POST':
        
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=image>
        <input type=submit value=Upload>
        </form>
        '''

    # check if the post request has the file part
    if 'image' not in request.files:
        flash('No file part')
        return redirect(request.url)
        
    file = request.files['image']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if not(file) or not(allowed_file(file.filename)):
        pass

    filename = FILE_DIR + '/' + secure_filename(file.filename)
    file.save(filename)

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select names from ingredients")

    data = cursor.fetchall()
    ingredientsList = [row['names'].lower() for row in data]

    print(ingredientsList, file=sys.stdout)

    output = ''
    
    # KerasOCR
    # output = output + processKerasOCR(filename)

    # EasyOCR
    # ocrText = processEasyOCR(filename)

    # Tesseract
    ocrText = processTesseract(filename)
    ocrText = re.sub('[^0-9a-zA-Z]+', ' ', ocrText.lower())

    print(ocrText, file=sys.stdout)

    result = process.extractBests(ocrText.lower(), ingredientsList, limit=None, scorer=fuzz.token_set_ratio, score_cutoff=50)

    ingredientsResult = [row[0] for row in result]

    return jsonify({"ingredients": ingredientsResult})
