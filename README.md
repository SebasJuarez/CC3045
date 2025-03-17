# Laboratorio 6

Este es un juego de **Connect Four** desarrollado en **Python**. En este se permite jugar contra una **IA básica** o ver una partida de IA vs IA. 

## Inspiración y links
El codigo de la logica se hizo tomando en cuenta el codigo del [Gym Connect Four de OpenAI](https://github.com/IASIAI/gym-connect-four).

## Características
- Interfaz gráfica con **Pygame**.
- **Modo PvAI**: Juega contra una inteligencia artificial simple.
- **Modo AI vs AI**: Observa dos IA jugando entre sí.
- **Activacion del modo alpha-beta pruning**

## Instalación

Para ejecutar este proyecto, primero necesitas instalar las dependencias necesarias:

```sh
pip install pygame numpy
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

