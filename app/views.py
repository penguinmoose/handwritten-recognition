import os
from flask import render_template, request, flash
from app import app
from app.forms import (UploadForm, ResultForm)
from datetime import datetime
from werkzeug.utils import secure_filename
import numpy as np
#from keras_preprocessing import image
from keras.utils import load_img, img_to_array
from keras.models import load_model
from PIL import Image

model_s = load_model('app/static/model/mnist.h5')
path = ""
secure_files = []

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tiff'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def evaluate_img(path):
    img = image.load_img(path, color_mode='grayscale', target_size=(28,28))
    #if white_bg:
    #    img = Image.fromarray(np.invert(img))
    x = image.img_to_array(img)
    if np.average(x) - 128 > 0:
        x = 255 - x
    x /= 255
    x = np.expand_dims(x, axis=0)
    y_proba = model_s.predict(x)
    result  = y_proba.tolist()
    return result

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_filename = str(datetime.timestamp(datetime.now())) + \
                os.path.splitext(filename)[1]
            path = os.path.join(app.root_path,
                                'static/img/upload/', new_filename)
            file.save(path)
            result = evaluate_img(path)
            # result = evaluate_img(path, form.white_background.data)
            pred = int(np.argmax(result, axis=-1))
            form = ResultForm()
            return render_template("result.html", title="Result", form=form,
                path=os.path.join('static/img/upload/', new_filename),
                result=result[0], pred=pred)
        else:
            msg = "Wrong file format: " + file.filename
            flash(msg, "warning")
            return render_template("index.html", title="Home", form=form)
    else:
        return render_template("index.html", title="Home", form=form)

@app.route('/about', methods=['GET'])
def about():
    return render_template("about.html", title="About")