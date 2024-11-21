from flask import Flask, jsonify
from model import CityModel
from agent_car import CarAgent
from agent_sempahore import SemaforoAgent

m=CityModel(1)
app=Flask(__name__)

@app.route("/try")
def trying():
    return("try succesfull")

@app.route("/getCarsInitial")
def getCarsInitial():
    pos=[]
    for cars in m.agents:
        if isinstance(cars, CarAgent):
            pos.append({"x":cars.pos[0],"z":cars.pos[1]})
    return jsonify({"InitialPositions":pos})
    
@app.route("/getSemaphores")
def getSemaphores():
    colors=[]
    for s in m.agents:
        if isinstance(s,SemaforoAgent):
            colors.append({"color":s.colorState})
    return jsonify({"SemaphoresStates":colors})

@app.route("/getCarsPositions")
def getCarsPositions():
    m.step()
    pos=[]
    for cars in m.agents:
        if isinstance(cars, CarAgent):
            pos.append({"x":cars.pos[0],"z":cars.pos[1]})
    return jsonify({"CarsPositions":pos})


if __name__=="__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)