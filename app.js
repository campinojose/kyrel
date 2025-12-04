// Main Application
let kyrel;
let gridSize = { width: 8, height: 8 };
let isRunning = false;

// Challenges
const challenges = {
    1: {
        title: 'Desafío 1: Línea Recta',
        description: 'Haz que Kyrel se mueva 5 casillas hacia adelante y coloque una bola en cada posición.',
        gridSize: { width: 8, height: 5 },
        startPos: { x: 0, y: 2 },
        solution: `// Solución sugerida:
for (let i = 0; i < 5; i++) {
    kyrel.putBall();
    if (i < 4) {
        kyrel.move();
    }
}`
    },
    2: {
        title: 'Desafío 2: Cuadrado',
        description: 'Haz que Kyrel dibuje un cuadrado de 3x3 usando bolas. Debe colocar bolas en el perímetro del cuadrado.',
        gridSize: { width: 6, height: 6 },
        startPos: { x: 1, y: 1 },
        solution: `// Solución sugerida:
for (let side = 0; side < 4; side++) {
    for (let i = 0; i < 3; i++) {
        kyrel.putBall();
        if (i < 2) {
            kyrel.move();
        }
    }
    kyrel.turnLeft();
}`
    },
    3: {
        title: 'Desafío 3: Escalera',
        description: 'Haz que Kyrel cree una escalera de 4 escalones. Cada escalón es una bola, y debe subir hacia la derecha y arriba.',
        gridSize: { width: 8, height: 8 },
        startPos: { x: 0, y: 4 },
        solution: `// Solución sugerida:
for (let i = 0; i < 4; i++) {
    kyrel.putBall();
    kyrel.move();
    kyrel.turnRight();
    kyrel.move();
    kyrel.turnLeft();
}`
    }
};

// Initialize the game
function initGame(width = 8, height = 8, startX = 0, startY = 0) {
    gridSize = { width, height };
    kyrel = new Kyrel(width, height);
    kyrel.x = startX;
    kyrel.y = startY;
    kyrel.saveState();
    renderGrid();
    updateStats();
}

// Render the grid
function renderGrid() {
    const gridContainer = document.getElementById('grid-container');
    gridContainer.innerHTML = '';
    gridContainer.style.gridTemplateColumns = `repeat(${gridSize.width}, 50px)`;
    gridContainer.style.gridTemplateRows = `repeat(${gridSize.height}, 50px)`;
    
    for (let y = 0; y < gridSize.height; y++) {
        for (let x = 0; x < gridSize.width; x++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.x = x;
            cell.dataset.y = y;
            
            // Check if Kyrel is at this position
            if (kyrel.x === x && kyrel.y === y) {
                cell.classList.add('kyrel');
                cell.textContent = kyrel.getDirectionSymbol();
            }
            
            // Check if there are balls at this position
            const balls = kyrel.getBallsAtPosition(x, y);
            if (balls > 0) {
                const ballElement = document.createElement('div');
                ballElement.className = 'ball';
                ballElement.textContent = balls > 1 ? balls : '';
                cell.appendChild(ballElement);
            }
            
            gridContainer.appendChild(cell);
        }
    }
}

// Update stats display
function updateStats() {
    document.getElementById('position').textContent = `X: ${kyrel.x}, Y: ${kyrel.y}`;
    document.getElementById('direction').textContent = kyrel.getDirectionName();
    document.getElementById('balls').textContent = kyrel.carrying;
}

// Execute user code
async function executeCode() {
    if (isRunning) return;
    
    isRunning = true;
    const code = document.getElementById('codeEditor').value;
    const runBtn = document.getElementById('runBtn');
    runBtn.disabled = true;
    runBtn.textContent = '⏳ Ejecutando...';
    
    try {
        // Create animation function
        const originalMove = kyrel.move.bind(kyrel);
        const originalTurnLeft = kyrel.turnLeft.bind(kyrel);
        const originalTurnRight = kyrel.turnRight.bind(kyrel);
        const originalPutBall = kyrel.putBall.bind(kyrel);
        const originalTakeBall = kyrel.takeBall.bind(kyrel);
        
        const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
        
        kyrel.move = async function() {
            originalMove();
            renderGrid();
            updateStats();
            await delay(300);
        };
        
        kyrel.turnLeft = async function() {
            originalTurnLeft();
            renderGrid();
            updateStats();
            await delay(200);
        };
        
        kyrel.turnRight = async function() {
            originalTurnRight();
            renderGrid();
            updateStats();
            await delay(200);
        };
        
        kyrel.putBall = async function() {
            originalPutBall();
            renderGrid();
            updateStats();
            await delay(200);
        };
        
        kyrel.takeBall = async function() {
            originalTakeBall();
            renderGrid();
            updateStats();
            await delay(200);
        };
        
        // Basic security validation - block obviously dangerous patterns
        // This is a simple educational tool, so we use a blacklist approach
        const dangerousPatterns = [
            /document\./gi,
            /window\./gi,
            /fetch\(/gi,
            /XMLHttpRequest/gi,
            /eval\(/gi,
            /import\s/gi,
            /require\(/gi,
            /__proto__/gi,
            /constructor/gi,
            /prototype/gi
        ];
        
        for (const pattern of dangerousPatterns) {
            if (pattern.test(code)) {
                throw new Error('El código contiene patrones no permitidos por seguridad.');
            }
        }
        
        // Execute the code in a more controlled manner
        // Using Function constructor with limited scope
        const executeFn = new Function('kyrel', `return (async function() { ${code} })();`);
        await executeFn(kyrel);
        
        
        // Restore original functions
        kyrel.move = originalMove;
        kyrel.turnLeft = originalTurnLeft;
        kyrel.turnRight = originalTurnRight;
        kyrel.putBall = originalPutBall;
        kyrel.takeBall = originalTakeBall;
        
        alert('✅ ¡Código ejecutado con éxito!');
    } catch (error) {
        alert('❌ Error: ' + error.message);
        console.error(error);
    } finally {
        isRunning = false;
        runBtn.disabled = false;
        runBtn.textContent = '▶ Ejecutar';
    }
}

// Reset game
function resetGame() {
    kyrel.reset();
    renderGrid();
    updateStats();
}

// Clear code editor
function clearCode() {
    document.getElementById('codeEditor').value = '';
}

// Load challenge
function loadChallenge(challengeId, targetButton) {
    const challenge = challenges[challengeId];
    if (!challenge) return;
    
    // Update active button
    document.querySelectorAll('.challenge-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    if (targetButton) {
        targetButton.classList.add('active');
    }
    
    // Update description - using textContent to prevent XSS
    const descElement = document.getElementById('challengeDescription');
    descElement.innerHTML = ''; // Clear previous content
    const titleElement = document.createElement('strong');
    titleElement.textContent = challenge.title;
    const descriptionElement = document.createElement('p');
    descriptionElement.textContent = challenge.description;
    descElement.appendChild(titleElement);
    descElement.appendChild(descriptionElement);
    
    // Initialize game with challenge settings
    initGame(
        challenge.gridSize.width,
        challenge.gridSize.height,
        challenge.startPos.x,
        challenge.startPos.y
    );
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize default game
    initGame();
    
    // Button event listeners
    document.getElementById('runBtn').addEventListener('click', executeCode);
    document.getElementById('resetBtn').addEventListener('click', resetGame);
    document.getElementById('clearBtn').addEventListener('click', clearCode);
    
    // Challenge buttons
    document.querySelectorAll('.challenge-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const challengeId = parseInt(btn.dataset.challenge);
            loadChallenge(challengeId, e.target);
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter to run code
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            executeCode();
        }
    });
});
