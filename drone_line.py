#! python3

from drone_swarm import DroneSwarm
from time import sleep
import time
import numpy as np
from PIL import Image
import rospy
import random
import wall_limit

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

    # #toward_target
    # area=0
    # i=0
    # t=rospy.get_time()
    # while area<400:
    #     xy=[0,0]
    #     while xy[1]<317 or xy[1]>322:
    #         if rospy.get_time()-t>0.2:
    #             i+=1
    #             t=rospy.get_time()
    #             NomFichier = '/home/louis/Documents/Challenge_drone_swarm/droneswarm-master/img/test'+str(i)+'im.png'   
    #             f=swarm.get_view(3)
    #             img = Image.fromarray(f, 'RGB')
    #             r,g,b=img.split()
    #             img=Image.merge('RGB',(b,g,r))
    #             img.save(NomFichier)
    #             xy,area=wall_limit.detect_guy(swarm.drones[3].view,i)
    #             print(xy)
    #             print(area)
    #             if area>400:
    #                 break
    #             swarm.drones[3].clockwise((320-xy[1])/320)
    #     swarm.drones[3].clockwise(0)
    #     swarm.drones[3].forward(10)
       
    # print('Target reached')
    # swarm.drones[3].stop()
    # sleep(4)

    #detect_wall
    speed= 10
    sleep(5)
    
    while True:
    
        wall_detected, size_wall=wall_limit.detect_wall(swarm.drones[3].view)
        t=rospy.get_time()
        i=0
        area=0

        while wall_detected=='RAS':
            
            if rospy.get_time()-t>0.2:
                swarm.drones[3].forward(speed)
                i+=1
                t=rospy.get_time()
                NomFichier = '/home/louis/Documents/Challenge_drone_swarm/droneswarm-master/img/test'+str(i)+'im.png'   
                f=swarm.get_view(3)
                img = Image.fromarray(f, 'RGB')
                r,g,b=img.split()
                img=Image.merge('RGB',(b,g,r))
                img.save(NomFichier)
                wall_detected, size_wall=wall_limit.detect_wall(swarm.drones[3].view,i)
                print('Detected wall: '+ str(size_wall))
                xy,area=wall_limit.detect_guy(swarm.drones[3].view,i)
                print('Detected guy: ['+str(xy) +'] and area = ' + str(area)+'.')
                if area>40:
                    break
        
        swarm.drones[3].stop()
        sleep(2)
        while area<400 and area>40:
            xy=[0,0]
            while xy[1]<317 or xy[1]>322:
                if rospy.get_time()-t>0.2:
                    i+=1
                    t=rospy.get_time()
                    NomFichier = '/home/louis/Documents/Challenge_drone_swarm/droneswarm-master/img/test'+str(i)+'im.png'   
                    f=swarm.get_view(3)
                    img = Image.fromarray(f, 'RGB')
                    r,g,b=img.split()
                    img=Image.merge('RGB',(b,g,r))
                    img.save(NomFichier)
                    xy,area=wall_limit.detect_guy(swarm.drones[3].view,i)
                    print('Getting closer to the detected guy: ['+str(xy) +'] and area = ' + str(area)+'.')
                    if area>400 or area<40:
                        break
                    swarm.drones[3].clockwise((320-xy[1])/320)
            swarm.drones[3].clockwise(0)
            swarm.drones[3].forward(10)

        if area>400:
            print('Target reached')
            swarm.drones[3].stop()
            sleep(4)
            swarm.drones[3].clockwise(10) 
            sleep(3*random.random())
       
        if wall_detected=='right':
                swarm.drones[3].clockwise(1) 
                sleep(3*random.random())
            
        if wall_detected=='left':
            swarm.drones[3].clockwise(-1)
            sleep(3*random.random()) 

        while wall_detected!='RAS':       
            if rospy.get_time()-t>0.2:
                i+=1
                t=rospy.get_time()
                NomFichier = '/home/louis/Documents/Challenge_drone_swarm/droneswarm-master/img/test'+str(i)+'im.png'   
                f=swarm.get_view(3)
                img = Image.fromarray(f, 'RGB')
                r,g,b=img.split()
                img=Image.merge('RGB',(b,g,r))
                img.save(NomFichier)
                wall_detected, size_wall=wall_limit.detect_wall(swarm.drones[3].view,i)  
                print('The wall size is: '+str(size_wall))   
                if wall_detected=='right':
                    swarm.drones[3].clockwise(1)             
                if wall_detected=='left':
                    swarm.drones[3].clockwise(-1)
                    
                
        swarm.stop()
        sleep(4)

    swarm.down(0.5)
    sleep(0.5)
    swarm.land()
    sleep(10)
    # Nécessaire pour stopper les threads de commande des drones
    swarm.turn_off()
    print("\nDrones éteints")

