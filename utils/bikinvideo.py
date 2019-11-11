import glob
import os

pathVid = []
def generateAllVideo():
    global pathVid
    wildCamera = glob.glob('..\\static\\Camera *')
    for i in wildCamera:
        filename = i.split("\\")[2]
        id = filename.split()[1]
        # filename = filename.split()[0]+'_'+filename.split()[1]
        print(">>>>>>>>>>>>>>>>>>>>>>>>",filename, id)
        pathVid.append('../static/vid/'+filename)
        os.system('ffmpeg -framerate 10 -i "'+i+'"/'+'%d.jpg ../static/vid/"'+filename+'".mp4')
        os.system('ffmpeg -i ../static/vid/"'+filename+'".mp4 -codec copy -f dash -window_size 10 -min_seg_duration 30 -use_timeline 1 -init_seg_name '+str(id)+'-init.m4s -media_seg_name '+str(id)+'-$Time$.m4s ../static/vid/"'+filename+'".mpd')

def generateSuspectVideo(filepath, start):
    filename = 'suspect'+filepath.split('\\')[2]
    id = filename
    os.system('ffmpeg -framerate 10 -i "'+filepath+'"\\'+'%d.jpg  static/vid/"'+filename+'".mp4')
    os.system('ffmpeg -i static/vid/"'+filename+'".mp4 -codec copy -f dash -min_seg_duration 30 -init_seg_name '+str(id)+'-init.m4s -media_seg_name '+str(id)+'-$Time$.m4s static/vid/"'+filename+'".mpd')
    return filename+'.mp4'
    
def convertToMPD(pathVid):
    for i in pathVid:
        os.system('ffmpeg -i '+i+'.mp4 -c copy -f dash ../static/vid/Camera_0.mpd')
def apahayo():
    return "apaaa"

if __name__ == "__main__":
    generateAllVideo()
    # convertToMPD(pathVid)
    # print(pathVid)