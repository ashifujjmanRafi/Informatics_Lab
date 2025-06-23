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
        self.collision_occurred = False  # Track if a collision occurred

    def display_road(self):
        # Display the road with all elements
        for lane in self.road:
            print(''.join(lane))
        print('-' * len(self.road[0]))

    def detect_collision(self):
        # Check if AV hits the stop sign
        if self.road[0][self.av_position] == 'S':
            print("Collision detected! AV hit the stop sign.")
            self.road[0][self.av_position] = 'X'  # Mark collision
            self.collision_occurred = True
            return True
        return False

    def move_human_car(self):
        # Move the human-driven car forward
        if self.human_car_position < len(self.road[2]) - 1:  # Ensure the car stays in bounds
            self.road[2][self.human_car_position] = ' '  # Remove car from current position
            self.human_car_position += 1  # Move car forward
            self.road[2][self.human_car_position] = 'H'  # Place car in the new position

    def move_autonomous_vehicle(self):
        # Move the autonomous vehicle forward unless a collision has occurred
        if not self.collision_occurred:
            self.road[0][self.av_position] = ' '
            self.av_position += 1
            if self.av_position < len(self.road[0]):
                if self.road[0][self.av_position] == 'S':
                    self.road[0][self.av_position] = 'X'  # Mark collision after moving to S
                    self.collision_occurred = True
                else:
                    self.road[0][self.av_position] = 'AV'

    def simulate(self):
        # Print legend
        print("H = Human car, AV = Autonomous vehicle, S = Stop sign")

        # Step 1: Initial position
        print("Initial Position:")
        self.display_road()

        while self.human_car_position < len(self.road[2]) - 1:  # Stop simulation when H reaches the end
            self.display_road()

            if self.detect_collision():
                break

            self.move_human_car()
            self.move_autonomous_vehicle()

            time.sleep(0.5)  # Simulate movement delay

        # Ensure H stops at the last position
        self.road[2][self.human_car_position] = 'H'
        print("Final Position: Human car reached the end.")
        self.display_road()
        print("Simulation ended.")

# Simulation parameters
road_length = 20

# Create a RoadCollisionSimulator instance
simulator = RoadCollisionSimulator(road_length)

# Run the simulation
simulator.simulate()
