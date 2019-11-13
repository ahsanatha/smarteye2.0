
var A = document.getElementById('A');
var B = document.getElementById('B');
var C = document.getElementById('C');

var caml1 = document.getElementById('caml1');
var caml2 = document.getElementById('caml2');
var caml3 = document.getElementById('caml3');


// caml1.style.display = "none";
// caml2.style.display = "none";

A.onclick = function () {

    if (caml1.style.display == "block") {
        caml1.style.display = "none";
    } else {
        caml1.style.display = "block";
    }
}
B.onclick = function () {
    if (caml2.style.display == "block") {
        caml2.style.display = "none";
    } else {
        caml2.style.display = "block";
    }
}
C.onclick = function (){
    if (caml3.style.display == "block") {
        caml3.style.display = "none";
    } else {
        caml3.style.display = "block";
    }
}

var laporkan = document.getElementById('laporkan');
var pelapor = document.getElementById('pelapor');
var cancel = document.getElementById('cancel');
var framer = document.getElementById('framer');

pelapor.style.display = "none";
framer.style.display = "none";

laporkan.onclick = function () {
    laporkan.style.display = "none";
    pelapor.style.display = "block";
    framer.style.display = "block";
    takeFrame()
    testBbox()
}

cancel.onclick = function () {
    laporkan.style.display = "block";
    pelapor.style.display = "none";
    framer.style.display = "none";
    return false;
}

var vid = document.getElementById("vid")
var frameRate = 30
var theInterval;
var selectedFrame;
var cam;
var box;

vid.onplay = function () {
    theInterval = setInterval(function () { getCurrentVideoFrame() }, (1000 / frameRate))
}
vid.onpause = function () {
    clearInterval(theInterval)
}

function getCurrentVideoFrame() {
    curTime = vid.currentTime
    theCurrentFrame = Math.floor(curTime * frameRate)
    return theCurrentFrame
}
function takeFrame() {
    fr = getCurrentVideoFrame()
    selectedFrame = fr
    cam = window.location.href.split('/')
    cam = cam[cam.length-1]
    console.log(cam)
    framer.innerHTML = '<img id="suspect" src="../static/Rec '+cam+'/' + fr + '.jpg" alt="">'
}
lapor = document.getElementById('lapor')
lapor.onclick = function () {
    title = document.getElementById('title').value
    reporter = 'Guest 1' //nanti ganti pake session
    image = document.getElementById('suspect').src;
    place = "lab AI" //nanti diganti pake nama kamera
    //  console.log(title)
    $.post('/lapor', { title, reporter, image, place },
        function (data, status) {
            if (status == "success") {
                console.log(data)
            } else {
                console.error(status)
            }
        })
}
// define varible for arr bbox per object
var btop = [], bbottom = [], bleft = [], bright = []

function testBbox() {
    $.get("/fetch/bbox",{fr:selectedFrame}, function (data, status) {
        console.log(data)
        // data from json
        recobj = data
        var hotspot_image = document.getElementById('suspect')
        box = document.getElementById('framer')

        var iHeight, iWidth
        var bboxes = [], numb, node

        numb = recobj.object.length

        for (i = 0; i < numb; i++) {
            node = document.createElement("div");
            node.id = "bbox" + i
            box.appendChild(node)
            bboxes.push(node)
        }

        console.log(bboxes)
        
        iHeight = hotspot_image.height;
        iWidth = hotspot_image.width;
        // console.log(iHeight, bbottom[0])
        // console.log(width, bright[0])
        for (j = 0; j < numb; j++) {
            btop[j] = recobj.object[j].bbox[0]
            bleft[j] = recobj.object[j].bbox[1]
            bbottom[j] = recobj.object[j].bbox[2]
            bright[j] = recobj.object[j].bbox[3]

            var bbox = document.getElementById("bbox" + j)

            bbox.style.top = btop[j] + "px"
            bbox.style.left = bleft[j] + "px"
            bbox.style.bottom = (iHeight - bbottom[j]) + "px"
            bbox.style.right = (iWidth - bright[j]) + "px"
            bbox.style.border = "2px solid #FF0000"
            bbox.style.position = "absolute"
        }

    })
}

// framer.addEventListener('click',clickHotspotImage(event))

// jika image di click
function clickHotspotImage(event) {
    var xCoordinate = event.offsetX
    var yCoordinate = event.offsetY
    // console.log(xCoordinate, yCoordinate)
    // console.log(yCoordinate, btop)
    if (xCoordinate >= bleft[0] && xCoordinate <= bright[0]) {
        if (yCoordinate >= btop[0] && yCoordinate <= bbottom[0]) {
            console.log(xCoordinate, yCoordinate, "object 1")
        }
    } else if (xCoordinate >= bleft[1] && xCoordinate <= bright[1]) {
        if (yCoordinate >= btop[1] && yCoordinate <= bbottom[1]) {
            console.log(xCoordinate, yCoordinate, "object 2")
        }
    } else if (xCoordinate >= bleft[2] && xCoordinate <= bright[2]) {
        if (yCoordinate >= btop[2] && yCoordinate <= bbottom[2]) {
            console.log(xCoordinate, yCoordinate, "object 3")
        }
    } else if (xCoordinate >= bleft[3] && xCoordinate <= bright[3]) {
        if (yCoordinate >= btop[3] && yCoordinate <= bbottom[3]) {
            console.log(xCoordinate, yCoordinate, "object 4")
        }
    } else if (xCoordinate >= bleft[4] && xCoordinate <= bright[4]) {
        if (yCoordinate >= btop[4] && yCoordinate <= bbottom[4]) {
            console.log(xCoordinate, yCoordinate, "object 5")
        }
    } else if (xCoordinate >= bleft[5] && xCoordinate <= bright[5]) {
        if (yCoordinate >= btop[5] && yCoordinate <= bbottom[5]) {
            console.log(xCoordinate, yCoordinate, "object 6")
        }
    } else if (xCoordinate >= bleft[6] && xCoordinate <= bright[6]) {
        if (yCoordinate >= btop[6] && yCoordinate <= bbottom[6]) {
            console.log(xCoordinate, yCoordinate, "object 7")
        }
    }
}


