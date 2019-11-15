
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
C.onclick = function () {
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
var box;
var recjson, btop, bbottom, bleft, bright, recobj, bboxes= []

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
    cam = (parseInt(cam[cam.length - 1])+1).toString()
    console.log(cam)
    $.post('../fetch/bbox',{ cam:cam, fr: selectedFrame },
    function (response, status) {
        // console.log('res',response)
        recjson = response
        var hotspot_image = document.getElementById('hotspot_image')
        var box = document.getElementById('box')
        var iHeight, iWidth

        recobj = recjson
        var imageData = recobj.image
        // console.log(recobj)
        var im = new Image();

        var numb, node
        numb = recobj.object.length


        for (var i = 0; i < numb; i++) {
            // console.log("iii", i)
            node = document.createElement("div");
            node.id = "bbox" + i
            node.className = "bbox"
            var tes = recobj.object[i].feature
            var kkk = i
            // node.onclick = function () {
            // 	console.log("person ke",kkk)
            // 	console.log(tes)

            // };
            // node.addEventListener( 'click', function(){
            //   console.log("person ke",kkk)
            // 	console.log(tes)
            // } );
            node.setAttribute("onclick", "clicker(" + i + ");");
            box.appendChild(node)
            bboxes.push(node)
        }
        // var bbox = document.getElementById("bbox")
        // console.log(bboxes)
        im.onload = function () {
            iHeight = im.height
            iWidth = im.width
            var ratio = iHeight / iWidth
            var parentBoxW = box.offsetWidth
            // console.log("width", parentBoxW)
            // console.log("height:", parentBoxW * ratio)
            var parentBoxH = parentBoxW * ratio

            for (j = 0; j < numb; j++) {
                btop = recobj.object[j].bbox[0]
                bleft = recobj.object[j].bbox[1]
                bbottom = recobj.object[j].bbox[2]
                bright = recobj.object[j].bbox[3]

                var bbox = document.getElementById("bbox" + j)

                // console.log("jj", bboxes[j])
                // bbox.style.top = (btop/iHeight)*parentBoxH+"px"
                // bbox.style.left = (bleft/iWidth)*parentBoxW+"px"
                // bbox.style.bottom = (parentBoxH - ((bbottom/iHeight)*parentBoxH)) +"px"
                // bbox.style.right = (parentBoxW - ((bright/iWidth)*parentBoxW)) +"px"

                bbox.style.top = (btop / iHeight) * 100 + "%"
                bbox.style.left = (bleft / iWidth) * 100 + "%"
                bbox.style.bottom = (parentBoxH - ((bbottom / iHeight) * parentBoxH)) / parentBoxH * 100 + "%"
                bbox.style.right = (parentBoxW - ((bright / iWidth) * parentBoxW)) / parentBoxW * 100 + "%"
                bbox.style.border = "2px solid transparent"
                bbox.style.position = "absolute"
            }
        }

        im.src = '../static/'+imageData;
        // console.log(imageData)
        hotspot_image.src = im.src
    });
}
lapor = document.getElementById('lapor')
lapor.onclick = function () {
    title = document.getElementById('title').value
    reporter = 'Guest 1' //nanti ganti pake session
    image = document.getElementById('suspect').src;
    place = "lab AI" //nanti diganti pake nama kamera
    $.post('/lapor', { title, reporter, image, place },
        function (data, status) {
            if (status == "success") {
                console.log(data)
            } else {
                console.error(status)
            }
        })
}




function clicker(id) {
    var tebox = document.getElementById('bbox' + id)
    // console.log()
    for (i = 0; i < bboxes.length; i++) {
        if (i != id) {
            bboxes[i].style.border = "2px solid transparent"
        } else {
            bboxes[i].style.border = "2px solid #f00"
        }

    }
    // tebox.style.border = "2px solid #f00"
    // console.log(bboxes)
    // console.log( document.getElementById('bbox'+id))
    console.log("person ke", id)
    console.log("features:", recobj.object[id].feature)
}

