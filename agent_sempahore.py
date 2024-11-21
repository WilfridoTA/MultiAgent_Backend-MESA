import mesa

class SemaforoAgent(mesa.Agent):
  def __init__(self, model, colorBool):
    super().__init__(model)
    self.colorState = colorBool #True -> Verde | False -> Rojo
    self.stepCounter = 0
    self.time = 0

  def changeColor(self):
    self.time += 1/4

    if self.time >= 10:
      self.time = 0 #Reiniciamos el contador
      self.colorState = not self.colorState #Invertimos el color
      print(f"Semaforo {self.unique_id} cambión de color")
      self.say_hi()


  def say_hi(self):
    if self.colorState:
      print(f"Semaforo: {self.unique_id} | Color: VERDE | Posicion {self.pos}")
    else:
      print(f"Semaforo: {self.unique_id} | Color: ROJO | Posicion {self.pos}")