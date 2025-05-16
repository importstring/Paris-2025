import motor_pair
import color_sensor
import time
from hub import port, button, light_matrix

class PortInitialization:
    def __init__(self):
        self.left_motor = port.A
        self.right_motor = port.B
        motor_pair.pair(motor_pair.PAIR_1, self.left_motor, self.right_motor)

        self.sensor_location = [
            [0, 1, 0],# Sensor 1 at position (0,1)
            [0, 2, 0],# Sensor 2 at position (1,1)
            [0, 0, 0]
        ]

        # Map sensor numbers to ports
        self.sensors = {
            1: port.C if any(1 in row for row in self.sensor_location) else None,
            2: port.D if any(2 in row for row in self.sensor_location) else None
        }

class LineFollower:
    def __init__(self, ports):
        self.ports = ports
        self.base_speed = 40# Conservative speed for reliability
        self.threshold = 50# Prime Lessons recommended midpoint

        # Validate sensors
        self.active_sensors = self._validate_sensors()

    def _validate_sensors(self):
        """Check which sensors are properly configured"""
        return {
            1: self.ports.sensors[1] is not None and color_sensor.reflection(self.ports.sensors[1]) is not None,
            2: self.ports.sensors[2] is not None and color_sensor.reflection(self.ports.sensors[2]) is not None
        }

    def _get_main_sensor(self):
        """Get primary sensor based on sensor_location configuration"""
        if self.active_sensors[1]:
            return self.ports.sensors[1]
        elif self.active_sensors[2]:
            return self.ports.sensors[2]
        else:
            raise ValueError("No valid color sensors detected!")

    def simple_follow(self):
        """Prime Lessons' basic line following algorithm"""
        sensor = self._get_main_sensor()
        try:
            while True:
                reflection = color_sensor.reflection(sensor)

                # Basic edge following logic
                if reflection < self.threshold:
                    # On line - turn right
                    motor_pair.move(motor_pair.PAIR_1, 100, velocity=self.base_speed)
                else:
                    # Off line - turn left
                    motor_pair.move(motor_pair.PAIR_1, -100, velocity=self.base_speed)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            motor_pair.stop(motor_pair.PAIR_1)

class Resources:
    def __init__(self):
        self.ports = PortInitialization()
        self.follower = LineFollower(self.ports)

    def line_follower(self, duration=None):
        """Simple line following entry point"""
        if not any(self.follower.active_sensors.values()):
            raise ValueError("No valid color sensors detected!")

        print("Starting line following...")
        self.follower.simple_follow()

if __name__ == "__main__":
    bot = Resources()
    bot.line_follower()
