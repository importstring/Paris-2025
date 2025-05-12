import motor_pair 
import color_sensor
import time
import distance_sensor
import force_sensor
from hub import port, button, light_matrix, motion_sensor, sound
import color

class PortInitialization:
    def __init__(self):
        """
        This class serves as a way to easily change the ports on the fly in an easy and organized fashion
        where everything is labled and easy to change. 
        """

        self.left_motor = port.A
        self.right_motor = port.B
        motor_pair.pair(motor_pair.PAIR_1, self.left_motor, self.right_motor)
        
        self.left_sensor = port.C
        self.right_sensor = port.D
        
        self.distance_sensor = port.E

        self.sensor_location = [
            [0, 1, 0],
            [0, 1, 0],
            [0, 0, 0]
            ]

class Resources:
    """
    This class serves the function of allowing us to adapt on the fly to any conditions Paris might 
    throw our way.
    """
    def __init__(self):
        ports = PortInitialization()
        
    def line_follower(self, duration=None, turns=[]):
        """
        The goal here is to anticipate all potential times we will need to
        use line following adapting this function to any and all scenerios. So that
        means adding extra optional params like time and next turn. Or even
        next turns (Every single turn Ex: [LWLWLWLWWW]) so that we can control
        which direction the robot goes when line following. Additionally
        we need to anticipate the potential requirement for different 
        places that the color sensor can be. There are two color sensor placements
        and we need to anticipate that this may change so we need sub logic.
        E.g
        [
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0]
        ]

        Params:
        |--> self
        |----> motors
        |----> sensor placement
        |--> duration --> optional: int
        |-----> amount of time in seconds that the robot should do something for
        |--> turns --> optional: array
        |------> ['W/L']
        """
        pass



class Controls:
    def __init__(self, port_init):
        pass
