import motor_pair
import color_sensor
import time
import color
import distance_sensor
from hub import port, button, light_matrix
import motor
import sys

class PortInitialization:
    def __init__(self):
        self.left_motor = port.C
        self.right_motor = port.F

        self.sensor_location = [
            [0, 1, 0],# Sensor 1 at position (0,1)
            [0, 2, 0],# Sensor 2 at position (1,1)
            [0, 0, 0]
        ]

        # Map sensor numbers to ports
        self.sensors = {
            1: port.B if any(1 in row for row in self.sensor_location) else None,
            2: port.A if any(2 in row for row in self.sensor_location) else None
        }

        self.first_sensor = port.B # Middle of the robot
        self.second_sesnor = port.A # Left side of robot

class BlockPositioner:
    def __init__(self, ports):
        self.ports = ports
        self.positioned_block = False

    def position_block(self):
        print('Positioning block')
        
        self.positioned_block = True

    def position_robot(self):
        while distance_sensor.distance(port.E) > 5:
            motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -100, 400, 400)
        
        while color_sensor.color(port.B) == color.BLACK:
            motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -180, 200, 200)
        
        for i in range(5):
            motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -90, 50, 50)
            time.sleep(0.3)

    
    def return_back(self):
        "Preform 180 and go back to start"
        motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 180, 100, -100)
        motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -500, 200, 200)
        motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -180, 100, -100)

        motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -180, 100, -100)
        motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 360, 200, 200)

        # Optimal 180° turn calculation
        WHEEL_DIAMETER_MM = 56# SPIKE Prime medium wheel
        AXLE_TRACK_MM = 120    # Distance between wheels
        TURN_DEGREES = (AXLE_TRACK_MM * 180) / (WHEEL_DIAMETER_MM / 2)

        
        motor_pair.move_for_time(motor_pair.PAIR_1, 1000, 0, velocity=-100)
        motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, int(TURN_DEGREES), 100, -100)


    def complete_sequence(self):
        self.position_robot()
        self.position_block()
        self.return_back()


if __name__ == "__main__":
    ports = PortInitialization()
    motor_pair.pair(motor_pair.PAIR_1, port.C, port.F)
    block = BlockPositioner(ports)
    block.complete_sequence()
