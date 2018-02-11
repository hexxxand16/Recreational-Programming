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
var mouse = {
    x: undefined,
    y: undefined
};

window.addEventListener("mousemove", function(m) {
    mouse.x = m.x;
    mouse.y = m.y;
});

var set_1A = ["Wooden", "Paper", "Trash", "Candy", "Copper", "Blunt", "Cheese", "Rusted", "Broken", 
    "Inferior", "Unlucky", "Cursed", "Bronze"];
var set_1B = ["Superior", "Iron", "Steel", "Silver", "Gold", "Platinum", "Sharp", "Lucky", "Powerful", "Fiery",  
    "Frozen", "Beserker", "Magical"];
var set_1C = ["Titanium", "Diamond", "Obsidian", "Ultimate", "Evil", "Chaotic", "Unobtainium"];

function getRarityColour(rarity) {
    switch(rarity) {
        case "common":
            return "white";
        case "uncommon":
            return "green";
        case "rare":
            return "blue";
        case "epic":
            return "rebeccapurple";
        case "legendary":
            return "orangered";
        case "mythical":
            return "violet";
        default:
            console.log("You made a typo you idiot.");
            break;
    }
}

function Weapon(name, dmg, rarity) {
    this.name = name;
    this.rarity = rarity;
    this.minDmg = Math.max(Math.floor(dmg * 0.8), 1);
    this.maxDmg = Math.max(Math.floor(dmg * 1.2), 1);
    this.sprite = [0, 0];

    this.generateSprite = function(rarity) {
        if (rarity === "common" || rarity == "uncommon" || rarity == "rare") {
            this.sprite[0] = randInt(0, 3);
        } else {
            this.sprite[0] = randInt(4, 7);
        }
    }

    this.draw = function(xpos, ypos) {
        image = new Image();
        image.src = "Sprites/Preview.png";

        c.strokeStyle = getRarityColour(this.rarity)
        c.beginPath();        
        c.drawImage(image, 96 * this.sprite[0], 96 * this.sprite[1], 96, 96, xpos, ypos, 32, 32);
        c.rect(xpos, ypos, 32, 32);
        c.stroke();
    }

    this.generateSprite(this.rarity);
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
    enemy.hp -= Math.floor(rng(weapon.minDmg, weapon.maxDmg) - enemy.def / 2);
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

function generateName(rarity) {
    if (rarity === "common" || rarity === "uncommon") {
        return set_1A[randInt(0, set_1A.length - 1)] + " Sword";
    } else if (rarity === "rare"|| rarity == "epic") {
        return set_1B[randInt(0, set_1B.length - 1)] + " Sword";
    } else {
        return set_1C[randInt(0, set_1C.length - 1)] + " Sword";
    }
}

function generateATK(rarity, level) {
    var atk = randInt(1 + 2 * level, 3 + 2 * level);
    if (rarity === "uncommon") {
        atk *= 1.2;
    } else if (rarity === "rare") {
        atk *= 1.5;
    } else if (rarity === "epic") {
        atk *= 2;
    } else if (rarity === "legendary") {
        atk *= 2.5;
    } else if (rarity === "mythical") {
        atk *= 3;
    }
    return Math.floor(atk);
}

function createWeapon() {   
    var rarity = generateRarity();
    var name = generateName(rarity);
    var atk = generateATK(rarity, 1);
    var weapon = new Weapon(name, atk, rarity);
    inventory.push(weapon)
}

function spawnEnemy() {
    hp = randInt(50, 100);
    def = randInt(0, 10);
    var enemy = new Enemy(theEnemy.x, theEnemy.y, hp, def);
    return enemy;
}

function dispWindow(mouse) {
    var y = Math.floor((mouse.y - 200) / 36);
    var x = Math.floor(mouse.x / 36);
    var item = inventory[x + 16 * y]
    if (item != undefined) {
        c.beginPath();
        c.strokeStyle = "white"
        c.rect(mouse.x, mouse.y, 140, -200);
        c.fill();
        c.stroke();
        c.fillStyle = "white";
        c.fillText("Name: " + item.name, mouse.x, mouse.y - 190);
        c.fillText("Damage: " + item.minDmg + " - " + item.maxDmg, mouse.x, mouse.y - 180);
        c.fillStyle = getRarityColour(item.rarity);
        c.fillText("Rarity: " + item.rarity, mouse.x, mouse.y - 170)
    }
}

var inventory = [];
leftHand = new Weapon("Wooden Sword", 10, "legendary");
theEnemy = new Enemy(160, 160, 40, 0);

var spawnWeapon = setInterval(createWeapon, 250);
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
    dispWindow(mouse);
}

update();