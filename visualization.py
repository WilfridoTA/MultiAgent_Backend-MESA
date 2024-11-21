import numpy as np
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from agent_car import CarAgent
from agent_sempahore import SemaforoAgent
from model import CityModel

# Inicializar matrices
def show_agents(m):
  agent_counts = np.zeros((m.grid.width, m.grid.height))
  color_map = np.zeros((m.grid.width, m.grid.height))

  # Rellenar matrices
  for cell_content, (x, y) in m.grid.coord_iter():
      agent_count = len(cell_content)
      agent_counts[x][y] = agent_count
      for agent in cell_content:
          if isinstance(agent, SemaforoAgent):
              color_map[x][y] = 1 if agent.colorState else -1  # 1 para verde, -1 para rojo
          if isinstance(agent, CarAgent):
              color_map[x][y] = 2  # 2 para carros
      if m.grid.properties["Estacionamiento"].data[x, y]:
          color_map[x][y] = 3  # 3 para estacionamiento

  # Trasponer las matrices si es necesario
  #agent_counts = agent_counts.T
  #color_map = color_map.T

  # Crear una paleta de colores personalizada
  custom_cmap = sns.color_palette(["red", "white", "green", "blue", "yellow"], as_cmap=True)

  # Plot usando seaborn
  g = sns.heatmap(color_map, cmap=custom_cmap, annot=True, cbar=False, square=True, linewidths=0.5, linecolor='black')
  g.figure.set_size_inches(5, 5)
  g.set(title="Estado de los semáforos en la cuadricula")
  plt.show()

def show_all_agents(m):
    agent_counts = np.zeros((m.grid.width, m.grid.height))
    for cell_content, (x, y) in m.grid.coord_iter():
        agent_count = len(cell_content)
        agent_counts[x][y] = agent_count
    # Plot using seaborn, with a visual size of 5x5

    g = sns.heatmap(agent_counts, cmap="viridis", annot=True, cbar=False, square=True)
    g.figure.set_size_inches(5, 5)
    g.set(title="number of agents on each cell of the grid");