import os
# import tempfile
import cv2
from base64 import b64encode
from flask import Flask, request
from utils import ImageProcess
from google.cloud import storage

app = Flask(__name__)

@app.route('/')
def home():
    return "<p>Hello, This is OCR to Text!</p>"

# @app.route('/ocr', methods=['POST'])
# def ocr():
#   content_type = request.headers.get('Content-Type')
#   if (content_type == 'application/json'):
#     body = request.get_json()
#     # Download image from cloud storage
#     path = body['path']
#     list_path = path.split('/')
#     form_path = 'image/card.jpg'
#     list_form_path = form_path.split('/')
#     tmp_form_path = os.path.join(tempfile.gettempdir(), list_form_path[1])
#     tmp_image_path = os.path.join(tempfile.gettempdir(), list_path[1])
#     storage_client = storage.Client()
#     bucket = storage_client.bucket('ocr-card')
#     blob_image = bucket.blob(path)
#     blob_image.download_to_filename(tmp_image_path)
#     image = cv2.imread(tmp_image_path)
#     form = cv2.imread(tmp_form_path)
#     cropped_image = ImageProcess.align_images(image, form)
#     cvbase64string = b64encode(cv2.imencode('.jpg', cropped_image)[1]).decode("UTF-8")
#     texts = ImageProcess.ocr(cvbase64string)
#     list_texts = []
#     for text in texts:
#       list_texts = text.description.split('\n')
#       break
#     response = {
#       'full': list_texts,
#       'status': 'success',
#       'id': list_texts[1],
#       'name_thai': list_texts[4].split(' ').pop(1) + list_texts[4].split(' ').pop(2) + ' ' + list_texts[4].split(' ').pop(3),
#       'name_eng': list_texts[5].split(' ').pop(1) + list_texts[5].split(' ').pop(2) + ' ' + list_texts[7].split(' ').pop(2)
#     }
#     return response
#   else:
#     return 'Content-Type not supported!'