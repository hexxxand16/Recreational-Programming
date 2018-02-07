var canvas = document.querySelector("canvas");

canvas.width = 1200;
canvas.height = 1200;
canvas.style.width = "600px";
canvas.style.height = "600px";
var c = canvas.getContext("2d");
c.scale(2, 2);

// Generates random numbers between a and b
function rng(a, b) {
    return Math.random() * (b - a) + a;
}

function Weapon(xpos, ypos, type, rarity) {
    this.x = xpos;
    this.y = ypos;
    this.rarity = rarity;
    this.type = type;

    this.draw = function() {
        image = new Image();
        image.src = "Sprites/Preview.png";

        switch(this.rarity) {
            case "common":
                c.strokeStyle = "white";
                break;
            case "uncommon":
                c.strokeStyle = "green";
                break;
            case "rare":
                c.strokeStyle = "blue";
                break;
            case "epic":
                c.strokeStyle = "rebeccapurple";
                break;
            case "legendary":
                c.strokeStyle = "orangered";
                break;
            case "mythical":
                c.strokeStyle = "violet";
                break;
            default:
                console.log("You made a typo you idiot.");
                break;
        }
        c.drawImage(image, 0, 0, 96, 96, this.x, this.y, 32, 32);
        c.rect(this.x, this.y, 32, 32);
        c.stroke();
    }
}

myWeapon = new Weapon(80, 80, "hi", "legendary");

function update() {
    requestAnimationFrame(update);
    c.fillStyle = "black";
    c.fillRect(0, 0, innerWidth, innerHeight);
    myWeapon.draw();
}

update();