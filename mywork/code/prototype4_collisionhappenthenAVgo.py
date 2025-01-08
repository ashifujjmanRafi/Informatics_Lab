import time

class RoadCollisionSimulator:
    def __init__(self, road_length):
        self.road = [[' ' for _ in range(road_length)] for _ in range(3)]  # Two-lane road with divider
        self.road[0][road_length // 2] = 'S'  # Stop sign in the top lane
        self.human_car_position = 0  # Human-driven car starts at the beginning of the bottom lane
        self.av_position = 0  # Autonomous vehicle starts at the beginning of the top lane
        self.road[1] = ['-' if i % 2 == 0 else ' ' for i in range(road_length)]  # Lane divider
        self.road[2][self.human_car_position] = 'H'  # Human car
        self.road[0][self.av_position] = 'AV'  # Autonomous vehicle

    def display_road(self):
        # Display the two-lane road with all elements
        for lane in self.road:
            print(''.join(lane))
        print('-' * len(self.road[0]))

    def detect_collision(self):
        # Check if AV hits the stop sign
        if self.road[0][self.av_position] == 'S':
            print("Collision detected! AV hit the stop sign.")
            self.road[0][self.av_position] = 'X'  # Mark collision
            return True
        return False

    def move_human_car(self):
        # Move the human-driven car forward
        self.road[2][self.human_car_position] = ' '
        self.human_car_position += 1
        if self.human_car_position < len(self.road[2]):
            self.road[2][self.human_car_position] = 'H'

    def move_autonomous_vehicle(self):
        # Move the autonomous vehicle forward
        self.road[0][self.av_position] = ' '
        self.av_position += 1
        if self.av_position < len(self.road[0]):
            self.road[0][self.av_position] = 'AV'
    def simulate(self):
        while self.av_position < len(self.road[0]) - 1:
            self.display_road()

            if self.detect_collision():
                break

            self.move_human_car()
            self.move_autonomous_vehicle()

            time.sleep(0.5)  # Simulate movement delay

        self.display_road()
        print("Simulation ended.")

# Simulation parameters
road_length = 20

# Create a RoadCollisionSimulator instance
simulator = RoadCollisionSimulator(road_length)

# Run the simulation
simulator.simulate()
