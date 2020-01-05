#! python3

from drone_swarm import DroneSwarm
from time import sleep
import time
import numpy as np
from PIL import Image

if __name__ == "__main__":
    swarm = DroneSwarm()

    # Nécessaire pour rendre les drones actifs
    swarm.turn_on()
    print("Drones démarrés")
    sleep(1)

    swarm.take_off()
    print("Décollage\n")

    print("Altitudes : " + ", ".join("%0.1f" % p[2]
                                         for p in swarm.get_position()))
    sleep(1)

    speed= 5
    swarm.up(speed)
    sleep(1); swarm.stop(); sleep(1)

    speed= 10
    swarm.forward(speed)
    sleep(15); swarm.stop();sleep(1)

    speed= 0
    swarm.clockwise(speed)
    sleep(5); swarm.stop(); sleep(5)
    
    NomFichier = '/home/louis/Documents/Challenge_drone_swarm/droneswarm-master/swarm_view.png'
      
    
  
    f=swarm.get_swarm_view()
    print(f)
 
    img = Image.fromarray(f, 'RGB')
    r,g,b=img.split()
    img=Image.merge('RGB',(b,g,r))
    img.save(NomFichier)
    img.show()
    

    speed= 10
    swarm.forward(speed)
    sleep(10); swarm.stop()

    start=time.time()
    while(time.time()-start<10):
        t=time.time()
        swarm.set_linear_velocity([5, 0, 0])
        swarm.set_angular_velocity([0,0, np.cos(t)])
        
    swarm.stop()

    swarm.land()
    sleep(10)
    # Nécessaire pour stopper les threads de commande des drones
    swarm.turn_off()
    print("\nDrones éteints")

