import mesa
from agent_sempahore import SemaforoAgent
import time

class CarAgent(mesa.Agent):

  def __init__(self, model,destination):
    super().__init__(model)
    self.isParked = False
    self.isMoving = True
    self.destination = destination

    posDestination=self.model.grid.properties["Estacionamiento"].select_cells(lambda x: x == self.destination)
    posDestinationAround=[(posDestination[0][0]+1,posDestination[0][1]),(posDestination[0][0]-1,posDestination[0][1]),(posDestination[0][0],posDestination[0][1]+1),(posDestination[0][0],posDestination[0][1]-1)]
    for p in posDestinationAround:
      if self.model.grid.properties["Left"].data[p]==1 or self.model.grid.properties["Right"].data[p]==1 or self.model.grid.properties["Up"].data[p]==1 or self.model.grid.properties["Down"].data[p]==1:
        self.destinationStreet=p

  def move(self):
    possibleMoves=[]

    #select posible movements

    if self.model.grid.properties["Left"].data[self.pos] == 1 :
      possibleMoves.append((self.pos[0],self.pos[1]-1))
      if self.pos[0]!=self.model.grid.width-1:
        if self.model.grid.properties["Left"].data[self.pos[0]+1,self.pos[1]-1]==1:
          possibleMoves.append((self.pos[0]+1,self.pos[1]-1))
      if self.pos[0]!=0:
        if self.model.grid.properties["Left"].data[self.pos[0]-1,self.pos[1]-1]==1:
          possibleMoves.append((self.pos[0]-1,self.pos[1]-1))

    if self.model.grid.properties["Right"].data[self.pos] == 1 :
      possibleMoves.append((self.pos[0],self.pos[1]+1))
      if self.pos[0]!=self.model.grid.width-1:
        if self.model.grid.properties["Right"].data[self.pos[0]+1,self.pos[1]+1]==1:
          possibleMoves.append((self.pos[0]+1,self.pos[1]+1))
      if self.pos[0]!=0:
        if self.model.grid.properties["Right"].data[self.pos[0]-1,self.pos[1]+1]==1:
          possibleMoves.append((self.pos[0]-1,self.pos[1]+1))

    if self.model.grid.properties["Up"].data[self.pos] == 1 :
      possibleMoves.append((self.pos[0]-1,self.pos[1]))
      if self.pos[1]!=self.model.grid.height-1:
        if self.model.grid.properties["Up"].data[self.pos[0]-1,self.pos[1]+1]==1:
          possibleMoves.append((self.pos[0]-1,self.pos[1]+1))
      if self.pos[1]!=0:
        if self.model.grid.properties["Up"].data[self.pos[0]-1,self.pos[1]-1]==1:
          possibleMoves.append((self.pos[0]-1,self.pos[1]-1))

    if self.model.grid.properties["Down"].data[self.pos] == 1 :
      possibleMoves.append((self.pos[0]+1,self.pos[1]))
      if self.pos[1]!=self.model.grid.height-1:
        if self.model.grid.properties["Down"].data[self.pos[0]+1,self.pos[1]+1]==1:
          possibleMoves.append((self.pos[0]+1,self.pos[1]+1))
      if self.pos[1]!=0:
        if self.model.grid.properties["Down"].data[self.pos[0]+1,self.pos[1]-1]==1:
          possibleMoves.append((self.pos[0]+1,self.pos[1]-1))

    #verify possible cells are available (there aren't cars in them) y semaforos
    invalidPostions = [] #temporal

    for pos in possibleMoves:
      cellmates = self.model.grid.get_cell_list_contents([pos]) #Obtener el contenido de la cleda
      # print(f"-------- CELLMATES TIENE:{cellmates}")
      for agent in cellmates:
        if isinstance(agent, CarAgent): #Buscar agentes carro
          invalidPostions.append(pos)
        if isinstance(agent, SemaforoAgent):
          if not agent.colorState: #Buscar agentes semaforo rojo
            invalidPostions.append(pos)

    #Eliminamos las posiciones invalidas
    for pos in invalidPostions: #Recorrer posiciones invalidas
      if pos in possibleMoves: #Remover posiciones invalidad
        possibleMoves.remove(pos)



    #select next move
    if len(possibleMoves) > 0:
      min_moves=[]
      min_moves.append(possibleMoves[0])
      print(min_moves)
      min_distance=abs(self.destinationStreet[0]-min_moves[0][0])+abs(self.destinationStreet[1]-min_moves[0][1])

      for i in possibleMoves:
        distance=abs(self.destinationStreet[0]-i[0])+abs(self.destinationStreet[1]-i[1])
        if distance<min_distance:
          min_moves.append(i)
          min_distance=distance
      for m in min_moves:
        distance=abs(self.destinationStreet[0]-m[0])+abs(self.destinationStreet[1]-m[1])
        if distance>min_distance:
          min_moves.remove(m)

      min_move=min_moves[self.random.randrange(len(min_moves))]

      #move agent
      self.model.grid.move_agent(self, min_move)

  def isDestination(self):
    neighbours=self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
    for n in neighbours:
      #print(n)
      if self.model.grid.properties["Estacionamiento"].data[n]==self.destination:
        self.model.grid.move_agent(self,n)
        self.isParked = True
        print(f"carro {self.unique_id} estacionado")
        self.model.parked+=1
    return self.isParked

  def lookingPark(self):
    if self.isMoving:
      self.move()
    else:
      self.isMoving = False
      self.isParked = True
      pass

  def carHi(self):
    print(f"Carro #{self.unique_id} | Posición: {self.pos}")

  def checkSemaforo(self):
    neighbors = self.model.grid.get_neighbors(self.pos, moore=False, include_center=True) #Se incluye el centro porque el carro puede estar "abajo" del semaforo

    for agent in neighbors:
      if isinstance(agent, SemaforoAgent):
        return agent.colorState #Refresamos si el semaforo esta

    return True #Decimos que el semaforo esta en verde para que siga avanzando


  def checkAnnotherCarr(self):
    neighbors  =self.model.grid.get_neighbors(self.pos, moore=False, include_center=False)
    if isinstance(agent, CarAgent):
      print(f"Carro #{self.unique_id} en: {self.pos} ve el carro #{agent.unique_id} en {agent.pos}")
      return True #Avisa que tenemos un carro cerca
    return False #Avisa que el camino esta despejado