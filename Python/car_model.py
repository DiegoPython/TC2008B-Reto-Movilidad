import mesa
import numpy as np

def get_model_grid(model):
    grid = np.zeros((model.grid.width, model.grid.height))

    for cell in model.grid.coord_iter():
        cell_content, x, y = cell

        if isinstance(cell_content, CarAgent):
            grid[x][y] = 0
        elif isinstance(cell_content, TrafficLight):
            if cell_content.state == cell_content.GREEN:
                grid[x][y] = 2
            elif cell_content.state == cell_content.YELLOW:
                grid[x][y] = 5
            else:
                grid[x][y] = 0
        else:
            grid[x][y] = 8

    return grid

class CarAgent(mesa.Agent):
    #Puntos de incio de los carros
    NORTH = 0
    SOUTH = 2
    EAST = 1
    WEST = 3
    
    def __init__(self, unique_id, model, origin):
        super().__init__(unique_id, model)
        self.origin = origin
        self.moves = 0
        self.new_pos = None
        self.remove_flag = False
        self.traffic_light_pos = self.model.traffic_light_positions[self.origin]
        self.traffic_light = self.model.grid[self.traffic_light_pos[0]][self.traffic_light_pos[1]]

    def step(self):
        self.new_pos = None
        #Obtenemos la siguiente posicion del agente
        self.move()

    #Funcion para determinar la siguiente posicion del agente
    def move(self):
        next_x = self.pos[0]
        next_y = self.pos[1]

        if self.origin == self.NORTH:
            next_x += 1
        elif self.origin == self.SOUTH:
            next_x -= 1
        elif self.origin == self.EAST:
            next_y -= 1
        else:
            next_y += 1

        if self.model.grid.out_of_bounds((next_x, next_y)):
            self.remove_flag = True
        elif self.model.grid.is_cell_empty((next_x, next_y)) and self.check_traffic_light():
            self.new_pos = (next_x, next_y)

    #Funcion para detectar el estado del semaforo
    def check_traffic_light(self):
        #Si el agente ya ha pasado el semaforo
        if not self.is_behind_light():
            return True

        #Si el semaforo no esta en verde, y el agente esta al lado de el
        if self.traffic_light.state != TrafficLight.GREEN and self.is_next_light():
            return False

        #Si el semaforo es verde o no estamos al lado de el
        return True

    #Funcion para saber si el agente se encuentra al lado de un semaforo
    def is_next_light(self):
        if (self.origin == self.NORTH or self.origin == self.SOUTH) and self.pos[0] == self.traffic_light_pos[0]:
            return True
        elif (self.origin == self.EAST or self.origin == self.WEST) and self.pos[1] == self.traffic_light_pos[1]:
            return True

        return False

    #Funicion para saber si el agente se encuentra detras del semaforo
    def is_behind_light(self):
        if self.origin == self.NORTH and self.pos[0] <= self.traffic_light_pos[0]:
            return True
        elif self.origin == self.SOUTH and self.pos[0] >= self.traffic_light_pos[0]:
            return True
        elif self.origin == self.EAST and self.pos[1] >= self.traffic_light_pos[0]:
            return True
        elif self.pos[1] <= self.traffic_light_pos[1]:
            return True

        return False

    #Funcion para eliminar un agente del modelo
    def remove(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
        self.model.num_cars -= 1
    
    #Actualizamos los datos del agente
    def advance(self):
        if self.new_pos == None:
            self.new_pos = self.pos
        elif self.pos != self.new_pos:
            self.moves += 1

        if not self.remove_flag:
            self.model.grid.move_agent(self, self.new_pos)

class TrafficLight(mesa.Agent):
    #Ubicaciones del semaforo
    NORTH = 0
    SOUTH = 2
    EAST = 1
    WEST = 3
    #Estados del semaforo
    GREEN = 3
    YELLOW = 2
    RED = 1

    def __init__(self, unique_id, pos, model, location, state=GREEN):
        super().__init__(pos, model)
        self.unique_id = unique_id
        self.pos = pos
        self.location = location
        self.state = state
        self.new_state = 0
        self.cars_detected = 0

    def step(self):
        self.cars_detected = self.count_cars()

        if self.cars_detected == 0:
            self.new_state = self.YELLOW

    #Funcion para cambiar el estado de un semaforo dependiendo de su posicion
    def change_state(self, horizontal, vertical):
        #Si el semaforo se encuentra en el eje vertical
        if self.location % 2 == 0:
            self.new_state = vertical
        #Si el semaforo se encuentra en el eje horizontal
        else:
            self.new_state = horizontal

    #Funcion para verificar si hay un auto al lado del semaforo
    def is_car_next(self):
        if self.location == self.NORTH and not self.model.grid.is_cell_empty(self.pos[0] + 1, self.pos[1]):
            return True
        
        if self.location == self.SOUTH and not self.model.grid.is_cell_empty(self.pos[0], self.pos[1] + 1):
            return True

        if self.location == self.EAST and not self.model.grid.is_cell_empty(self.pos[0] - 1, self.pos[1]):
            return True

        if self.location == self.WEST and not self.model.grid.is_cell_empty(self.pos[0] + 1, self.pos[1]):
            return True

        return False

    #Funcion auxiliar para contar los carros en la calle asignada al semaforo
    def count_cars(self):
        count = 0
        if self.location == self.NORTH:
            for i in range(self.pos[0] + 1):
                if not self.model.grid.is_cell_empty((i, self.pos[1] - 1)):
                    count += 1
        elif self.location == self.SOUTH:
            for i in range(self.pos[0], self.model.grid.width):
                if not self.model.grid.is_cell_empty((i, self.pos[1] + 1)):
                    count += 1
        elif self.location == self.EAST:
            for i in range(self.pos[1], self.model.grid.height):
                if not self.model.grid.is_cell_empty((self.pos[0] - 1, i)):
                    count += 1
        else:
            for i in range(self.pos[1] + 1):
                if not self.model.grid.is_cell_empty((self.pos[0] + 1, i)):
                    count += 1

        return count

    #Actualizamos los datos del agente
    def advance(self):
        if self.new_state == 0:
            self.new_state = self.state
        
        self.state = self.new_state

class TrafficModel(mesa.Model):
    def __init__(self, N):
        self.max_cars = N + 1
        self.num_cars = N
        self.num_agents = N + 4 #Agregamos los semaforos a nuestro total de agentes
        width = 8
        height = 8
        self.grid = mesa.space.SingleGrid(width, height, False)
        self.schedule = mesa.time.SimultaneousActivation(self)

        #Posiciones predefinidas para los semaforos y carros
        self.traffic_light_positions = ((2, 5), (5, 5), (5, 2), (2, 2))
        self.car_origins = ((0, 4), (4, 7), (7, 3), (3, 0))

        #Variables para guardar los estados de los semaforos
        self.horizontal_state = 0
        self.vertical_state = 0
        self.new_horizontal_state = 0
        self.new_vertical_state = 0

        #Bandera para el cambio de semaforo
        self.random_light_flag = False
        self.change_state_flag = False

        #Posicionar semaforos
        for i in range(len(self.traffic_light_positions)):
            traffic_light_pos = self.traffic_light_positions[i]
            traffic_light = TrafficLight(i, traffic_light_pos, self, i, TrafficLight.YELLOW)
            self.grid.place_agent(traffic_light, traffic_light_pos)
            self.schedule.add(traffic_light)

        #Posicionar autos
        for i in range(self.num_cars):
            car_origin_index = i % len(self.car_origins)

            if self.grid.is_cell_empty(self.car_origins[car_origin_index]):
                car_agent = CarAgent(i + 4, self, car_origin_index)
                self.grid.place_agent(car_agent, self.car_origins[car_origin_index])
                self.schedule.add(car_agent)

        #DataCollector
        self.datacollector = mesa.DataCollector(
            model_reporters={'Grid': get_model_grid}
        )

        self.datacollector.collect(self)

    def step(self):
        #if self.num_cars < self.max_cars:
        #    self.add_car()
        self.check_intersection()
        self.schedule.step()
        self.remove_agents()
        self.datacollector.collect(self)

    #Funcion para controlar los estados de los semaforos dependiendo
    #del numero de autos en la interseccion
    def check_intersection(self):
        #Variables para el conteo de cada calle
        horizontal_count = 0
        vertical_count = 0

        #Lista para guardar y manipular facilmente los semaforos
        lights = []

        #Realizamos el conteo de carros en cada calle
        for i in range(4):
            #Obtenemos el semaforo
            light_pos = self.traffic_light_positions[i]
            light = self.grid[light_pos[0]][light_pos[1]]
            #Obtenemos el conteo de carros
            light_count = light.count_cars()

            #Agregamos el semaforo a la lista
            lights.append(light)

            #Realizamos el conteo de acuerdo a la posision del semaforo
            if i % 2 == 0:
                vertical_count += light_count
            else:
                horizontal_count += light_count

        #Si en ambos "ejes" hay la misma cantidad de autos, elegimos uno al azar
        if horizontal_count == vertical_count and not self.random_light_flag:
            green = self.random.randint(0, 1)

            #Actualizamos los estados de las banderas
            self.random_light_flag = True

            #Damos paso a los autos en el eje horizontal
            if green == 1:
                self.new_horizontal_state = TrafficLight.GREEN
                self.new_vertical_state = TrafficLight.RED
            #Damos paso a los autos en el eje vertical
            else:
                self.new_horizontal_state = TrafficLight.RED
                self.new_vertical_state = TrafficLight.GREEN
        #Si hay mas autos en el eje horizontal que en el vertical
        elif horizontal_count > vertical_count:
            self.new_horizontal_state = TrafficLight.GREEN
            self.new_vertical_state = TrafficLight.RED

            #Actualizamos los estados de las banderas
            self.random_light_flag = False
        #Si hay mas autos en el eje vertical que en el horizontal
        else:
            self.new_horizontal_state = TrafficLight.RED
            self.new_vertical_state = TrafficLight.GREEN
            
            #Actualizamos los estados de las banderas
            self.random_light_flag = False

        if self.horizontal_state == 0:
            self.horizontal_state = self.new_horizontal_state
            self.vertical_state = self.new_vertical_state
        elif self.horizontal_state != self.new_horizontal_state and not self.change_state_flag:
            self.random_light_flag = False
            self.change_state_flag = True

        #Actualizamos los estados de los semaforos
        for light in lights:
            light.change_state(self.horizontal_state, self.vertical_state)

    #Funcion para agregar un auto en una posicion inicial aleatoria
    def add_car(self):
        random_origin = self.random.randint(0, 3)

        if self.grid.is_cell_empty(self.car_origins[random_origin]):
            self.num_cars += 1
            self.num_agents += 1
            car_agent = CarAgent(self.num_agents, self, random_origin)
            self.grid.place_agent(car_agent, self.car_origins[random_origin])
            self.schedule.add(car_agent)

    def remove_agents(self):
        for agent in self.schedule.agents:
            if isinstance(agent, CarAgent) and agent.remove_flag == True:
                agent.remove()

    def is_intersection_clear(self):
        for i in range(self.traffic_light_positions[3][1] + 1, self.traffic_light_positions[0][1]):
            for j in range(self.traffic_light_positions[3][0] + 1, self.traffic_light_positions[2][0]):
                if not self.grid.is_cell_empty((j, i)):
                    return False

        return True
