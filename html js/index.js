var canvas = document.querySelector("canvas");

canvas.width = 1200;
canvas.height = 1200;
canvas.style.width = "600px";
canvas.style.height = "600px";
var c = canvas.getContext("2d");
c.scale(2, 2);

function ship(xpos, ypos) {
    this.x = xpos;
    this.y = ypos;
    this.dx = 1;
    this.dy = 0;

    this.hp = 50;
    this.pow = 1;

    this.draw = function() {
        c.fillStyle = "rgb(0, 0, 0)";
        c.fillRect(this.x, this.y, 40, 40);
    }

    this.movement = function() {
        this.x += this.dx;
        this.y += this.dy;
    }
}


var player = new ship(400, 400);

function update() {
    requestAnimationFrame(update)
    c.clearRect(0, 0, innerWidth, innerHeight);
    player.draw();
    player.movement();
}

update()