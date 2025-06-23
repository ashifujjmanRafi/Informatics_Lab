import time

class RoadCollisionSimulator:
    def __init__(self, road_length):
        # Initialize the road with 3 lanes: top (AV1, H), middle (divider), bottom (AV2)
        self.road = [[' ' for _ in range(road_length)] for _ in range(3)]  
        
        # Initial positions
        self.av1_position = 0  # AV1 starts at the beginning of the top lane
        self.human_position = road_length // 2 + 2  # Human starts in the middle-right of top lane
        self.av2_position = 0  # AV2 starts at the beginning of the bottom lane
        self.av3_position = 0  # AV3 will appear later in the top lane
        
        # Place vehicles in initial positions
        self.road[0][self.av1_position] = 'AV1'  # Place AV1 in the top lane
        self.road[0][self.human_position] = 'H'   # Place Human in the top lane
        self.road[2][self.av2_position] = 'AV2'  # Place AV2 in the bottom lane
        
        # Lane divider setup (alternating '-' and ' ')
        self.road[1] = ['-' if i % 2 == 0 else ' ' for i in range(road_length)]

        # Open a file to write the simulation output
        self.output_file = open("NextStep.txt", "w")

    def write_road_to_file(self, description):
        # Write the description and road state to the file
        self.output_file.write(description + "\n")
        for lane in self.road:
            road_line = ''.join(lane)
            self.output_file.write(road_line + "\n")  # Write each lane to the file
        self.output_file.write('-' * len(self.road[0]) + "\n")  # Separator line
        self.output_file.flush()  # Ensure data is written to the file

    def move_av1(self):
        # Move AV1 forward in the top lane
        if self.av1_position < len(self.road[0]) - 1:
            self.road[0][self.av1_position] = ' '  # Remove AV1 from current position
            self.av1_position += 1  # Move AV1 forward
            if self.road[0][self.av1_position] != 'H':  # Don't overwrite Human
                self.road[0][self.av1_position] = 'AV1'  # Place AV1 in the new position

    def move_av2(self):
        # Move AV2 forward in the bottom lane
        if self.av2_position < len(self.road[2]) - 1:
            self.road[2][self.av2_position] = ' '  # Remove AV2 from current position
            self.av2_position += 1  # Move AV2 forward
            self.road[2][self.av2_position] = 'AV2'  # Place AV2 in the new position

    def add_av3(self):
        # Add AV3 to the top lane at the beginning
        self.av3_position = 0
        self.road[0][self.av3_position] = 'AV3'

    def simulate(self):
        # Step 1: Initial position
        self.write_road_to_file("H = Human,\nAV1,AV2,AV3 = Autonomous Vehicles,\n")
        self.write_road_to_file("Initial Position:")

        # Move vehicles until AV1 is close to Human
        while self.av1_position < self.human_position - 2:
            self.move_av1()
            self.move_av2()
            time.sleep(0.3)

        # Step 2: Position right before Human
        self.write_road_to_file("Position Right Before Human:")

        # Step 3: Final movements and add AV3
        self.move_av1()
        self.move_av2()
        self.add_av3()  # AV3 appears in the final position

        # Step 3: Final position
        self.write_road_to_file("Final Position:")

        self.output_file.write("Simulation ended.\n")  # Write simulation end message
        self.output_file.close()  # Close the file after simulation ends

# Simulation parameters
road_length = 20

# Create an instance of the RoadCollisionSimulator
simulator = RoadCollisionSimulator(road_length)

# Run the simulation
simulator.simulate()