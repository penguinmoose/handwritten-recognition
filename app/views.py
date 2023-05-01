import os
from flask import render_template, request, flash
from app import app
from app.forms import (UploadForm, ResultForm)
from datetime import datetime
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.utils import img_to_array
from keras.models import load_model
import cv2

model_s = load_model("app/static/model/mnist.h5")
path = ""
secure_files = []


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def evaluate_img(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Convert a color image to a grayscale image
    ret, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    # Convert the grayscale image to blak and white image
    # cv2.imshow('threh',thresh)
    # cv2.waitKey(0)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    # Define size of kernel
    dilation = cv2.dilate(thresh, rect_kernel, iterations=5)
    # cv2.dilate makes the font thicker.
    # cv2.imshow('dilation',dilation)
    # cv2.waitKey(0)
    contors, hierarchy = cv2.findContours(
        dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.findCOntours find groups of continuous color/brightness changes
    sorted_ctrs = sorted(
        contors, key=lambda contors: cv2.boundingRect(contors)[0])
    # sort the contors by upper left coordinate
    #print("Contors: ", sorted_ctrs)
    im2 = dilation.copy()
    results = []
    num_img = 0
    try:
        x = os.mkdir(path[:-4])
    except:
        print("Mkdir error", x)
    for i in sorted_ctrs:
        x, y, w, h = cv2.boundingRect(sorted_ctrs[num_img])
        # cv2.boundingRect returns the upper left cordinates, width, and height that
        # can encloses a contour
        print("print x, y, w, h:", x, y, w, h)
        cropped = im2[y:y+h, x:x+w]
        # Extract an image from the larger image
        bg = np.zeros((28, 28), np.uint8)
        if w >= h:
            resized = cv2.resize(
                cropped, (26, int(round(26*h/w))), interpolation=cv2.INTER_AREA)
            # cv2.resize resies the given image with specified interporation method
            rh, rw = resized.shape
            print("Shape:", rh, rw)
            bg[round((28-rh)/2):round((28-rh)/2)+rh, 1:27] = resized
        else:
            resized = cv2.resize(
                cropped, (int(round(26*w/h)), 26), interpolation=cv2.INTER_AREA)
            rh, rw = resized.shape
            print("Shape:", rh, rw)
            bg[1:27, round((28-rw)/2):round((28-rw)/2)+rw] = resized
        # cv2.imshow('resized_centered', bg)
        # cv2.waitKey(0)
        char_path = os.path.join(path[:-4], str(num_img)+".png")
        cv2.imwrite(char_path, bg)
        img_path = char_path.split("app")[1]
        x = img_to_array(bg)
        #print ("Ave - 128: ", np.average(x)-128)
        if np.average(x)-128 > 0:
            x = 255 - x
            #print ("Inversed Ave: ", np.average(x))
        x /= 255
        x = np.expand_dims(x, axis=0)
        y_proba = model_s.predict(x)
        result = y_proba.tolist()
        pred = int(np.argmax(result, axis=-1))
        results.append([result[0], pred, img_path])
        num_img += 1
    return (results)


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
            results = evaluate_img(path)
            print(results)
            form = ResultForm()
            return render_template("result.html", title="Result", form=form,
                                   path=os.path.join(
                                       'static\\img\\upload\\', new_filename),
                                   results=results)
        else:
            msg = "Wrong file format: " + file.filename
            flash(msg, "warning")
            return render_template("index.html", title="Home", form=form)
    else:
        return render_template("index.html", title="Home", form=form)


@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html", title="About")