from flask import render_template,request
from flask import Flask, current_app, jsonify, make_response, request,session
from sklearn.cluster import KMeans
import pandas as pd
import itertools
from operator import itemgetter
from sklearn.preprocessing import MinMaxScaler
from PIL import Image
from flask import json
from werkzeug.utils import secure_filename
import os
import base64
import numpy as np
import re
from flask_restful import Api, Resource
from io import BytesIO
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './upload'

app.secret_key = 'oke bro'

@app.route('/')
def hello_world():
    return render_template('index.html')
@app.route('/example')
def example_page():
    return render_template('example.html')
@app.route('/apex')
def apex_page():
    return render_template('apex.html')

@app.route('/react')
def react_page():
    return render_template('react.html')

@app.route('/result')
def result_page():
    return render_template('result.html')

@app.route('/upload',methods = ['GET','POST'])
def upload_process():
    image = request.files["fileUpload"]
    image.save(os.path.join(app.config["UPLOAD_FOLDER"], image.filename))
    check =image.filename[-3:]
    if check =='csv':
        df = pd.read_csv('upload/'+image.filename)
    else:
        df = pd.read_excel("upload/"+image.filename)
    list = []
    for result in df.columns.values:
        list.append({'header': result})
    session['image_upload'] = image.filename
    return make_response(json.dumps(list), 200)

@app.route('/process_cluster',methods = ['GET','POST'])
def process_cluster():
    color = ['rgba(199, 205, 250, 1)', 'rgba(18, 41, 211, 1)', 'rgba(18, 211, 22, 1)', 'rgba(142, 86, 143, 1)',
             'rgba(223, 83, 83, .5)', 'rgba(0, 0, 0, 1)', 'rgba(255, 17, 0, 1)', 'rgba(166, 115, 89, 1)',
             'rgba(85, 64, 53, 1)']
    x_radio = request.form['x_radio']
    y_radio = request.form['y_radio']
    cluster = request.form['cluster']
    sess =session.get('image_upload')
    check = sess[-3:]
    if check =='csv':
        df = pd.read_csv('upload/'+session.get('image_upload'))
    else:
        df = pd.read_excel("upload/"+session.get('image_upload'))
    km = KMeans(n_clusters=int(cluster))

    y_predicted = km.fit_predict(df[[y_radio,x_radio]])
    df['cluster'] = y_predicted
    km.cluster_centers_
    list = []
    for i in range(0, int(cluster)):
        list.append(df[df.cluster == int(i)].to_dict('records'))
    list_data = []
    centroid =[]
    for i in range(0, int(cluster)):
        centroid.append([km.cluster_centers_[:, 0][i],km.cluster_centers_[:, 1][i]])
        for y in list[i]:
            list_data.append(y)

    data = sorted(list_data, key=itemgetter('cluster'))
    val_dict =[]
    cent ={'name': 'Centroid', 'color': 'rgba(30, 130, 76, 1)',
     'data': centroid}
    val_dict.append(cent)
    for key, value in itertools.groupby(list_data, key=itemgetter('cluster')):
        my_dict = {"name": "Cluster" + str(key), "color": color[key]}
        clus = []
        for i in value:
            clus.append([i.get(x_radio), i.get(y_radio)])
        my_dict["data"] = clus
        val_dict.append(my_dict)




    # print(cent)
    return make_response(json.dumps(val_dict), 200)

if __name__ == '__main__':
    app.run()
