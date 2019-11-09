from flask import Flask, escape, request, render_template
import glob

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def root():
    wildCamera = glob.glob('static\\Camera *')
    cameras = []
    for i in wildCamera:
        filename = i.split("\\")[1]
        id = filename.split()[1]
        # filename = filename.split()[0]+'_'+filename.split()[1]
        cameras.append(filename)
    if request.method == 'GET':
        camera = "Camera 0"
    elif request.method == "POST":
        camera = request.form.get("Camera")
        
    return render_template('index.html', cameras = cameras, camera=camera)

# @app.route('/takeframe')
# def getFrame()

if __name__ == '__main__':
   app.run(host="0.0.0.0" ,debug = True)