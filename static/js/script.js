
var vid = document.getElementById("video")
var frameRate = 10
var theInterval;

vid.onplay = function () {
    theInterval = setInterval(function () { getCurrentVideoFrame() }, (1000 / frameRate))
}
vid.onpause = function () {
    clearInterval(theInterval)
}

function getCurrentVideoFrame() {
    curTime = vid.currentTime
    theCurrentFrame = Math.floor(curTime * frameRate)
    // console.log(theCurrentFrame)
    return theCurrentFrame
}
function takeFrame() {
    fr = getCurrentVideoFrame()
    document.getElementById("gambar").src = "static/{{ camera }}/"+fr+".jpg"

}
