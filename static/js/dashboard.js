
    var A = document.getElementById('A');
    var B = document.getElementById('B');

    var caml1 = document.getElementById('caml1');
    var caml2 = document.getElementById('caml2');

    // caml1.style.display = "none";
    // caml2.style.display = "none";

    A.onclick = function() {
        
        if (caml1.style.display == "block") {
            caml1.style.display = "none";
        } else {
            caml1.style.display = "block";
        }
    }
    B.onclick = function() {
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

    laporkan.onclick = function() {
        laporkan.style.display = "none";
            pelapor.style.display = "block";
            framer.style.display = "block";
    }

    cancel.onclick = function() {
        laporkan.style.display = "block";
            pelapor.style.display = "none";
            framer.style.display = "none";
        return false;
    }


