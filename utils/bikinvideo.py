import glob
import os

pathVid = []
def generateAllVideo():
    global pathVid
    wildCamera = glob.glob('Res *')
    for i in wildCamera:
        filename = i.split("\\")[0]
        id = filename.split()[1]
        os.system('ffmpeg -framerate 30 -i "'+i+'"/'+'%d.jpg vid/"'+filename+'".mp4')
        os.system('ffmpeg -i vid/"'+filename+'".mp4 -codec copy -f dash -window_size 10 -min_seg_duration 30 -use_timeline 1 -init_seg_name '+filename+'-init.m4s -media_seg_name '+filename+'-$Time$.m4s vid/"'+filename+'".mpd')

def generateOneVideo(filepath):
    global pathVid
    filename = filepath.split("\\")[1]
    filename = filename.split()[0]+'_'+filename.split()[1]
    os.system('ffmpeg -y -framerate 30 -i "'+filepath+'"/'+'%d.jpg static/vid/"'+filename+'".mp4')
    os.system('ffmpeg -i static/vid/"'+filename+'".mp4 -codec copy -f dash -window_size 10 -min_seg_duration 30 -use_timeline 1 -init_seg_name '+filename+'-init.m4s -media_seg_name '+filename+'-$Time$.m4s static/vid/"'+filename+'".mpd')
    return filename

def generateSuspectVideo(filepath):
    cam = filepath.split('/')[1]
    cam = cam.split()[1]
    filename = 'suspect'+cam
    frames = set([int(i[0]) for i in [i[2].split('.') for i in [i.split('\\') for i in glob.glob('static\\Res '+cam+'\\*.jpg')]]])
    start = min(frames)
    id = filename
    os.system('ffmpeg -y -framerate 30  -start_number '+str(start)+' -i "'+filepath+'"/'+'%d.jpg  static/vid/"'+filename+'".mp4')
    os.system('ffmpeg -i static/vid/"'+filename+'".mp4 -codec copy -f dash -min_seg_duration 30 -init_seg_name '+filename+'-init.m4s -media_seg_name '+filename+'-$Time$.m4s static/vid/"'+filename+'".mpd')
    return filename+'.mpd'

if __name__ == "__main__":
    generateAllVideo()
