from flask import Flask, escape, request, render_template
import glob
import json
from utils.bikinvideo import generateSuspectVideo, generateOneVideo
from utils.find_suspect import find_suspect, find_idx_suspect
import os
import shutil

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
    

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/findSuspect', methods=["POST"])
def getFrame():
    cam = request.form.get('camera')
    frameId = request.form.get('frameId')
    cam = cam.split()[1]
    with open('static\\Json '+cam+'\\0.json') as json_file:
        data = json.load(json_file)
    selectedData = data['data'][int(frameId)]['object']
    suspect_ft = selectedData[0]['feature']
    target_dir = 'static/res/'
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    if len(suspect_ft) > 0 :
        frame_num, suspect_idx = find_idx_suspect(cam, suspect_ft, target_dir + str(cam))
        if (frame_num is not -1):
            find_suspect(cam, frame_num, suspect_ft, target_dir + str(cam), 'forward')
            find_suspect(cam, frame_num, suspect_ft, target_dir + str(cam), 'backward')
        frames = set([int(i[0]) for i in [i[3].split('.') for i in [i.split('\\') for i in glob.glob('static\\res\\'+str(cam)+'\\*.jpg')]]])
        first_frame = min(frames)
        print(first_frame)
        path = generateSuspectVideo('static\\res\\'+str(cam), first_frame)
    else :
        path = 'None'
    return path

    
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)