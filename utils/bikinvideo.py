import glob
import os

pathVid = []
def generateAllVideo():
    global pathVid
    wildCamera = glob.glob('Res *')
    for i in wildCamera:
        filename = i.split("\\")[0]
        id = filename.split()[1]
        print(">>>>>>>>>>>>>>>>>>>>>>>>",filename, id)
        os.system('ffmpeg -framerate 30 -i "'+i+'"/'+'%d.jpg vid/"'+filename+'".mp4')
        os.system('ffmpeg -i vid/"'+filename+'".mp4 -codec copy -f dash -window_size 10 -min_seg_duration 30 -use_timeline 1 -init_seg_name '+filename+'-init.m4s -media_seg_name '+filename+'-$Time$.m4s vid/"'+filename+'".mpd')

def generateSuspectVideo(filepath):
    cam = filepath.split(' ')[1]
    filename = 'suspect'+cam
    frames = set([int(i[0]) for i in [i[1].split('.') for i in [i.split('\\') for i in glob.glob('Res '+str(cam)+'\\*.jpg')]]])
    start = min(frames)
    id = filename
    os.system('ffmpeg -framerate 30  -start_number '+str(start)+' -i "'+filepath+'"\\'+'%d.jpg  vid/"'+filename+'".mp4')
    os.system('ffmpeg -i vid/"'+filename+'".mp4 -codec copy -f dash -min_seg_duration 30 -init_seg_name '+filename+'-init.m4s -media_seg_name '+filename+'-$Time$.m4s vid/"'+filename+'".mpd')
    return filename+'.mp4'
    
def convertToMPD(pathVid):
    for i in pathVid:
        os.system('ffmpeg -i '+i+'.mp4 -c copy -f dash ../static/vid/Camera_0.mpd')
def apahayo():
    return "apaaa"

if __name__ == "__main__":
    # generateAllVideo()
    for i in glob.glob('Res *'):
        print(generateSuspectVideo(i))
