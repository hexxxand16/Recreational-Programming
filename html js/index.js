var canvas = document.querySelector("canvas");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

var c = canvas.getContext("2d");

c.lineWidth = 2;
for (var i = 0; i < 10; i++) {
    for (var j = 0; j < 10; j++) {
        c.fillStyle = "rgba(255, 255, 255, 1)";
        c.rect(10 + 40 * j, 10 + 50 * i, 40, 40);
        if (j % 2 === 0) {
            c.fillStyle = "rgba(0, 0, 0, 1)";
            c.fillRect(12 + 40 * j, 12 + 50 * i, 36, 36);
        }
    }
}
c.stroke();