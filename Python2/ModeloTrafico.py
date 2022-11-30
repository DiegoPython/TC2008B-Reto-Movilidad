
from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import RandomActivation
import random


class AgenteVehiculo(Agent):
    '''
    Agente que simula el comportamiento
    de un vehículo
    '''

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.tipo = random.choice([1, 2, 3])
        self.direccion = 0    # 0 - derecho, 1 - derecha
        self.frente = 0      # 0 - arriba, 1 - derecha, 2 - abajo, 3 - izquierda

    def move(self):

        if self.frente == 0:
            newY = self.pos[1] + 1
            #celdaEnfrente = (self.pos[0], self.pos[1]+1)
            if newY >= self.model.grid.height:
                coords = [(25, 0), (27, 0)]
                celdaEnfrente = random.choice(coords)
                celdaEnfrente2 = (celdaEnfrente[0], celdaEnfrente[1]+1)
            else:
                celdaEnfrente = (self.pos[0], newY)
                if celdaEnfrente[1]+1 >= self.model.grid.height:
                    celdaEnfrente2 = (self.pos[0], 0)
                else:
                    celdaEnfrente2 = (celdaEnfrente[0], newY+1)
            celdaDerecha = (self.pos[0]+1, self.pos[1])
            celdaIzquierda = (self.pos[0]-1, self.pos[1])
        elif self.frente == 1:
            newX = self.pos[0] + 1
            if newX >= self.model.grid.width:
                coords = [(0, 28), (0, 30)]
                celdaEnfrente = random.choice(coords)
                celdaEnfrente2 = (celdaEnfrente[0]+1, celdaEnfrente[1])
            else:
                celdaEnfrente = (newX, self.pos[1])
                if celdaEnfrente[0]+1 >= self.model.grid.width:
                    celdaEnfrente2 = (0, celdaEnfrente[1])
                else:
                    celdaEnfrente2 = (newX+1, celdaEnfrente[1])
            #celdaEnfrente = (self.pos[0]+1, self.pos[1])
            celdaDerecha = (self.pos[0], self.pos[1]-1)
            celdaIzquierda = (self.pos[0], self.pos[1]+1)
        elif self.frente == 2:
            newY = self.pos[1] - 1
            if newY <= 0:
                celdaEnfrente = (self.pos[0], self.model.grid.height)
            else:
                celdaEnfrente = (self.pos[0], newY)
            celdaDerecha = (self.pos[0]-1, self.pos[1])
            celdaIzquierda = (self.pos[0]+1, self.pos[1])
        elif self.frente == 3:
            newX = self.pos[0] - 1
            if newX <= 0:
                celdaEnfrente = (self.model.grid.width, self.pos[1])
            else:
                celdaEnfrente = (newX, self.pos[1])
            celdaDerecha = (self.pos[0], self.pos[1]+1)
            celdaIzquierda = (self.pos[0], self.pos[1]-1)

        # if self.model.grid.is_cell_empty(celdaEnfrente):
        #    self.model.grid.move_agent(self, celdaEnfrente)

        if self.pos == (25, 22) or self.pos == (27, 22):
            if self.model.grid[23][32].color == 2 or self.model.grid[23][32].color == 3:
                return

        elif self.pos == (20, 28) or self.pos == (20, 30):
            if self.model.grid[29][26].color == 2 or self.model.grid[29][26].color == 3:
                return

        if self.model.grid.is_cell_empty(celdaEnfrente2):
            if self.pos == (27, 28) or self.pos == (25, 30):
                # 0 - derecho, 1 ó 2 - derecha ó izquierda
                proxMov = random.choice([0, 1, 2])
                if proxMov == 0 and self.model.grid.is_cell_empty(celdaEnfrente):
                    self.model.grid.move_agent(self, celdaEnfrente)

                else:
                    if self.frente == 0 and self.pos == (27, 28) and self.model.grid.is_cell_empty(celdaDerecha):
                        self.frente = 1
                        self.model.grid.move_agent(self, celdaDerecha)
                        # Hacer que el frente del coche gire cuando se gira hacia la derecha

                    elif self.frente == 1 and self.pos == (25, 30) and self.model.grid.is_cell_empty(celdaIzquierda):
                        self.frente = 0
                        self.model.grid.move_agent(self, celdaIzquierda)

            elif self.model.grid.is_cell_empty(celdaEnfrente):
                self.model.grid.move_agent(self, celdaEnfrente)

            else:
                return

        else:
            return

    def step(self):
        self.move()


class AgenteSemaforo(Agent):
    '''
    Agente que simula el comportamiento de los
    semáforos
    '''

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # 1 - verde, 2 - amarillo, 3 - rojo
        self.color = 3
        self.pasos = 0
        self.verde = 0
        self.anterior = False

    def step(self):
        self.pasos += 1
        semaforo1 = 0
        semaforo2 = 0
        for i in range(12, 25):
            if not self.model.grid.is_cell_empty((i, 28)):
                semaforo1 += 1
            if not self.model.grid.is_cell_empty((i, 30)):
                semaforo1 += 1

        for i in range(14, 28):
            if not self.model.grid.is_cell_empty((25, i)):
                semaforo2 += 1
            if not self.model.grid.is_cell_empty((27, i)):
                semaforo2 += 1

        if self.model.grid[23][32].color == 1 and self.verde >= 2 and semaforo1 != 0:
            self.model.grid[23][32].pasos = 22
            self.model.grid[23][32].verde = 0

        if self.model.grid[29][26].color == 1 and self.verde == 2 and semaforo2 != 0:
            self.model.grid[29][26].pasos = 22
            self.model.grid[29][26].verde = 0

        if self.model.grid[23][32].color == 1 and self.model.grid[29][26].color == 3 and semaforo2 == 0 and (self.model.grid[23][32].pasos == 5 or self.model.grid[29][26].pasos == 5):
            self.model.grid[29][26].color = 3
            self.model.grid[29][26].pasos = 0
            self.model.grid[23][32].color = 3
            self.model.grid[23][32].pasos = 0

        elif self.model.grid[23][32].color == 3 and self.model.grid[29][26].color == 1 and semaforo1 == 0 and (self.model.grid[23][32].pasos == 5 or self.model.grid[29][26].pasos == 5):
            self.model.grid[29][26].color = 3
            self.model.grid[29][26].pasos = 0
            self.model.grid[23][32].color = 3
            self.model.grid[23][32].pasos = 0

        if self.model.grid[29][26].color == 3 and self.model.grid[23][32].color == 3 and self.pasos == 5:
            if semaforo1 >= semaforo2:
                self.model.grid[29][26].color = 1
                if self.model.grid[29][26].anterior:
                    self.model.grid[29][26].verde += 1
                self.model.grid[29][26].anterior = True
                self.model.grid[23][32].anterior = False
            else:
                self.model.grid[23][32].color = 1
                if self.model.grid[23][32].anterior:
                    self.model.grid[23][32].verde += 1
                self.model.grid[23][32].anterior = True
                self.model.grid[29][26].anterior = False
            return

        elif self.pasos > 5 and self.model.grid[29][26].color == 3 and self.model.grid[23][32].color == 3:
            self.pasos = 0

        elif self.model.grid[29][26].color == 1 and self.pasos == 22:
            self.model.grid[29][26].color = 2

        elif self.model.grid[23][32].color == 1 and self.pasos == 22:
            self.model.grid[23][32].color = 2

        elif self.model.grid[29][26].color == 2 and self.pasos == 32:
            self.model.grid[29][26].color = 3
            self.pasos = 0

        elif self.model.grid[23][32].color == 2 and self.pasos == 32:
            self.model.grid[23][32].color = 3
            self.pasos = 0



class AgenteSemaforoConvencional(Agent):
    '''
    Agente que simula el comportamiento de un semáforo convencional
    '''

    def __init__(self, unique_id, model, j):
        super().__init__(unique_id, model)
        if j == 0:
            self.color = 3
            self.pasos = 0
        else:
            self.color = 1
            self.pasos = 200

    def step(self):
        self.pasos += 1

        if self.pasos == 200 and self.color == 3:
            self.color = 1

        elif self.pasos == 340 and self.color == 1:
            self.color = 2

        elif self.pasos == 400 and self.color == 2:
            self.color = 3
            self.pasos = 0


class AgenteBanqueta(Agent):
    '''
    En realidad no es un agente pero nos
    ayuda a simular la existencia de banquetas
    en la simulación
    '''

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class TraficModel(Model):
    '''
    Modelo para la simulación de tránsito
    '''

    # tipo 1 = semáforos convencionales, tipo 2 = nuestros semáforos
    def __init__(self, N, tipo, width, height):
        self.num_agents = N
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Crear banquetas
        numBanq = (width*2 - 2) + (height*2 - 2)
        listaCoords = []

        for i in range(int(width/2 - 2)):
            x = i
            y = int(height/2)
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(height/2)):
            x = int(width/2 - 3)
            y = i
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(width/2 + 1), width):
            x = i
            y = int(height/2)
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(height/2)):
            x = int(width/2 + 1)
            y = i
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(width/2 - 2)):
            x = i
            y = int(height/2 + 4)
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(height/2 + 5), height):
            x = int(width/2 - 3)
            y = i
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(width/2 + 1), width):
            x = i
            y = int(height/2 + 4)
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(height/2 + 5), height):
            x = int(width/2 + 1)
            y = i
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(len(listaCoords)):
            a = AgenteBanqueta(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, listaCoords[i])

        # Añadir los vehículos a las celdas
        j = 0
        for i in range(numBanq, numBanq + self.num_agents):
            positions = [(25, 0), (27, 0), (0, 30), (0, 28),
                         (25, 2), (27, 2), (2, 30), (2, 28),
                         (25, 4), (27, 4), (4, 30), (4, 28),
                         (6, 30), (6, 28)]

            a = AgenteVehiculo(i, self)

            if positions[j][0] < positions[j][1]:
                a.frente = 1
            self.schedule.add(a)
            x = positions[j][0]
            y = positions[j][1]
            self.grid.place_agent(a, (x, y))
            j += 1

        # Añadir semáforos
        if tipo == 2:
            j = 0
            for i in range(numBanq + self.num_agents, numBanq + self.num_agents + 2):
                posSemaforos = [(23, 32), (29, 26)]
                a = AgenteSemaforo(i, self)
                self.schedule.add(a)
                x = posSemaforos[j][0]
                y = posSemaforos[j][1]
                self.grid.place_agent(a, (x, y))
                j += 1

        else:
            j = 0
            for i in range(numBanq + self.num_agents, numBanq + self.num_agents + 2):
                posSemaforos = [(23, 32), (29, 26)]
                a = AgenteSemaforoConvencional(i, self, j)
                self.schedule.add(a)
                x = posSemaforos[j][0]
                y = posSemaforos[j][1]
                self.grid.place_agent(a, (x, y))
                j += 1

    def getColors(self):
        '''
        Obtener los colores de los semáforos
        '''
        agents = self.schedule.agents
        colors = []

        for a in agents:
            if isinstance(a, AgenteSemaforo):
                colors.append(a.color)

        return colors

    def getFront(self):
        '''
        Obtener la dirección de los vehículos
        '''
        agents = self.schedule.agents
        directions = []

        for a in agents:
            if isinstance(a, AgenteVehiculo):
                directions.append(a.frente)

        return directions

    def step(self):
        '''
        Avanzar el modelo un paso
        '''
        self.schedule.step()

        agents = self.schedule.agents
        ps = []
        colors = []

        for a in agents:
            if isinstance(a, AgenteVehiculo):
                xy = a.pos
                p = [xy[0], xy[1], -1.67]
                ps.append(p)

        return ps
