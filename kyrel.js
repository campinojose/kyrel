// Kyrel Game Engine
class Kyrel {
    constructor(width, height) {
        this.width = width;
        this.height = height;
        this.x = 0;
        this.y = 0;
        this.direction = 0; // 0: East, 1: South, 2: West, 3: North
        this.grid = [];
        this.carrying = 0;
        this.history = [];
        
        // Initialize grid
        for (let i = 0; i < height; i++) {
            this.grid[i] = [];
            for (let j = 0; j < width; j++) {
                this.grid[i][j] = {
                    balls: 0
                };
            }
        }
        
        this.saveState();
    }
    
    saveState() {
        this.history.push({
            x: this.x,
            y: this.y,
            direction: this.direction,
            grid: JSON.parse(JSON.stringify(this.grid)),
            carrying: this.carrying
        });
    }
    
    reset() {
        if (this.history.length > 0) {
            const initial = this.history[0];
            this.x = initial.x;
            this.y = initial.y;
            this.direction = initial.direction;
            this.grid = JSON.parse(JSON.stringify(initial.grid));
            this.carrying = initial.carrying;
            this.history = [initial];
        }
    }
    
    move() {
        const directions = [
            { dx: 1, dy: 0 },  // East
            { dx: 0, dy: 1 },  // South
            { dx: -1, dy: 0 }, // West
            { dx: 0, dy: -1 }  // North
        ];
        
        const dir = directions[this.direction];
        const newX = this.x + dir.dx;
        const newY = this.y + dir.dy;
        
        if (this.isValidPosition(newX, newY)) {
            this.x = newX;
            this.y = newY;
            this.saveState();
            return true;
        } else {
            throw new Error(`¡No puedo moverme! Posición fuera del grid: (${newX}, ${newY})`);
        }
    }
    
    turnLeft() {
        this.direction = (this.direction + 3) % 4; // Turn left = -1 (or +3) mod 4
        this.saveState();
    }
    
    turnRight() {
        this.direction = (this.direction + 1) % 4;
        this.saveState();
    }
    
    putBall() {
        this.grid[this.y][this.x].balls++;
        this.saveState();
    }
    
    takeBall() {
        if (this.grid[this.y][this.x].balls > 0) {
            this.grid[this.y][this.x].balls--;
            this.carrying++;
            this.saveState();
            return true;
        } else {
            throw new Error('¡No hay bolas para recoger en esta posición!');
        }
    }
    
    isValidPosition(x, y) {
        return x >= 0 && x < this.width && y >= 0 && y < this.height;
    }
    
    getDirectionName() {
        const names = ['Este', 'Sur', 'Oeste', 'Norte'];
        return names[this.direction];
    }
    
    getDirectionSymbol() {
        const symbols = ['→', '↓', '←', '↑'];
        return symbols[this.direction];
    }
    
    getBallsAtPosition(x, y) {
        return this.grid[y][x].balls;
    }
    
    getPosition() {
        return { x: this.x, y: this.y };
    }
    
    getCurrentState() {
        return {
            x: this.x,
            y: this.y,
            direction: this.direction,
            directionName: this.getDirectionName(),
            directionSymbol: this.getDirectionSymbol(),
            carrying: this.carrying,
            grid: this.grid
        };
    }
}

// Make Kyrel available globally
window.Kyrel = Kyrel;
