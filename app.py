#import os
import base64
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import numpy as np
#import os
import six.moves.urllib as urllib
import sys
#import tensorflow as tf
from collections import defaultdict
from io import StringIO
from PIL import Image
sys.path.append("..")
import sys
import cv2
from run import process
#import argparse
import os
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods=['POST'])
def upload():
    data_url = request.form.get('file')   # here parse the data_url out http://xxxxx/?image={dataURL}
    content = data_url.split(';')[1]
    image_encoded = content.split(',')[1]
    body = base64.decodebytes(image_encoded.encode('utf-8'))
    file = request.files['file1']
    #print(file)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        fh = open("uploads/"+filename, "wb")
        fh.write(body)
        fh.close()
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], "output.jpg")
        return redirect(url_for('uploaded_file',filename=filename))
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    PATH_TO_TEST_IMAGES_DIR = app.config['UPLOAD_FOLDER']
    TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR,filename.format(i)) for i in range(1, 2) ]
    #IMAGE_SIZE = (12, 8)
    #parser = argparse.ArgumentParser(description='DeepNude App CLI Version with no Watermark.')
    #parser.add_argument('-i', "--input", help='Input image to process.', action="store", dest="input", required=False, default="input.jpg")
    #parser.add_argument('-o', "--output",help='Output path to save result.', action="store", dest="output", required=False, default="output.jpg")
    #parser.add_argument('-g', "--use-gpu", help='Enable using CUDA gpu to speed up the process.', action="store_true",dest="use_gpu", default=False)
    
    if not os.path.isdir("checkpoints"):
        print("[-] Checkpoints folder not found, download it from Github repository, and extract files to 'checkpoints' folder.")
        sys.exit(1)
    #arguments = parser.parse_args()
    
    #print("[*] Processing: %s" % arguments.input)
    
    #if (arguments.use_gpu):
     #   print("[*] Using CUDA gpu to speed up the process.")
    for image_path in TEST_IMAGE_PATHS:
        #image = Image.open(image_path)
        dress = cv2.imread(image_path)
        h = dress.shape[0]
        w = dress.shape[1]
        dress = cv2.resize(dress, (512,512), interpolation=cv2.INTER_CUBIC)
        watermark = process(dress)
        watermark =  cv2.resize(watermark, (w,h), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite('uploads/'+filename, watermark)
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
if __name__ == '__main__':
	http_server = WSGIServer(('0.0.0.0', 80), app)
	http_server.serve_forever()
