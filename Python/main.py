import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mycolorpy import colorlist
from car_model import TrafficModel

exec_time = 1
model = TrafficModel(3)

init_time = time.time()
while time.time() - init_time < exec_time:
    model.step()
end_time = time.time()

data = model.datacollector.get_model_vars_dataframe()

figure, axis = plt.subplots(figsize=(7, 7))
axis.set_xticks([])
axis.set_yticks([])
patch = plt.imshow(data.iloc[0][0], cmap='Set1')
#plt.colorbar()

def animate(i):
    patch.set_data(data.iloc[i][0])

anim = animation.FuncAnimation(figure, animate, frames=len(data))

plt.show()
