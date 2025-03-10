# Q-Learning en Frozen Lake

Este proyecto implementa el algoritmo de **Q-learning** para resolver el juego **Frozen Lake** utilizando la librería **Gymnasium**. El agente aprende a moverse desde el inicio hasta la meta evitando caer en agujeros y lidiando con la naturaleza resbaladiza del hielo.

## Características
- Implementación de **Q-learning** con tabla Q.
- Entrenamiento progresivo con **reducción de exploración** (epsilon decay).
- **Evaluación automatizada** del agente después del entrenamiento.
- Posibilidad de realizar **múltiples pruebas** y obtener estadísticas de desempeño.
- **Visualización opcional** del juego en tiempo real.

## Instalación
Es importante tener Python instalado y ejecuta los siguientes comandos para instalar las dependencias:

```bash
pip install gymnasium numpy matplotlib
gymnasium[toy-text]
```

## Uso
Ejecuta el script principal para entrenar y evaluar el agente:

```bash
python FrozenLake.py
```

Si deseas **desactivar o activar la visualización**, puedes modificar la variable `visualize` en el código:

```python
visualize = False/True
```

## Resultados
El script realiza **múltiples pruebas** después del entrenamiento y muestra:
- **Tasa de éxito por prueba**
- **Tasa de éxito promedio con desviación estándar**

Ejemplo de salida:

```
Prueba 1: Tasa de éxito = 75.00%
Prueba 2: Tasa de éxito = 73.00%
...
Tasa de éxito promedio después de 10 pruebas: 72.60% ± 4.32%
```
