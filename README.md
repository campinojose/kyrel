# 🤖 Kyrel - Taller Tecnológico

Kyrel es un proyecto educativo interactivo para aprender programación de forma divertida. Controla a Kyrel, un robot que se mueve en una cuadrícula, utilizando comandos de JavaScript.

## 🎯 Objetivo

Aprender conceptos básicos de programación como:
- Secuencias de comandos
- Bucles (loops)
- Funciones
- Lógica de control
- Depuración de código

## 🚀 Cómo usar

1. Abre `index.html` en tu navegador web
2. Escribe código JavaScript en el editor
3. Haz clic en "Ejecutar" para ver a Kyrel en acción
4. Prueba los desafíos para practicar

## 📝 Comandos Disponibles

### Movimiento
- `kyrel.move()` - Mueve a Kyrel una casilla hacia adelante
- `kyrel.turnLeft()` - Gira a Kyrel 90 grados a la izquierda
- `kyrel.turnRight()` - Gira a Kyrel 90 grados a la derecha

### Interacción con Bolas
- `kyrel.putBall()` - Coloca una bola en la posición actual
- `kyrel.takeBall()` - Recoge una bola de la posición actual

## 💡 Ejemplos

### Ejemplo 1: Mover en línea recta
```javascript
kyrel.move();
kyrel.move();
kyrel.move();
```

### Ejemplo 2: Hacer un cuadrado
```javascript
for (let i = 0; i < 4; i++) {
    kyrel.move();
    kyrel.move();
    kyrel.move();
    kyrel.turnLeft();
}
```

### Ejemplo 3: Colocar bolas en patrón
```javascript
for (let i = 0; i < 5; i++) {
    kyrel.putBall();
    kyrel.move();
}
```

## 🎮 Desafíos

El proyecto incluye varios desafíos predefinidos:

1. **Línea Recta**: Coloca bolas en una línea de 5 casillas
2. **Cuadrado**: Dibuja el perímetro de un cuadrado con bolas
3. **Escalera**: Crea una escalera ascendente

## 🛠️ Tecnologías Utilizadas

- HTML5
- CSS3
- JavaScript (ES6+)

## 📚 Estructura del Proyecto

```
kyrel/
├── index.html      # Interfaz principal
├── styles.css      # Estilos visuales
├── kyrel.js        # Motor del juego Kyrel
├── app.js          # Lógica de la aplicación
└── README.md       # Este archivo
```

## 🎨 Características

- ✨ Interfaz visual moderna e intuitiva
- 🎯 Múltiples desafíos de programación
- 🎬 Animaciones suaves de movimiento
- 📱 Diseño responsive
- ⌨️ Atajo de teclado: Ctrl/Cmd + Enter para ejecutar

## 🤝 Contribuir

Este es un proyecto educativo. Siéntete libre de:
- Agregar nuevos desafíos
- Mejorar la interfaz
- Añadir más comandos a Kyrel
- Corregir errores

## 📄 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

## 👨‍💻 Autor

Proyecto creado como parte del Taller Tecnológico

---

¡Diviértete aprendiendo a programar con Kyrel! 🚀