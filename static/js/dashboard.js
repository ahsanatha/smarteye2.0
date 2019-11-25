
var A = document.getElementById('A');
var B = document.getElementById('B');
// var C = document.getElementById('C');

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
// C.onclick = function () {
//     if (caml3.style.display == "block") {
//         caml3.style.display = "none";
//     } else {
//         caml3.style.display = "block";
//     }
// }




