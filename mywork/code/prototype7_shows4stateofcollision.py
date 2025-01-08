import time

class RoadCollisionSimulator:
    def __init__(self, road_length):
        # Initialize the road with 3 lanes: top (AV), middle (divider), and bottom (Human car)
        self.road = [[' ' for _ in range(road_length)] for _ in range(3)]  
        self.road[0][road_length // 2] = 'S'  # Stop sign in the top lane (initially at the middle)
        self.human_car_position = 0  # Human-driven car starts at the beginning of the bottom lane
        self.av_position = 0  # Autonomous vehicle starts at the beginning of the top lane
        self.road[2][self.human_car_position] = 'H'  # Place human car in the bottom lane
        self.road[0][self.av_position] = 'AV'  # Place autonomous vehicle in the top lane
        self.collision_occurred = False  # Track if a collision occurred
        
        # Correct lane divider setup (initializing lane divider as alternating '-' and ' ')
        self.road[1] = ['-' if i % 2 == 0 else ' ' for i in range(road_length)]

        # Open a file to write the simulation output
        self.output_file = open("collision_situation.txt", "w")

    def write_road_to_file(self, description):
        # Write the description and road state to the file
        self.output_file.write(description + "\n")
        for lane in self.road:
            road_line = ''.join(lane)
            self.output_file.write(road_line + "\n")  # Write each lane to the file
        self.output_file.write('-' * len(self.road[0]) + "\n")  # Separator line
        self.output_file.flush()  # Ensure data is written to the file

    def detect_collision(self):
        # Check if the AV hits the stop sign in the top lane
        if self.road[0][self.av_position] == 'S':
            # Collision detected, write states to file in 2 steps


            # Step 1: Collision with stop sign
            self.road[0][self.av_position] = 'X'  # Mark collision with 'X'
            self.write_road_to_file("Complete Stop Step: Marking Stop with 'X'.")

            self.collision_occurred = True
            return True
        return False

    def move_human_car(self):
        # Move the human-driven car forward in the bottom lane
        self.road[2][self.human_car_position] = ' '  # Remove car from current position
        self.human_car_position += 1  # Move car forward
        if self.human_car_position < len(self.road[2]):
            self.road[2][self.human_car_position] = 'H'  # Place car in the new position

    def move_autonomous_vehicle(self):
        # Move the autonomous vehicle forward in the top lane
        if not self.collision_occurred:
            self.road[0][self.av_position] = ' '  # Remove AV from current position
            self.av_position += 1  # Move AV forward
            if self.av_position < len(self.road[0]):
                if self.road[0][self.av_position] == 'S':
                    # Do not update AV to 'X' here; collision detection will handle this.
                    pass
                else:
                    self.road[0][self.av_position] = 'AV'  # Place AV in the new position

    def simulate(self):
        # Step 1: Initial position
        self.write_road_to_file("H = Human Car,\nAV = Autonomous Vechiels, \nS = Stop Sign\n")
        self.write_road_to_file("Initial Position:")

        while self.av_position < len(self.road[0]) - 1:  # Continue until the AV reaches the end of the road
            if self.detect_collision():
                break

            # Step 2: Before collision, when AV is one step away from stop sign
            if self.av_position == len(self.road[0]) // 2 - 1:
                self.write_road_to_file("Position Right Before STOP:")

            self.move_human_car()
            self.move_autonomous_vehicle()

            time.sleep(0.5)  # Simulate movement delay

        # After collision, continue moving only the human car
        while self.human_car_position < len(self.road[2]) - 1:
            self.move_human_car()
            time.sleep(0.1)

        # Step 4: Final position
        self.write_road_to_file("Final Position: Human car reached the end.")

        self.output_file.write("Simulation ended.\n")  # Write simulation end message
        self.output_file.close()  # Close the file after simulation ends

# Simulation parameters
road_length = 20

# Create an instance of the RoadCollisionSimulator
simulator = RoadCollisionSimulator(road_length)

# Run the simulation
simulator.simulate()
