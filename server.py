from flask import Flask, escape, request, render_template,jsonify
import glob
import json
from utils.bikinvideo import generateSuspectVideo, generateOneVideo
from utils.find_suspect import find_suspect, find_idx_suspect
import os
from datetime import datetime
import time
import shutil
import numpy as np
import math


app = Flask(__name__)

cam_name = "Rec "

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    global cam_name
    wildCamera = glob.glob('static\\'+cam_name+'*')
    cameras = []
    for i in wildCamera:
        filename = i.split("\\")[1]
        id = filename.split()[1]
        cameras.append(filename)
    if request.method == 'GET':
        camera = cam_name+"0"
    elif request.method == "POST":
        if request.form.get("Camera") is None:
            camera = cam_name+"0"
        else :
            camera = request.form.get('Camera')
    if not os.path.exists('static\\vid\\'+camera.split()[0]+'_'+camera.split()[1]+'.mpd'):
        camera = generateOneVideo('static\\'+camera)
        return render_template('dashboard.html', cameras = cameras, camera=camera)
    else :
        return render_template('dashboard.html', cameras = cameras, camera=camera.split()[0]+'_'+camera.split()[1])

# @app.route('/cekClick', methods=['POST'])
# def cek():
#     x = request.form.get('x')
#     y = request.form.get('y')
#     fr = request.form.get('fr')
#     cam = request.form.get('cam')
#     with open('static\\Json Result '+cam+'\\result.json') as data_file:    
#         data = json.load(data_file)
#     obj_bbox = data['data'][int(fr)]['object']
#     distance = [] 
#     for dd in obj_bbox:
#         if len(dd['bbox']) > 0:
#             bb = dd['bbox'].copy()
#             center_bb = (bb[2]+bb[0])/2, (bb[3]+bb[1])/2
#             print('center ', center_bb)
#             dis = math.sqrt(pow(int(y)-bb[0],2)+pow(int(x)-bb[1],2))
#             distance.append(dis)
#     # print(distance)
#     bbox = obj_bbox[np.argmin(distance)]['bbox']
#     # print('bbox', bbox)
#     # print(len(obj_bbox))
#     obj_fitur = obj_bbox[np.argmin(distance)]['feature']
#     return jsonify({
#         "bbox" : bbox,
#         "obj_fitur" : obj_fitur
#     })

@app.route('/fetch/bbox', methods=['GET'])
def bbox():
    with open('0.json') as json_file:
        print(json_file)
        return json_file

@app.route('/lapor', methods=['POST'])
def lapor():
    report = {}
    report_dir = 'static\\report.json'
    report['title'] = request.form.get('title')
    report['reporter'] = request.form.get('reporter')
    report['place'] = request.form.get('place')
    report['image'] = request.form.get('image')
    report['elapsed'] = str(time.time())
    report['date'] = str(datetime.now().date())
    report['time'] = str(datetime.now().time())[:8]
    print(report)
    with open(report_dir) as data_file:    
        old_data = json.load(data_file)
    old_data['report'].append(report)
    with open(report_dir, 'w') as fp:
        json.dump(old_data, fp)
    return "new data added to db"
    
@app.route('/dash')
def dash():
    return render_template('dashboard.html')

@app.route('/cam/<id>')
def cam(id):
    camera = 'Rec '+str(id)
    filename = camera.split()[0]+'_'+camera.split()[1]
    return render_template('cam.html',camera = camera, filename = filename)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/findSuspect', methods=["POST"])
def getFrame():
    cam = request.form.get('camera')
    frameId = request.form.get('frameId')
    cam = cam.split('_')[1]
    with open('static\\Json Result '+cam+'\\result.json') as json_file:
        data = json.load(json_file)
    selectedData = data['data'][int(frameId)]['object']
    suspect_ft = selectedData[0]['feature']
    target_dir = 'static/Res '+cam
    print('target dir', target_dir)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    if len(suspect_ft) > 0 :
        frame_num, suspect_idx = find_idx_suspect(cam, suspect_ft, target_dir + str(cam))
        if (frame_num is not -1):
            find_suspect(cam, frame_num, suspect_ft, target_dir, 'forward')
            find_suspect(cam, frame_num, suspect_ft, target_dir, 'backward')
        path = generateSuspectVideo(target_dir)
    else :
        path = 'None'
    return path

    
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port =3000,debug = True)