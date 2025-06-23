import time

class RoadCollisionSimulator:
    def __init__(self, road_length):
        # Initialize the road with 3 lanes: top (AV), middle (divider), bottom (H)
        self.road = [[' ' for _ in range(road_length)] for _ in range(3)]  
        
        # Initial positions
        self.av_position = 0  # AV starts at the beginning of the top lane
        self.human_position = 0  # Human starts at the beginning of the bottom lane
        self.traffic_light_position = road_length // 2 + 2  # Traffic light in the middle-right
        
        # Place vehicles and traffic light in initial positions
        self.road[0][self.av_position] = 'AV'  # Place AV in the top lane
        self.road[0][self.traffic_light_position] = 'TL:green'  # Place traffic light in top lane
        self.road[2][self.human_position] = 'H'   # Place Human in the bottom lane
        
        # Lane divider setup (alternating '-' and ' ')
        self.road[1] = ['-' if i % 2 == 0 else ' ' for i in range(road_length)]

        # Open a file to write the simulation output
        self.output_file = open("TrafficLightRecog.txt", "w")

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
        if self.av_position < self.traffic_light_position - 2:
            self.road[0][self.av_position] = ' '  # Remove AV from current position
            self.av_position += 1  # Move AV forward
            self.road[0][self.av_position] = 'AV'  # Place AV in the new position

    def move_human(self):
        # Move Human forward in the bottom lane
        if self.human_position < len(self.road[2]) - 1:
            self.road[2][self.human_position] = ' '  # Remove Human from current position
            self.human_position += 1  # Move Human forward
            self.road[2][self.human_position] = 'H'  # Place Human in the new position

    def simulate(self):
        # Step 1: Initial position
        self.write_road_to_file("AV = Autonomous Vehicle,\nH = Human,\nTL:green = Traffic Light (Green)\n")
        self.write_road_to_file("Initial Position:")

        # Move vehicles until AV is close to traffic light
        while self.av_position < self.traffic_light_position - 2:
            self.move_av()
            self.move_human()
            time.sleep(0.3)

        # Step 2: Position right before traffic light
        self.write_road_to_file("Position Right Before TL:")

        # Step 3: Final movement
        self.move_av()
        self.move_human()

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