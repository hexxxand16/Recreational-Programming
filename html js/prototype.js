var canvas = document.querySelector("canvas");

canvas.width = 1200;
canvas.height = 1200;
canvas.style.width = "600px";
canvas.style.height = "600px";
var c = canvas.getContext("2d");
c.scale(2, 2);

// Generates random numbers between a and b (inclusive)
function rng(a, b) {
    return Math.random() * (b - a) + a;
}

// Generates random intergers between a and b (inclusive)
function randInt(a, b) {
    return Math.floor(rng(a, b + 1))
}

function Weapon(name, dmg, rarity) {
    this.name = name;
    this.rarity = rarity;
    this.minDmg = Math.max(Math.floor(dmg * 0.8), 1);
    this.maxDmg = Math.max(Math.floor(dmg * 1.2), 1);

    this.draw = function(xpos, ypos) {
        image = new Image();
        image.src = "Sprites/Preview.png";
        c.beginPath();

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
        c.drawImage(image, 0, 0, 96, 96, xpos, ypos, 32, 32);
        c.rect(xpos, ypos, 32, 32);
        c.stroke();
    }
}

function Enemy(xpos, ypos, hp, def) {
    this.x = xpos;
    this.y = ypos;
    this.hp = hp;
    this.def = def;

    this.draw = function() {
        c.fillStyle = "red";
        c.fillRect(this.x, this.y, 40, 40);
    }
}

function attack(weapon, enemy) {
    enemy.hp -= Math.floor(rng(weapon.minDmg, weapon.maxDmg));
    console.log(enemy.hp)
}

function generateRarity() {
    var p = randInt(0, 2550)
    if (p <= 1999) {
        return "common";
    } else if (p <= 2399) {
        return "uncommon";
    } else if (p <= 2499) {
        return "rare";
    } else if (p <= 2539) {
        return "epic";
    } else if (p <= 2549) {
        return "legendary";
    } else {
        return "mythical";
    }
}

function createWeapon() {
    var name = "Steel Sword";    
    var rarity = generateRarity();
    var atk = randInt(1, 10);
    var weapon = new Weapon(name, atk, rarity);
    inventory.push(weapon)
}

function spawnEnemy() {
    hp = randInt(50, 100);
    def = randInt(0, 20);
    var enemy = new Enemy(theEnemy.x, theEnemy.y, hp, def);
    return enemy;
}

var inventory = [];
var leftHand;
leftHand = new Weapon("Wooden Sword", 10, "legendary");
theEnemy = new Enemy(160, 160, 40, 0);

var spawnWeapon = setInterval(createWeapon, 5);
var dealDamage = setInterval(function() {attack(leftHand, theEnemy)}, 1000);
function update() {
    requestAnimationFrame(update);
    c.fillStyle = "black";
    c.fillRect(0, 0, innerWidth, innerHeight);
    leftHand.draw(40, 40);
    for (let i = 0; i < inventory.length; i++) {
        inventory[i].draw(36 * (i % 16), 200 + 36 * Math.floor(i / 16));
    }
    if (inventory.length > 176) {
        inventory = [];
    }
    if (theEnemy.hp <= 0) {
        theEnemy = spawnEnemy();
    }
}

update();