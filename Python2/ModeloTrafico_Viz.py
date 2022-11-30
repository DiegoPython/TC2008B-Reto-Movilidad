from ModeloTrafico import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portayal = {'Shape': 'rect',
                'Filled': 'true',
                'Layer': 0,
                'Color': 'red',
                'w': 1,
                'h': 1}

    if (isinstance(agent, AgenteBanqueta)):
        portayal['Color'] = 'grey'

    elif (isinstance(agent, AgenteSemaforo) or isinstance(agent, AgenteSemaforoConvencional)):
        if agent.color == 1:
            portayal['Color'] = 'green'
        elif agent.color == 3:
            portayal['Color'] = 'red'
        else:
            portayal['Color'] = 'yellow'
    return portayal


grid = CanvasGrid(agent_portrayal, 55, 55, 500, 500)
server = ModularServer(TraficModel,
                       [grid],
                       'Modelo de tráfico',
                       {'N': 14, 'tipo': 2, 'width': 55, 'height': 55})


server.port = 8521  # The default
server.launch()
