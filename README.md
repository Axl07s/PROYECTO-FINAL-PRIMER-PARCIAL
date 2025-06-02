📌 Requisitos del Sistema Mínimos:

Sistema Operativo: Windows 10 (64-bit) / macOS 10.15+ / Linux (Ubuntu 20.04+)

Procesador: Intel Core i3 o equivalente

Memoria RAM: 4 GB

Tarjeta gráfica: Intel HD Graphics 4000 o equivalente

Almacenamiento: 500 MB de espacio disponible

Python: Versión 3.8 o superior

Dependencias: Pygame 2.0+

Recomendados:
Procesador: Intel Core i5 o equivalente

Memoria RAM: 8 GB

Tarjeta gráfica: NVIDIA GTX 1050 / AMD RX 560 o superior

🕹️ Controles del Juego

Jugador 1 (Rojo):
Movimiento: W (arriba), A (izquierda), S (agacharse), D (derecha)

Saltar: W

Golpear: E

Jugador 2 (Lila):
Movimiento: Flechas (↑, ←, ↓, →)

Saltar: Flecha arriba (↑)

Golpear: 1 (tecla numérica)

Controles generales:
Pausa: ESC

Menú principal: ESC (en pausa)

Reiniciar partida: ESPACIO (al final del juego)

🎮 Cómo Jugar
Selección de dificultad:

En el menú de configuración puedes elegir entre:

Fácil: Para principiantes (más vida, menos daño)

Normal: Equilibrado

Difícil: Para expertos (menos vida, más daño)

Mecánicas del juego:

Cada jugador comienza con 100 puntos de vida (varía según dificultad)

Ganas una ronda reduciendo la vida del oponente a 0

El primero en ganar 2 rondas gana el combate

Cada combate tiene 3 rondas máximo

Movimientos especiales:

Salto: Presiona arriba (W o ↑) para esquivar golpes

Agacharse: Presiona abajo (S o ↓) para evitar golpes altos

Combo: Golpea repetidamente para encadenar ataques

⚙️ Instalación
Clona el repositorio:

git clone https://github.com/tu-usuario/stickman-fighters-kombat.git

cd stickman-fighters-kombat

Instala las dependencias:
pip install -r requirements.txt

Ejecuta el juego:
python main.py


📂 Estructura de archivos
stickman-fighters-kombat/
├── assets/
│   ├── audio/       # Efectos de sonido y música
│── fondos      # Imágenes de fondo
│── sprites     # Sprites de los personajes
├── Mapas/           # Fondos de los niveles
├── main.py          # Punto de entrada principal
├── juego.py         # Lógica principal del juego
├── menu_principal.py # Menú inicial
├── menu_config.py   # Menú de configuración
├── menu_pausa.py    # Menú de pausa
└── README.md        # Este archivo
🎯 Objetivo del Juego
Derrota a tu oponente en un combate al mejor de 3 rondas. Usa estrategia para esquivar ataques y contraatacar en el momento adecuado.
