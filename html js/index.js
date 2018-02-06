var canvas = document.querySelector("canvas");

canvas.width = 1200;
canvas.height = 1200;
canvas.style.width = "600px";
canvas.style.height = "600px";
var c = canvas.getContext("2d");
c.scale(2, 2);

function constrain(n, a, b) {
    if (n < a) {
        n = a;
    }
    if (n > b) {
        n = b;
    }
    return n;
}

// Generates random numbers between a and b (inclusive)
function rng(a, b) {
    return Math.random() * (b - a) + a
}

function ship(xpos, ypos) {
    this.x = xpos;
    this.y = ypos;
    this.dx = 0;
    this.dy = 0;
    this.max_vel = 3;

    this.hp = 50;
    this.pow = 1;

    this.draw = function() {
        c.fillStyle = "rgb(255, 255, 255)";
        this.x = constrain(this.x + this.dx, 0, 560);
        this.y = constrain(this.y + this.dy, 0, 560);
        c.strokeStyle = "rgb(255, 255, 255)"
        c.rect(this.x, this.y, 40, 40);
        c.stroke();
    }

    this.movement = function() {
        if (map[37]) {
            this.dx = -this.max_vel;
        }
        if (map[38]) {
            this.dy = -this.max_vel;
        }
        if (map[39]) {
            this.dx = this.max_vel;
        }
        if (map[40]) {
            this.dy = this.max_vel;
        }
        if (!map[37] && !map[39]) {
            this.dx = 0;
        }
        if (!map[38] && !map[40]) {
            this.dy = 0;
        }
    }
}

function bullet(xpos, ypos, dx, dy) {
    this.x = xpos;
    this.y = ypos;
    this.dx = dx;
    this.dy = dy;

    this.draw = function() {
        c.beginPath();
        c.arc(this.x, this.y, 5, 0, 2 * Math.PI);
        c.stroke();
    }
    
    this.movement = function() {
        this.x += this.dx;
        this.y += this.dy;
    }
}

function spray() {
    bullet_Array[bullet_Array.length] = new bullet(rng(0, 600), rng(0, 50), rng(-2, 2) , rng(1, 10));
}

var bullet_Array = [];
var map = {};
var player = new ship(400, 400);

onkeydown = onkeyup = function(e) {
    map[e.keyCode] = e.type == 'keydown';
}

window.setInterval(spray, 1);
function update() {
    requestAnimationFrame(update);
    c.fillStyle = "black";
    c.fillRect(0, 0, innerWidth, innerHeight);
    c.beginPath();
    player.draw();
    player.movement();
    for (var i = 0; i < bullet_Array.length; i++) {
        bullet_Array[i].draw();
        bullet_Array[i].movement();
        if (bullet_Array[i].y > 600 || bullet_Array.x > 600 || bullet_Array.x < 0) {
            bullet_Array.splice(i, 1);
        }
    }
}

update();