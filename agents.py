import mesa

class CarAgent(mesa.Agent):

  def __init__(self, model,destination):
    super().__init__(model)
    self.isParked = False
    self.isMoving = True
    self.destination = destination
    self.prevMoves=[]
    self.forbidenMoves=[]

    #defines the position of the assigned parking spot
    posDestination=self.model.grid.properties["Estacionamiento"].select_cells(lambda x: x == self.destination)
    #defines the position of the street in front of the assigned parking spot
    posDestinationAround=[(posDestination[0][0]+1,posDestination[0][1]),(posDestination[0][0]-1,posDestination[0][1]),(posDestination[0][0],posDestination[0][1]+1),(posDestination[0][0],posDestination[0][1]-1)]
    for p in posDestinationAround:
      if self.model.grid.properties["Left"].data[p]==1 or self.model.grid.properties["Right"].data[p]==1 or self.model.grid.properties["Up"].data[p]==1 or self.model.grid.properties["Down"].data[p]==1:
        self.destinationStreet=p

    #defines forbbiden moves in order to optimize travel routes and avoid cicles
    if self.destination==15 or self.destination==16:
      self.forbidenMoves=[(12,22),(13,22),(11,14),(11,15),(11,6),(11,7)]
    elif self.destination==8:
      self.forbidenMoves=[(14,2),(15,2),(18,8),(19,8)]
    elif self.destination==12:
      self.forbidenMoves=[(14,15),(11,14),(11,15),(6,21),(7,21),(12,22),(13,22),(11,6),(11,7)]
    elif self.destination==13:
      self.forbidenMoves=[(14,2),(15,2),(21,14),(21,15),(15,14)]
    elif self.destination==17 or self.destination==14:
      self.forbidenMoves=[(21,14),(21,15),(15,14)]
    elif self.destination==5:
      self.forbidenMoves=[(16,0),(16,1)]
    elif self.destination==9:
      self.forbidenMoves=[(0,11),(1,11),(11,6),(11,7),(12,11),(13,11)]
    elif self.destination==6 or self.destination==7:
      self.forbidenMoves=[(0,11),(1,11),(5,11),(6,11),(11,14),(11,15)]
    elif self.destination==2:
      self.forbidenMoves=[(12,11),(13,11)]
    elif self.destination==4 or self.destination==10:
      self.forbidenMoves=[(0,11),(1,11),(5,11),(6,11)]
    elif self.destination==1:
      self.forbidenMoves=[(2,12),(2,13),(12,11),(13,11)]
    elif self.destination==3:
      self.forbidenMoves=[(16,0),(16,1),(16,12),(16,13)]

  #comunicates with semaphore
  def sayDistance(self):
    found=False
    neigh=[]
    searchpos=[self.pos[0],self.pos[1]]
    distance=100
    if self.model.grid.properties["Left"].data[self.pos] == 1 :
      while searchpos[1]>0 and found==False:
        #print(searchpos)
        neigh=self.model.grid.get_neighbors((searchpos[0],searchpos[1]), moore=False, include_center=True,radius=0)
        if len(neigh)>0:
          for i in neigh:
            if isinstance(i, SemaforoAgent):
              found=True
              if i.distanceNearestCar!=None:
                distance=i.distanceNearestCar
              if abs(self.pos[1]-searchpos[1])<distance:
                i.changeDistanceNearestCar(abs(self.pos[1]-searchpos[1]))
                i.hasReveived=True
        searchpos[1]-=1

    if self.model.grid.properties["Right"].data[self.pos] == 1 :
      searchpos=[self.pos[0],self.pos[1]]
      while searchpos[1]<self.model.width and found==False:
        #print(searchpos)
        neigh=self.model.grid.get_neighbors((searchpos[0],searchpos[1]), moore=False, include_center=True,radius=0)
        if len(neigh)>0:
          for i in neigh:
            if isinstance(i, SemaforoAgent):
              found=True
              if i.distanceNearestCar!=None:
                distance=i.distanceNearestCar
              if abs(searchpos[1]-self.pos[1])<distance:
                i.changeDistanceNearestCar(abs(searchpos[1]-self.pos[1]))
                i.hasReveived=True
        searchpos[1]+=1

    if self.model.grid.properties["Up"].data[self.pos] == 1 :
      searchpos=[self.pos[0],self.pos[1]]
      while searchpos[0]>0 and found==False:
        #print(searchpos)
        neigh=self.model.grid.get_neighbors((searchpos[0],searchpos[1]), moore=False, include_center=True,radius=0)
        if len(neigh)>0:
          for i in neigh:
            if isinstance(i, SemaforoAgent):
              found=True
              if i.distanceNearestCar!=None:
                distance=i.distanceNearestCar
              if abs(self.pos[0]-searchpos[0])<distance:
                i.changeDistanceNearestCar(abs(self.pos[0]-searchpos[0]))
                i.hasReveived=True
        searchpos[0]-=1

    if self.model.grid.properties["Down"].data[self.pos] == 1 :
      searchpos=[self.pos[0],self.pos[1]]
      while searchpos[0]<self.model.height and found==False:
        #print(searchpos)
        neigh=self.model.grid.get_neighbors((searchpos[0],searchpos[1]), moore=False, include_center=True,radius=0)
        if len(neigh)>0:
          for i in neigh:
            if isinstance(i, SemaforoAgent):
              found=True
              if i.distanceNearestCar!=None:
                distance=i.distanceNearestCar
              if abs(searchpos[0]-self.pos[0])<distance:
                i.changeDistanceNearestCar(abs(searchpos[0]-self.pos[0]))
                i.hasReveived=True
        searchpos[0]+=1

  def move(self):
    possibleMoves=[]

    #select posible movements
    #checks the direction of it's position
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

    for f in self.forbidenMoves:
      if f in possibleMoves:
        possibleMoves.remove(f)

    for pos in possibleMoves:
      cellmates = self.model.grid.get_cell_list_contents([pos]) #Obtener el contenido de la cleda
      for agent in cellmates:
        if isinstance(agent, CarAgent): #Buscar agentes carro
          invalidPostions.append(pos)
        if isinstance(agent, SemaforoAgent):
          if agent.complexColorState == -1: #Buscar agentes semaforo rojo
            invalidPostions.append(pos)

    #Eliminamos las posiciones invalidas
    for pos in invalidPostions: #Recorrer posiciones invalidas
      if pos in possibleMoves: #Remover posiciones invalidad
        possibleMoves.remove(pos)

    #checks that the agent isn't repeating incorrect behaviour
    shouldAdd=False

    if len(possibleMoves) > 2:
      #marks that the actual position is a desicion point for the agent
      shouldAdd=True
      for i in possibleMoves:
        if i in self.prevMoves and len(possibleMoves)>1:
          possibleMoves.remove(i)

    #select next move
    if len(possibleMoves) > 0:
      min_moves=[]
      min_moves.append(possibleMoves[0])
      min_distance=abs(self.destinationStreet[0]-min_moves[0][0])+abs(self.destinationStreet[1]-min_moves[0][1])

      #defines which move will get the agent closer to it's destination
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

      #ads the desicion to it's history
      if(shouldAdd):
        if(len(self.prevMoves)>20):
          self.prevMoves.remove(self.prevMoves[0])
        self.prevMoves.append(min_move)

      #move agent
      self.model.grid.move_agent(self, min_move)

  def isDestination(self):
    #checks if it's found its parking spot
    neighbours=self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
    for n in neighbours:
      if self.model.grid.properties["Estacionamiento"].data[n]==self.destination:
        self.model.grid.move_agent(self,n)
        self.isParked = True
        self.model.parked+=1
    return self.isParked

  def checkSemaforo(self):
    neighbors = self.model.grid.get_neighbors(self.pos, moore=False, include_center=True) #Se incluye el centro porque el carro puede estar "abajo" del semaforo

    for agent in neighbors:
      if isinstance(agent, SemaforoAgent):
        return agent.colorState #Refresamos si el semaforo esta

    return True #Decimos que el semaforo esta en verde para que siga avanzando

class SemaforoAgent(mesa.Agent):
  def __init__(self, model, colorBool, complexColor, verHor):
    super().__init__(model)
    self.colorState = colorBool #True -> Verde | False -> Rojo
    self.distanceNearestCar=None #Esta distancia debe ser modificada por el carro
    self.parejaDistance = None #Distancia que ambos comparten
    self.complexColorState = complexColor # -1 -> Rojo  0 -> Amarillo   1 -> Verde
    self.semType = verHor #Horizontal o vertical
    self.hasReveived=False

  def changeDistanceNearestCar(self,distance):
    self.distanceNearestCar=distance


  def changeColor(self):
    Sem_neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False) #Identificar los semaforos alrededor
    for semV in Sem_neighbors:
      if isinstance(semV, SemaforoAgent):
        if semV.semType != self.semType: #Revisamos pareja contraria
          #print(f"sem {self.pos} encontro pareja contraria: {semV.pos}")
          #comparamos las distnacias entre semaforos
          if self.parejaDistance == None and semV.parejaDistance == None:
            self.complexColorState = 0 #Amarillo
          #Comparamos la distancia del vecino
          elif semV.parejaDistance != None and self.parejaDistance != None:
            if self.parejaDistance < semV.parejaDistance:
              self.complexColorState = 1 #Verde
              semV.complexColorState = -1
            elif self.parejaDistance > semV.parejaDistance:
              self.complexColorState = -1 #Rojo
              semV.complexColorState = 1
          elif self.parejaDistance == None and semV.parejaDistance != None:
            self.complexColorState = -1
            semV.complexColorState = 1
          elif self.parejaDistance != None and semV.parejaDistance == None:
            self.complexColorState = 1
            semV.complexColorState = -1
          self.cambiaPareja(semV.pos)

      self.cambiaPareja(self.pos)

  def reset(self):
    self.hasReveived=False

  def cambiaPareja(self, posSemaforo):
    mainSemafore=self.model.grid.get_neighbors(posSemaforo, moore=True, include_center=True, radius=0)[0]
    Sem_neighbors = self.model.grid.get_neighbors(posSemaforo, moore=True, include_center=False)
    for semV in Sem_neighbors:
        if isinstance(semV, SemaforoAgent):
          if semV.semType == mainSemafore.semType:
            semV.complexColorState = mainSemafore.complexColorState

  #Función dedicaada en revisar las distancias y asignar la distanciaPareja
  def revisarDistancia(self):
    #Comparar distancia con semaforos de alrededor
    Sem_neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True) #Identificar los semaforos alrededor
    for semV in Sem_neighbors:
      if isinstance(semV, SemaforoAgent): #Revisamos que sean semaforos los agentes de alrededor
        if semV.semType == self.semType: #En caso de ser su pareja revisar su distancia
          if self.hasReveived==True or semV.hasReveived==True:
            self.hasReveived=semV.hasReveived=True
          else:
            self.distanceNearestCar=semV.distanceNearestCar=None
          if self.distanceNearestCar != None and semV.distanceNearestCar != None:
            if self.distanceNearestCar > semV.distanceNearestCar:
              #CAmbiamos la distancia pareja de ambos
              self.parejaDistance = self.distanceNearestCar
              semV.parejaDistance = self.distanceNearestCar
            else:
              self.parejaDistance = semV.distanceNearestCar
              semV.parejaDistance = semV.distanceNearestCar
          elif self.distanceNearestCar != None and semV.distanceNearestCar == None:
            self.parejaDistance = self.distanceNearestCar
            semV.parejaDistance = self.distanceNearestCar
          elif self.distanceNearestCar == None and semV.distanceNearestCar == None:
            self.parejaDistance = None #Resetear distancia pareja de ambos
            semV.parejaDistance = None

    under_Sem = self.model.grid.get_neighbors(self.pos, moore = False, include_center = True, radius = 0)
    for car in under_Sem:
      if isinstance(car, CarAgent):
        print("Hay un carro abajo de mi")
        self.distanceNearestCar = None #Resetear mi distancia