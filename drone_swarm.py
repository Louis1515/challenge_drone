from drone import Drone
import numpy as np
import cv2

class DroneSwarm():
    """
    Class used to manager a drone swarm, allowing to drive each of the
    drones individually. The different command methods can either drive a
    single drone (by specifying the ``drone`` argument, an integer between
    0 and the total number of drones, excluded), or the whole swarm (by leaving
    ``drone`` to None).
    """

    # Number of drone in the swarm, should be coherent with context.world
    drones_number = 5

    def __init__(self):
        self.drones = [Drone(i) for i in range(1, self.drones_number+1)]
        self.swarm_view = np.zeros((360*2, 640*3,3))
        
    def get_swarm_view(self):
        """
        Return the view of the whole swarm as a single image.
        """
        line1 = np.hstack((np.hstack((self.drones[0].view, self.drones[1].view)), self.drones[2].view))
        line2 = np.hstack((np.hstack((self.drones[3].view, self.drones[4].view)), np.zeros((360, 640,3), np.uint8)))
        self.swarm_view = np.vstack((line1,line2))
       
        return self.swarm_view
    
    def get_view(self, drone=None):
        """
        Return a list of each drone view, as np.ndarray.
        """
        return self.__swarm_get("view", drone)

    def get_sonar(self, drone=None):
        return self.__swarm_get("sonar", drone)

    def get_linear_velocity(self, drone=None):
        convert = lambda v : [getattr(v.linear, c) for c in 'xyz']
        if drone is None:
            return [convert(d.vel) for d in self.drones]
        else:
            return convert(self.drones[drone].vel)

    def get_angular_velocity(self, drone=None):
        convert = lambda v : [getattr(v.angular, c) for c in 'xyz']
        if drone is None:
            return [convert(d.vel) for d in self.drones]
        else:
            return convert(self.drones[drone].vel)

    def get_position(self, drone=None):
        return self.__swarm_get("position", drone)

    def get_orientation(self, drone=None):
        """
        Return the orientation as a quaternion.
        """
        return self.__swarm_get("orientation", drone)

    def turn_on(self, drone=None):
        self.__swarm_do("turn_on", drone)

    def turn_off(self, drone=None):
        self.__swarm_do("turn_off", drone)

    def take_off(self, drone=None):
        self.__swarm_do("take_off", drone)
    
    def land(self, drone=None): 
        self.__swarm_do("land", drone)

    def stop(self, drone=None):
        self.__swarm_do("stop", drone)

    def set_linear_velocity(self, lv, drone=None):
        """lv is a array [v.x, v.y, v.z]"""
        self.__swarm_do("set_linear_velocity", drone, lv)

    def set_angular_velocity(self, av, drone=None):
        """av is a array [w.x, w.y, w.z]"""
        self.__swarm_do("set_angular_velocity", drone, av)

    def up(self, speed, drone=None):
        self.__swarm_do("up", drone, speed)

    def down(self, speed, drone=None):
        self.__swarm_do("down", drone, speed)

    def forward(self, speed, drone=None):
        self.__swarm_do("forward", drone, speed)

    def backward(self, speed, drone=None):
        self.__swarm_do("backward", drone, speed)

    def right(self, speed, drone=None):
        self.__swarm_do("right", drone, speed)

    def left(self, speed, drone=None):
        self.__swarm_do("left", drone, speed)

    def clockwise(self, speed, drone=None):
        self.__swarm_do("clockwise", drone, speed)

    def counter_clockwise(self, speed, drone=None):
        self.__swarm_do("counter_clockwise", drone, speed)

    def __swarm_do(self, f, drone_id=None, *args, **kwargs):
        """
        If drone_id is None then call f for each of the swarm drone, else
        call self.f with drone_id argument.
        """
        if drone_id is None:
            for drone in self.drones:
                getattr(drone, f)(*args, **kwargs)
        else:
            getattr(self.drones[drone_id], f)(*args, **kwargs)

    def __swarm_get(self, attr, drone_id=None):
        """
        If drone_id is None then return the list of the drones ``attr``
        attribute, else return the attribute of drone_id.
        """
        if drone_id is None:
            return [getattr(drone, attr) for drone in self.drones]
        else:
            return getattr(self.drones[drone_id], attr)

if __name__ == "__main__":
    swarm = DroneSwarm()
    swarm.turn_on()
    swarm.take_off()