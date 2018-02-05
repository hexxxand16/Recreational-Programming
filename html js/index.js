var canvas = document.querySelector("canvas");

canvas.width = 1200;
canvas.height = 1200;
canvas.style.width = "600px";
canvas.style.height = "600px";
var c = canvas.getContext("2d");
c.scale(2, 2);

c.font = "18px Arial";
c.lineWidth = 2;
for (var i = 0; i < 10; i++) {
    for (var j = 0; j < 10; j++) {
        c.fillStyle = "rgb(255, 255, 255)";
        c.rect(80 + 40 * j, 10 + 50 * i, 40, 40);
        if (j % 2 === 0) {
            c.fillStyle = "rgb(0, 0, 0)";
            c.fillRect(82 + 40 * j, 12 + 50 * i, 36, 36);
        }
    }
    c.fillStyle = "rgb(0, 0, 0)";
    c.fillText("6 6", 20, 38 + 50 * i);
}
c.stroke();