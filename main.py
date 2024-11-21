from agent_car import CarAgent
from model import CityModel
from agent_sempahore import SemaforoAgent
import visualization

m=CityModel(10)
visualization.show_agents(m)
#while m.parked!=m.carsNum:
for i in range(5):
  m.step()
  visualization.show_agents(m)