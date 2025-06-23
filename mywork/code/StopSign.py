import time

class RoadCollisionSimulator:
    def __init__(self, road_length):
        # Initialize the road with 2 lanes: top (AV and Stop Sign), bottom (divider - other lane is open)
        self.road = [[' ' for _ in range(road_length)] for _ in range(2)]  
        
        # Initial positions
        self.av_position = 0  # AV starts at the beginning of the top lane
        self.stop_sign_position = road_length // 2  # Stop sign in the middle of top lane
        
        # Place AV and stop sign in initial positions
        self.road[0][self.av_position] = 'AV'  # Place AV in the top lane
        self.road[0][self.stop_sign_position] = 'S'  # Place stop sign in top lane
        
        # Lane divider setup (alternating '-' and ' ') - represents the other open lane
        self.road[1] = ['-' if i % 2 == 0 else ' ' for i in range(road_length)]

        # Open a file to write the simulation output
        self.output_file = open("StopSign.txt", "w")

    def write_road_to_file(self, description):
        # Write the description and road state to the file
        self.output_file.write(description + "\n")
        for lane in self.road:
            road_line = ''.join(lane)
            self.output_file.write(road_line + "\n")  # Write each lane to the file
        self.output_file.write('-' * len(self.road[0]) + "\n")  # Separator line
        self.output_file.flush()  # Ensure data is written to the file

    def move_av(self):
        # Move AV forward in the top lane towards stop sign
        if self.av_position < self.stop_sign_position - 1:
            self.road[0][self.av_position] = ' '  # Remove AV from current position
            self.av_position += 1  # Move AV forward
            self.road[0][self.av_position] = 'AV'  # Place AV in the new position

    def simulate(self):
        # Header information
        self.write_road_to_file("AV = Autonomous Vehicles,\nS = Stop Sign of a partial road,\nOther lane is open.\n")
        
        # Step 1: Initial position
        self.write_road_to_file("Initial Position:")

        # Move AV until it's right before the stop sign
        while self.av_position < self.stop_sign_position - 1:
            self.move_av()
            time.sleep(0.3)

        # Step 2: Position right before stop sign
        self.write_road_to_file("Position Right Before STOP sign:")

        self.output_file.write("Simulation ended.\n")  # Write simulation end message
        self.output_file.close()  # Close the file after simulation ends

# Simulation parameters
road_length = 15

# Create an instance of the RoadCollisionSimulator
simulator = RoadCollisionSimulator(road_length)

# Run the simulation
simulator.simulate()