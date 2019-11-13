
var A = document.getElementById('A');
var B = document.getElementById('B');

var caml1 = document.getElementById('caml1');
var caml2 = document.getElementById('caml2');

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
    console.log('<img src="static/Rec 0/'+getCurrentVideoFrame()+'.jpg" alt="">')
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
    // laporan = document.getElementById('laporan').value
    framer.innerHTML = '<img style="width:auto" src="../static/Rec 0/'+fr+'.jpg" alt="">'
    //TODO : Bikin Laporan
    //TODO : Pilih Orang
    //TODO : Rapiin Front-end (done)
    // $.post("/lapor", {laporan, image : fr, place : "{{ camera }}",  })
    // $.post("/findSuspect", { camera: "{{ camera }}", frameId: fr },
    //     function (data, status) {
    //         if (status == "success") {
    //             vid.src = 'static/vid/' + data
    //         } else {
    //             console.log(status)
    //         }
    //     })

}

