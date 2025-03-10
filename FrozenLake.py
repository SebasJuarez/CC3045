# Autor: Sebastian Juárez

import numpy as np
import gymnasium as gym
import random

# Parámetros de Q-learning - Primeras pruebas
alpha = 0.1  # Tasa de aprendizaje
gamma = 0.99  # Factor de descuento
epsilon = 1.0  # Probabilidad de exploración
epsilon_min = 0.01  # Mínimo de epsilon
epsilon_decay = 0.995  # Factor de reducción de epsilon
num_episodes = 5000  # Número de episodios
max_steps = 100  # Pasos máximos por episodio
visualize = False  # Si esta en False no se visualiza el entorno
num_trials = 10  # Número de pruebas para evaluar rendimiento

env = gym.make("FrozenLake-v1", is_slippery=True, render_mode="human" if visualize else None)

# se inicia la table Q con ceros
q_table = np.zeros((env.observation_space.n, env.action_space.n))

# Entrenamiento del agente con Q-learning
for episode in range(num_episodes):
    state, _ = env.reset()
    done = False
    for step in range(max_steps):
        # Elegir acción: exploración o explotación
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()  # Explorar 
        else:
            action = np.argmax(q_table[state, :])  # Explotar
        
        # Controles del entorno
        next_state, reward, done, truncated, _ = env.step(action)
        
        # Se actualiza la tabla Q usando la ecuación de Bellman
        q_table[state, action] = q_table[state, action] + alpha * (reward + gamma * np.max(q_table[next_state, :]) - q_table[state, action])
        
        state = next_state
        
        if done:
            break
    
    epsilon = max(epsilon_min, epsilon * epsilon_decay)

# Evaluación del agente en múltiples pruebas
overall_success_rates = []

# Se ejecutan las pruebas usando las políticas aprendidas
for trial in range(num_trials):
    successes = 0
    num_test_episodes = 100
    
    for _ in range(num_test_episodes):
        state, _ = env.reset()
        done = False
        for _ in range(max_steps):
            action = np.argmax(q_table[state, :])
            state, reward, done, truncated, _ = env.step(action)
            if done and reward == 1.0:
                successes += 1
                break
    
    success_rate = successes / num_test_episodes * 100
    overall_success_rates.append(success_rate)
    print(f"Prueba {trial + 1}: Tasa de éxito = {success_rate:.2f}%")

# Calculos de las pruebas y media del rendimiento
mean_success_rate = np.mean(overall_success_rates)
std_success_rate = np.std(overall_success_rates)
print(f"\nTasa de éxito promedio después de {num_trials} pruebas: {mean_success_rate:.2f}% ± {std_success_rate:.2f}%")

env.close()
