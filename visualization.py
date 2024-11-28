import numpy as np
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from agents import CarAgent
from agents import SemaforoAgent
from model import CityModel
from mesa.visualization import SolaraViz, make_plot_component, make_space_component #Para visualizar
import solara as sol

m=CityModel(4)
from mesa.visualization import Slider, SolaraViz, make_space_component


def agent_draw(agent):
  if isinstance(agent, SemaforoAgent):
    if agent.complexColorState==-1:
        return {"color": "red", "size": 40}
    elif agent.complexColorState==0:
        return {"color": "orange", "size": 40}
    elif agent.complexColorState==1:
        return {"color": "green", "size": 40}
  elif isinstance(agent, CarAgent):
    return {"color": "blue", "size": 10}

propertylayer_portrayal = {
    "Building": {"color": "grey", "opacity": 0.4, "condition": lambda val: val != 0, "colorbar":False},
    "Estacionamiento": {"color": "yellow", "opacity": 0.6, "condition": lambda val: val != 0, "colorbar":False},
}

model_params = {
    "seed": None,
    "carsNum": 17,
}

model = CityModel(17)

page = SolaraViz(
    model,
    components=[make_space_component(agent_portrayal=agent_draw, propertylayer_portrayal=propertylayer_portrayal, backend="matplotlib")],
    model_params=model_params,
    name="City Model",
)
page  # noqa

