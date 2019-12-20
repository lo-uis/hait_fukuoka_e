# -*- coding: utf-8 -*-

import os, re
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug import secure_filename
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential, Model, load_model
from PIL import Image
import sys

def predict (path) :
    list_ = ["ramen","star"]
    num = len(list_)
    IMAGE_SIZE = 224

    # convert data by specifying file from terminal
    image = Image.open("static/asset" + path)
    image = image.convert('RGB')
    image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    data = np.asarray(image,dtype=np.float32)

    X = []
    X.append(data)
    X = np.array(X)

    # load model
    model = load_model('./vgg16_transfer.h5')

    # estimated result of the first data (multiple scores will be returned)
    result = model.predict([X])[0]
    predicted = result.argmax()
    percentage = int(result[predicted] * 100)

    print(list_[predicted], percentage)

    return list_[predicted]


app = Flask(__name__)


@app.route('/')
def index():
    name = "Hello World"
    return render_template('index.html', title='flask test', name=name)

###########################
# 以下画像アップロード処理
##########################

#iPhoneの画像ファイル形式への対応

#画像アップロード
UPLOAD_FOLDER = './static/asset/uploads'
ALLOWED_EXTENSIONS = set(['jpg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

#アップロードを許可する画像ファイル
def allowed_file(filename):
    # ファイル名の拡張子より前を取得し, フォーマット後のファイル名に変更
    filename = re.search("(?<!\.)\w+", filename).group(0) + "." + 'jpg'
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#画像POST処理
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        img_file = request.files['img_file']
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_url = '/uploads/' + filename

            jg = predict(img_url)

            if jg == star :
                star_or_ramen = "この画像はスタバです"
            elif jg == ramen:
                star_or_ramen = "この画像はラーメンです"


            return render_template('index.html', img_url=img_url, kekka = star_or_ramen)


        else:
          return ''' <p>許可されていない拡張子です</p> '''
    else:
        return redirect(url_for('index'))


#アップロードされた画像ファイル
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


## おまじない
if __name__ == "__main__":
    app.run(port=8000, debug=True)
