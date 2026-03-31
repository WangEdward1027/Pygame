const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');
const livesElement = document.getElementById('lives');
const gameOverElement = document.getElementById('gameOver');
const finalScoreElement = document.getElementById('finalScore');
const startBtn = document.getElementById('startBtn');
const restartBtn = document.getElementById('restartBtn');

const CELL_SIZE = 20;
const ROWS = 21;
const COLS = 19;

canvas.width = COLS * CELL_SIZE;
canvas.height = ROWS * CELL_SIZE;

const WALL = 1;
const DOT = 2;
const EMPTY = 0;
const POWER_DOT = 3;

const maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,3,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,3,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,2,1,1,1,1,1,2,1,2,1,1,2,1],
    [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
    [1,1,1,1,2,1,1,1,0,1,0,1,1,1,2,1,1,1,1],
    [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
    [1,1,1,1,2,1,0,1,1,0,1,1,0,1,2,1,1,1,1],
    [0,0,0,0,2,0,0,1,0,0,0,1,0,0,2,0,0,0,0],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,2,1],
    [1,3,2,1,2,2,2,2,2,0,2,2,2,2,2,1,2,3,1],
    [1,1,2,1,2,1,2,1,1,1,1,1,2,1,2,1,2,1,1],
    [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];

let pacman = {
    x: 9,
    y: 15,
    direction: 'right',
    nextDirection: 'right',
    mouthOpen: true
};

let ghosts = [
    { x: 9, y: 9, color: '#ff0000', direction: 'up', speed: 1 },
    { x: 8, y: 9, color: '#00ffff', direction: 'down', speed: 1 },
    { x: 10, y: 9, color: '#ffb8ff', direction: 'left', speed: 1 },
    { x: 9, y: 10, color: '#ffb852', direction: 'right', speed: 1 }
];

let score = 0;
let lives = 3;
let gameRunning = false;
let gameInterval;
let ghostInterval;
let powerMode = false;
let powerModeTimer;

function drawMaze() {
    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLS; col++) {
            const cell = maze[row][col];
            const x = col * CELL_SIZE;
            const y = row * CELL_SIZE;

            if (cell === WALL) {
                ctx.fillStyle = '#0000ff';
                ctx.fillRect(x, y, CELL_SIZE, CELL_SIZE);
                ctx.strokeStyle = '#0000aa';
                ctx.lineWidth = 2;
                ctx.strokeRect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2);
            } else if (cell === DOT) {
                ctx.fillStyle = '#ffcc00';
                ctx.beginPath();
                ctx.arc(x + CELL_SIZE / 2, y + CELL_SIZE / 2, 3, 0, Math.PI * 2);
                ctx.fill();
            } else if (cell === POWER_DOT) {
                ctx.fillStyle = '#ffcc00';
                ctx.beginPath();
                ctx.arc(x + CELL_SIZE / 2, y + CELL_SIZE / 2, 8, 0, Math.PI * 2);
                ctx.fill();
            }
        }
    }
}

function drawPacman() {
    const x = pacman.x * CELL_SIZE + CELL_SIZE / 2;
    const y = pacman.y * CELL_SIZE + CELL_SIZE / 2;
    const radius = CELL_SIZE / 2 - 2;

    ctx.fillStyle = '#ffff00';
    ctx.beginPath();

    let startAngle, endAngle;
    const mouthAngle = pacman.mouthOpen ? 0.2 : 0.05;

    switch (pacman.direction) {
        case 'right':
            startAngle = mouthAngle;
            endAngle = Math.PI * 2 - mouthAngle;
            break;
        case 'left':
            startAngle = Math.PI + mouthAngle;
            endAngle = Math.PI - mouthAngle;
            break;
        case 'up':
            startAngle = -Math.PI / 2 + mouthAngle;
            endAngle = -Math.PI / 2 - mouthAngle + Math.PI * 2;
            break;
        case 'down':
            startAngle = Math.PI / 2 + mouthAngle;
            endAngle = Math.PI / 2 - mouthAngle;
            break;
    }

    ctx.arc(x, y, radius, startAngle, endAngle);
    ctx.lineTo(x, y);
    ctx.closePath();
    ctx.fill();
}

function drawGhosts() {
    ghosts.forEach(ghost => {
        const x = ghost.x * CELL_SIZE + CELL_SIZE / 2;
        const y = ghost.y * CELL_SIZE + CELL_SIZE / 2;
        const radius = CELL_SIZE / 2 - 2;

        ctx.fillStyle = powerMode ? '#0000ff' : ghost.color;
        
        ctx.beginPath();
        ctx.arc(x, y - 2, radius, Math.PI, 0);
        ctx.lineTo(x + radius, y + radius);
        
        for (let i = 0; i < 3; i++) {
            const waveX = x + radius - (i + 1) * (radius * 2 / 3);
            ctx.quadraticCurveTo(waveX + radius / 3, y + radius + 5, waveX, y + radius);
        }
        
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(x - 4, y - 4, 4, 0, Math.PI * 2);
        ctx.arc(x + 4, y - 4, 4, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(x - 3, y - 3, 2, 0, Math.PI * 2);
        ctx.arc(x + 5, y - 3, 2, 0, Math.PI * 2);
        ctx.fill();
    });
}

function movePacman() {
    let newX = pacman.x;
    let newY = pacman.y;

    switch (pacman.nextDirection) {
        case 'up':
            if (canMove(pacman.x, pacman.y - 1)) {
                pacman.direction = 'up';
                newY--;
            }
            break;
        case 'down':
            if (canMove(pacman.x, pacman.y + 1)) {
                pacman.direction = 'down';
                newY++;
            }
            break;
        case 'left':
            if (canMove(pacman.x - 1, pacman.y)) {
                pacman.direction = 'left';
                newX--;
            }
            break;
        case 'right':
            if (canMove(pacman.x + 1, pacman.y)) {
                pacman.direction = 'right';
                newX++;
            }
            break;
    }

    if (newX !== pacman.x || newY !== pacman.y) {
        pacman.x = newX;
        pacman.y = newY;
        pacman.mouthOpen = !pacman.mouthOpen;

        if (maze[pacman.y][pacman.x] === DOT) {
            maze[pacman.y][pacman.x] = EMPTY;
            score += 10;
            scoreElement.textContent = score;
        } else if (maze[pacman.y][pacman.x] === POWER_DOT) {
            maze[pacman.y][pacman.x] = EMPTY;
            score += 50;
            scoreElement.textContent = score;
            activatePowerMode();
        }

        if (checkWin()) {
            gameOver(true);
        }
    } else {
        switch (pacman.direction) {
            case 'up':
                if (canMove(pacman.x, pacman.y - 1)) newY--;
                break;
            case 'down':
                if (canMove(pacman.x, pacman.y + 1)) newY++;
                break;
            case 'left':
                if (canMove(pacman.x - 1, pacman.y)) newX--;
                break;
            case 'right':
                if (canMove(pacman.x + 1, pacman.y)) newX++;
                break;
        }

        if (newX !== pacman.x || newY !== pacman.y) {
            pacman.x = newX;
            pacman.y = newY;
            pacman.mouthOpen = !pacman.mouthOpen;

            if (maze[pacman.y][pacman.x] === DOT) {
                maze[pacman.y][pacman.x] = EMPTY;
                score += 10;
                scoreElement.textContent = score;
            } else if (maze[pacman.y][pacman.x] === POWER_DOT) {
                maze[pacman.y][pacman.x] = EMPTY;
                score += 50;
                scoreElement.textContent = score;
                activatePowerMode();
            }

            if (checkWin()) {
                gameOver(true);
            }
        }
    }
}

function canMove(x, y) {
    if (x < 0 || x >= COLS || y < 0 || y >= ROWS) {
        return false;
    }
    return maze[y][x] !== WALL;
}

function moveGhosts() {
    ghosts.forEach(ghost => {
        const directions = ['up', 'down', 'left', 'right'];
        const validDirections = [];

        directions.forEach(dir => {
            let newX = ghost.x;
            let newY = ghost.y;

            switch (dir) {
                case 'up': newY--; break;
                case 'down': newY++; break;
                case 'left': newX--; break;
                case 'right': newX++; break;
            }

            if (canMove(newX, newY)) {
                validDirections.push(dir);
            }
        });

        if (validDirections.length > 0) {
            if (Math.random() < 0.7 && validDirections.includes(ghost.direction)) {
                let newX = ghost.x;
                let newY = ghost.y;

                switch (ghost.direction) {
                    case 'up': newY--; break;
                    case 'down': newY++; break;
                    case 'left': newX--; break;
                    case 'right': newX++; break;
                }

                if (canMove(newX, newY)) {
                    ghost.x = newX;
                    ghost.y = newY;
                } else {
                    const randomDir = validDirections[Math.floor(Math.random() * validDirections.length)];
                    ghost.direction = randomDir;
                    moveGhostInDirection(ghost, randomDir);
                }
            } else {
                const randomDir = validDirections[Math.floor(Math.random() * validDirections.length)];
                ghost.direction = randomDir;
                moveGhostInDirection(ghost, randomDir);
            }
        }
    });
}

function moveGhostInDirection(ghost, direction) {
    switch (direction) {
        case 'up': ghost.y--; break;
        case 'down': ghost.y++; break;
        case 'left': ghost.x--; break;
        case 'right': ghost.x++; break;
    }
}

function checkCollisions() {
    ghosts.forEach((ghost, index) => {
        if (ghost.x === pacman.x && ghost.y === pacman.y) {
            if (powerMode) {
                ghost.x = 9;
                ghost.y = 9;
                score += 200;
                scoreElement.textContent = score;
            } else {
                lives--;
                livesElement.textContent = lives;
                
                if (lives <= 0) {
                    gameOver(false);
                } else {
                    resetPositions();
                }
            }
        }
    });
}

function activatePowerMode() {
    powerMode = true;
    clearTimeout(powerModeTimer);
    powerModeTimer = setTimeout(() => {
        powerMode = false;
    }, 7000);
}

function resetPositions() {
    pacman.x = 9;
    pacman.y = 15;
    pacman.direction = 'right';
    pacman.nextDirection = 'right';

    ghosts.forEach((ghost, index) => {
        ghost.x = 9;
        ghost.y = 9;
    });
}

function checkWin() {
    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLS; col++) {
            if (maze[row][col] === DOT || maze[row][col] === POWER_DOT) {
                return false;
            }
        }
    }
    return true;
}

function gameOver(won) {
    gameRunning = false;
    clearInterval(gameInterval);
    clearInterval(ghostInterval);
    
    finalScoreElement.textContent = score;
    gameOverElement.classList.remove('hidden');
}

function draw() {
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    drawMaze();
    drawPacman();
    drawGhosts();
}

function gameLoop() {
    if (!gameRunning) return;
    
    movePacman();
    checkCollisions();
    draw();
}

function ghostLoop() {
    if (!gameRunning) return;
    
    moveGhosts();
    checkCollisions();
    draw();
}

function startGame() {
    score = 0;
    lives = 3;
    scoreElement.textContent = score;
    livesElement.textContent = lives;
    gameOverElement.classList.add('hidden');
    
    resetPositions();
    
    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLS; col++) {
            if (maze[row][col] === EMPTY) {
                if ((row === 1 || row === 3 || row === 5 || row === 14 || row === 16 || row === 18 || row === 19) && 
                    col !== 0 && col !== COLS - 1 && !(row === 19 && (col === 9))) {
                    maze[row][col] = DOT;
                }
            }
        }
    }
    
    maze[1][1] = POWER_DOT;
    maze[1][17] = POWER_DOT;
    maze[16][1] = POWER_DOT;
    maze[16][17] = POWER_DOT;
    
    gameRunning = true;
    clearInterval(gameInterval);
    clearInterval(ghostInterval);
    
    gameInterval = setInterval(gameLoop, 150);
    ghostInterval = setInterval(ghostLoop, 200);
    
    draw();
}

document.addEventListener('keydown', (e) => {
    if (!gameRunning) return;
    
    switch (e.key) {
        case 'ArrowUp':
            pacman.nextDirection = 'up';
            e.preventDefault();
            break;
        case 'ArrowDown':
            pacman.nextDirection = 'down';
            e.preventDefault();
            break;
        case 'ArrowLeft':
            pacman.nextDirection = 'left';
            e.preventDefault();
            break;
        case 'ArrowRight':
            pacman.nextDirection = 'right';
            e.preventDefault();
            break;
    }
});

startBtn.addEventListener('click', startGame);
restartBtn.addEventListener('click', startGame);

draw();
