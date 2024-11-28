from agents import CarAgent
from agents import SemaforoAgent
import mesa

class CityModel(mesa.Model):
    def __init__(self, carsNum, seed=None):
      super().__init__(seed=seed)
      self.carsNum = carsNum
      self.width=24
      self.height=24
      self.running = True
      self.parked=0

      #create property layers
      propertyUp=mesa.space.PropertyLayer("Up",self.width, self.height, 0)
      propertyDown=mesa.space.PropertyLayer("Down",self.width, self.height,0)
      propertyRight=mesa.space.PropertyLayer("Right",self.width, self.height, 0)
      propertyLeft=mesa.space.PropertyLayer("Left",self.width, self.height, 0)
      propertyEstacionamiento=mesa.space.PropertyLayer("Estacionamiento",self.width, self.height, 0)
      propertyBuilding=mesa.space.PropertyLayer("Building",self.width, self.height, 0)

      #create grid
      self.grid=mesa.space.MultiGrid(self.width, self.height, False,property_layers=[propertyEstacionamiento,propertyUp,propertyDown,propertyRight,propertyLeft,propertyBuilding])

      #define grid's property layers
      self.estacionamientos=[(2,9),(3,2),(3,17),(4,11),(4,20),(5,6),(8,8),(9,21),(10,4),(10,11),(10,16),(17,2),(17,17),(17,19),(20,5),(20,8),(20,19)]
      for i in range(len(self.estacionamientos)):
        self.grid.properties["Estacionamiento"].set_cell((self.estacionamientos[i][1],self.estacionamientos[i][0]),i+1)

      self.direccionDerecha=[[[1,11],[14,15]],[[15,21],[14,15]],[[12,14],[15,15]],[[7,11],[18,19]],[[0,22],[22,23]]]
      self.direccionIzquierda=[[[1,23],[0,1]],[[8,12],[5,6]],[[16,22],[6,7]],[[2,12],[12,13]],[[16,22],[12,13]],[[13,15],[12,12]],[[2,6],[18,19]]]
      self.direccionAbajo=[[[0,1],[0,21]],[[6,7],[15,21]],[[12,13],[1,11]],[[12,13],[15,21]],[[12,12],[12,14]]]
      self.direccionArriba=[[[6,7],[2,12]],[[14,15],[2,12]],[[14,15],[16,22]],[[15,15],[13,15]],[[18,19],[16,22]],[[22,23],[2,23]]]

      for r in self.direccionDerecha:
        for i in range(r[1][0],r[1][1]+1 ):
          for j in range(r[0][0],r[0][1]+1):
            self.grid.properties["Right"].set_cell((i,j),1)

      for l in self.direccionIzquierda:
        for i in range(l[1][0],l[1][1]+1):
          for j in range(l[0][0],l[0][1]+1):
            self.grid.properties["Left"].set_cell((i,j),1)

      for d in self.direccionAbajo:
        for i in range(d[1][0],d[1][1]+1):
          for j in range(d[0][0],d[0][1]+1):
            self.grid.properties["Down"].set_cell((i,j),1)

      for u in self.direccionArriba:
        for i in range(u[1][0],u[1][1]+1):
          for j in range(u[0][0],u[0][1]+1):
            self.grid.properties["Up"].set_cell((i,j),1)

      for i in range(self.height):
        for j in range(self.width):
          if self.grid.properties["Estacionamiento"].data[i,j]==0 and self.grid.properties["Down"].data[i,j]==0 and self.grid.properties["Up"].data[i,j]==0 and self.grid.properties["Right"].data[i,j]==0 and self.grid.properties["Left"].data[i,j]==0:
            self.grid.properties["Building"].set_cell((i,j),1)


      # --------------------------------- CREACIÓN DE SEMAFOROS ----------------------------------
      semVer = [[6,2],[7,2],[6,7],[7,7],[0,17],[1,17],[6,21],[7,21],[18,16],[19,16]] #Revisar esto | Valores invertidos
      semRoj = [[8,0],[8,1],[8,5],[8,6],[2,18],[2,19],[5,22],[5,23],[17,14],[17,15]]

      #Semaforos verdes
      for sv in semVer:
        self.grid.place_agent(SemaforoAgent(self,True, 0, "hor"),(sv[1],sv[0]))

      #Semaforos rojos
      for sr in semRoj:
        self.grid.place_agent(SemaforoAgent(self,False, 0, "ver"),(sr[1],sr[0]))


      # ------------------------------------  CREACIÓN DE CARROS  ------------------------------------
      estacionamientosSeleccionados=[]
      for _ in range(self.carsNum):
        estacionamiento = self.random.randrange(1,18)
        while estacionamiento in estacionamientosSeleccionados:
          estacionamiento = self.random.randrange(1,18)
        estacionamientosSeleccionados.append(estacionamiento)
        c = CarAgent(self,estacionamiento)
        added = False

        while not added: #Asegurar que el carro sea agregado y no se quede con posición NONE
          x = self.random.randrange(self.grid.width)
          y = self.random.randrange(self.grid.height)

          cellmates = self.grid.get_cell_list_contents([x,y])

          if not any(isinstance(agent, CarAgent) or isinstance(agent, SemaforoAgent) for agent in cellmates): #Revisamos que no tengamos agentes Carro en la celda
            #Revisar si la celda es viable
            if self.grid.properties["Up"].data[x,y]:
              self.grid.place_agent(c, (x, y))
              added = True
            elif self.grid.properties["Down"].data[x,y]:
              self.grid.place_agent(c, (x, y))
              added = True
            elif self.grid.properties["Left"].data[x,y]:
              self.grid.place_agent(c, (x, y))
              added = True
            elif self.grid.properties["Right"].data[x,y]:
              self.grid.place_agent(c, (x,y))
              added = True

        print(f"Carro #{c.unique_id} | agregado en posición: {c.pos}")

      self.running = True

    def step(self):
      for agent in self.agents:
        if isinstance(agent, CarAgent):
          agent.sayDistance()

      for agent in self.agents:
        if isinstance(agent, SemaforoAgent):
          agent.revisarDistancia()

      for agent in self.agents:
        if isinstance(agent, SemaforoAgent):
          agent.changeColor()

      for agent in self.agents:
        if isinstance(agent, SemaforoAgent):
          agent.reset()

      for agent in self.agents: #Iterar sobre todos los agentes del modelo
          if isinstance(agent, CarAgent):
              #Accioens para los carros
              if agent.isParked==False:
                if agent.isDestination()==False:
                  agent.move()
              else:
                pass