#---------------------------
# Autor: Sebastian Juárez - 21471
#---------------------------

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import heapq
from abc import ABC, abstractmethod
import os

# Task 1.1 - Graph Search

# Funcion que toma la imagen y la convierte en una matriz de pixeles
def load_and_discretize_image(image_path, block_size=1):
    image = Image.open(image_path).convert('RGB')
    image_array = np.array(image)
    
    height, width, _ = image_array.shape
    
    color_map = {(255, 255, 255): 0, (0, 0, 0): 1, (5, 252, 6): 2, (254, 0, 0): 3}
    
    # Convertimos la imagen a una matriz de colores discretos
    flattened = image_array.reshape(-1, 3)
    discretized_matrix = np.array([color_map.get(tuple(pixel), 0) for pixel in flattened])
    discretized_matrix = discretized_matrix.reshape(height, width)
    
    # Pixeleamos la imagen
    new_height = height // block_size
    new_width = width // block_size
    reduced_matrix = np.full((new_height, new_width), -1, dtype=int)
    
    for i in range(new_height):
        for j in range(new_width):
            block = discretized_matrix[i * block_size:(i + 1) * block_size, j * block_size:(j + 1) * block_size]
            unique, counts = np.unique(block, return_counts=True)
            most_frequent = unique[np.argmax(counts)]
            reduced_matrix[i, j] = most_frequent
    
    print(f"Discretized matrix:\n{reduced_matrix}")
    return reduced_matrix

# Task 1.2 - Framework de problemas

class MazeProblem(ABC):
    def __init__(self, maze_matrix):
        self.maze = maze_matrix
        self.height, self.width = maze_matrix.shape
        self.start = self.find_position(3)  # Puntos de inicio (punto rojo)
        self.goals = self.find_positions(2)  # Puntos de llegada (punto/s verde/s)
        
        # Posiciones de inicio y metas
        # print(f"Start position (red): {self.start}")
        # print(f"Goal positions (green): {self.goals}")

    # Funcion que encuentra la primera posicion en la matriz
    def find_position(self, value):
        result = np.argwhere(self.maze == value)
        return tuple(result[0]) if len(result) > 0 else None
    
    # Funcion que encuentra todas las posiciones en la matriz
    def find_positions(self, value):
        return [tuple(pos) for pos in np.argwhere(self.maze == value)]

    # Metodos abstractos
    @abstractmethod
    def actions(self, state):
        pass

    @abstractmethod
    def result(self, state, action):
        pass

    @abstractmethod
    def goal_test(self, state):
        pass

    @abstractmethod
    def step_cost(self, state, action, next_state):
        pass

class MazeSolver(MazeProblem):
    
    def __init__(self, maze_matrix):
        super().__init__(maze_matrix)
        self.moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Movimientos: derecha, izquierda, abajo, arriba
    
    # Funcion que devuelve los movimientos posibles desde el estado actual
    def actions(self, state):
        valid_actions = []
        for move in self.moves:
            new_state = (state[0] + move[0], state[1] + move[1])
            if 0 <= new_state[0] < self.height and 0 <= new_state[1] < self.width:
                if self.maze[new_state] != 1:  # Bloquea los puntos negros y los identifica como paredes
                    valid_actions.append(move)
        return valid_actions
    
    # Funcion que devuelve el nuevo estado despues de realizar una accion
    def result(self, state, action):
        return (state[0] + action[0], state[1] + action[1])
    
    # Funcion que verifica si el estado actual es la meta
    def goal_test(self, state):
        return state in self.goals
    
    # Funcion que devuelve el costo de un paso
    def step_cost(self, state, action, next_state):
        return 1
    
# Task 1.3 - Graph Search Algorithms

# Clase base para algoritmos de búsqueda en grafos
class GraphSearch(ABC):
    
    def __init__(self, problem):
        self.problem = problem

    @abstractmethod
    def search(self):
        pass

# Implementación de Búsqueda en Anchura (Breadth-First Search)
class BFS(GraphSearch):
    
    def search(self):
        frontier = deque([self.problem.start])
        explored = set()
        parent_map = {self.problem.start: None}
        
        while frontier:
            state = frontier.popleft()
            if self.problem.goal_test(state):
                return self.reconstruct_path(parent_map, state)
            
            explored.add(state)
            for action in self.problem.actions(state):
                child = self.problem.result(state, action)
                if child not in explored and child not in frontier:
                    parent_map[child] = state
                    frontier.append(child)
        
        return None
    
    def reconstruct_path(self, parent_map, goal_state):
        path = []
        while goal_state is not None:
            path.append(goal_state)
            goal_state = parent_map[goal_state]
        return path[::-1]

# Implementación de Búsqueda en Profundidad (Depth-First Search)
class DFS(GraphSearch):
    
    def search(self):
        frontier = [self.problem.start]
        explored = set()
        parent_map = {self.problem.start: None}
        
        while frontier:
            state = frontier.pop()
            if self.problem.goal_test(state):
                return self.reconstruct_path(parent_map, state)
            
            explored.add(state)
            for action in self.problem.actions(state):
                child = self.problem.result(state, action)
                if child not in explored and child not in frontier:
                    parent_map[child] = state
                    frontier.append(child)
        
        return None
    
    def reconstruct_path(self, parent_map, goal_state):
        path = []
        while goal_state is not None:
            path.append(goal_state)
            goal_state = parent_map[goal_state]
        return path[::-1]

# Implementación de A* con heurísticas personalizadas
class AStar(GraphSearch):
    
    def __init__(self, problem, heuristic):
        super().__init__(problem)
        self.heuristic = heuristic
    
    def search(self):
        frontier = []
        heapq.heappush(frontier, (0, self.problem.start))
        explored = {}
        parent_map = {self.problem.start: None}
        g_cost = {self.problem.start: 0}
        
        while frontier:
            _, state = heapq.heappop(frontier)
            if self.problem.goal_test(state):
                return self.reconstruct_path(parent_map, state)
            
            explored[state] = True
            for action in self.problem.actions(state):
                child = self.problem.result(state, action)
                new_cost = g_cost[state] + self.problem.step_cost(state, action, child)
                
                if child not in explored or new_cost < g_cost.get(child, float('inf')):
                    parent_map[child] = state
                    g_cost[child] = new_cost
                    f_cost = new_cost + self.heuristic(child, self.problem.goals)
                    heapq.heappush(frontier, (f_cost, child))
        
        return None
    
    def reconstruct_path(self, parent_map, goal_state):
        path = []
        while goal_state is not None:
            path.append(goal_state)
            goal_state = parent_map[goal_state]
        return path[::-1]

# Definición de heurísticas para A*
def manhattan_heuristic(state, goals):
    if not goals:
        return float('inf')  # Retornar un valor grande si no hay metas
    return min(abs(state[0] - g[0]) + abs(state[1] - g[1]) for g in goals)

def euclidean_heuristic(state, goals):
    if not goals:
        return float('inf')  # Retornar un valor grande si no hay metas
    return min(((state[0] - g[0]) ** 2 + (state[1] - g[1]) ** 2) ** 0.5 for g in goals)

# Task 1.4 - Visualización de la Solución

# Función para visualizar la solución en el laberinto
def visualize_solution(maze, path, original_filename):
    maze_copy = np.copy(maze)
    for pos in path:
        if maze_copy[pos] not in [2, 3]:
            maze_copy[pos] = 4
    
    cmap = plt.cm.colors.ListedColormap(["white", "black", "green", "red", "blue"])
    plt.imshow(maze_copy, cmap=cmap)
    plt.colorbar()
    plt.show()
    
    # Guarda la imagen en la carpeta de soluciones
    solution_folder = './soluciones'
    os.makedirs(solution_folder, exist_ok=True)
    solution_filename = os.path.join(solution_folder, f'solucion-{os.path.basename(original_filename)}')
    plt.imsave(solution_filename, maze_copy, cmap=cmap)

# Main

if __name__ == "__main__":
    # image_path = './images/Test.bmp'
    image_path = './images/Test2.bmp'
    # image_path = './images/Prueba-Lab1.bmp'
    # image_path = './images/turing.bmp'
    maze_matrix = load_and_discretize_image(image_path)
    problem = MazeSolver(maze_matrix)
    
    solvers = [
        ("BFS", BFS(problem)),
        ("DFS", DFS(problem)),
        ("A* (Manhattan)", AStar(problem, manhattan_heuristic)),
        ("A* (Euclidean)", AStar(problem, euclidean_heuristic))
    ]
    
    solution_found = False
    
    for solver_name, solver in solvers:
        print(f"Trying {solver_name}...")
        solution_path = solver.search()
        
        if solution_path:
            # print(f"{solver_name} Solution Path:", solution_path)
            visualize_solution(maze_matrix, solution_path, image_path)
            solution_found = True
            break
        else:
            print(f"No hay una solución encontrada para {solver_name}")
    
    if not solution_found:
        print("No se encontró una solución para el problema.")