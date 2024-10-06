import matplotlib.pyplot as plt
from math import sin,pi,cos
import sympy
from game import Game

game = Game()
plt.style.use('seaborn-v0_8-white')
input_values = []
a=0
while a<20:
    input_values.append(a)
    a+=0.001
y_values = []
x_values = []

for a in input_values:
    x,y = game.track(600,400,a)

    x_values.append(x)
    y_values.append(-y)


fig, ax = plt.subplots()
ax.scatter(x_values,y_values,s=10)
#ax.scatter(x_values,y_values,s=5,c=y_values,cmap=plt.cm.Blues)
ax.set_title("track",fontsize=24)
ax.set_xlabel("x",fontsize=14)
ax.set_ylabel("y",fontsize=14)
ax.tick_params(labelsize=14)

plt.tight_layout()
plt.show()
plt.savefig('track.png',bbox_inches='tight')