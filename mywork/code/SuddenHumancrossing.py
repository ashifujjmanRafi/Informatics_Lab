import time

class RoadCollisionSimulator:
    def __init__(self, road_length):
        # Initialize the road with 2 lanes: top (AV and Human), bottom (divider)
        self.road = [[' ' for _ in range(road_length)] for _ in range(2)]  
        
        # Initial positions
        self.av_position = 0  # AV starts at the beginning of the top lane
        self.human_position = road_length // 2 + 1  # Human will appear later in the middle-right
        
        # Place AV in initial position
        self.road[0][self.av_position] = 'AV'  # Place AV in the top lane
        
        # Lane divider setup (alternating '-' and ' ')
        self.road[1] = ['-' if i % 2 == 0 else ' ' for i in range(road_length)]

        # Open a file to write the simulation output
        self.output_file = open("Suddenhumancrossing.txt", "w")

    def write_road_to_file(self, description):
        # Write the description and road state to the file
        self.output_file.write(description + "\n")
        for lane in self.road:
            road_line = ''.join(lane)
            self.output_file.write(road_line + "\n")  # Write each lane to the file
        self.output_file.write('-' * len(self.road[0]) + "\n")  # Separator line
        self.output_file.flush()  # Ensure data is written to the file

    def move_av(self):
        # Move AV forward in the top lane
        if self.av_position < len(self.road[0]) - 1:
            self.road[0][self.av_position] = ' '  # Remove AV from current position
            self.av_position += 1  # Move AV forward
            if self.road[0][self.av_position] != 'H':  # Don't overwrite Human
                self.road[0][self.av_position] = 'AV'  # Place AV in the new position

    def add_human(self):
        # Human suddenly appears in the road
        self.road[0][self.human_position] = 'H'

    def simulate(self):
        # Header information
        self.write_road_to_file("H = Human,\nAV = Autonomous Vehicles,\n")
        
        # Step 1: Initial position (only AV visible)
        self.write_road_to_file("Initial Position:")

        # Move AV until it's close to where human will appear
        while self.av_position < self.human_position - 2:
            self.move_av()
            time.sleep(0.3)

        # Human suddenly crosses - add human to the scene
        self.add_human()
        
        # Step 2: Position right before Human (human has suddenly appeared)
        self.write_road_to_file("Position Right Before H:")

        self.output_file.write("Simulation ended.\n")  # Write simulation end message
        self.output_file.close()  # Close the file after simulation ends

# Simulation parameters
road_length = 15

# Create an instance of the RoadCollisionSimulator
simulator = RoadCollisionSimulator(road_length)

# Run the simulation
simulator.simulate()