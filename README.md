# Laboratorio 7

Este es un juego de **Connect Four** desarrollado en **Python**. En este se permite jugar contra una **IA básica** o ver una partida de IA vs IA en diferentes modos. 

## Inspiración y links
El código de la lógica se hizo tomando en cuenta el código del [Gym Connect Four de OpenAI](https://github.com/IASIAI/gym-connect-four).
Link al [video](https://youtu.be/folwdBaiDYQ)

## Características
- Interfaz gráfica con **Pygame**.
- **Modo PvAI**: Juega contra una inteligencia artificial simple.
- **Modo AI vs AI**: Observa dos IA jugando entre sí.
- **Activación del modo alpha-beta pruning**
- **IA con aprendizaje por refuerzo (Q-learning)**: La IA TD aprende de sus partidas.
- **Modo Minimax vs TD** y **Minimax+AB vs TD**, en 1 o múltiples partidas.
- **Modo TD vs TD**, para observar o evaluar partidas entre dos agentes que aprenden.
- **Estadísticas con gráficas** después de múltiples partidas.

## Instalación

Para ejecutar este proyecto, primero necesitas instalar las dependencias necesarias:

```sh
pip install pygame numpy matplotlib
```

## Cómo jugar
Ejecuta el script principal:

```sh
python ConnectFour.py
```

### Controles
- **Hacer un movimiento**: Haz clic en una columna para soltar tu ficha.
- **Salir del juego**: Cierra la ventana del juego.

## Lógica del juego
El juego se desarrolla de la siguiente manera:
1. El usuario elige una columna válida para soltar su ficha.
2. La ficha cae hasta la posición más baja disponible en la columna.
3. Se verifica si hay una condición de victoria.
4. Se alterna el turno entre el jugador y la IA.
5. El juego termina si alguien gana o el tablero se llena.