
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
    framer.innerHTML = '<img id="suspect" width="100%" src="../static/Rec '+cam+'/' + fr + '.jpg" alt="">'
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
// function printMousePos(event) {
//     // console.log("clientX: " + event.clientX + " - clientY: " + event.clientY, selectedFrame);

//     $.post('/cekClick', { x: event.clientX, y: event.clientY, fr: selectedFrame, cam},
//         function (data, status) {
//             if (status == 'success'){
//                 // console.log(data['bbox'])
//                 // console.log(data['obj_fitur'])
//             }
//     })

// }

// framer.addEventListener("click", printMousePos);


