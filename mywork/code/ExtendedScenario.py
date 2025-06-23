import time

class RoadCollisionSimulator:
    def __init__(self, road_length):
        # Initialize the road with 2 lanes: top (AVs), bottom (divider)
        self.road = [[' ' for _ in range(road_length)] for _ in range(2)]  
        self.road[0][road_length // 2] = 'S'  # Stop sign in the top lane (initially at the middle)
        
        # Position AV1 (truck) closer to stop sign, AV2 (car) further back
        self.av1_position = road_length // 2 - 2  # AV1 truck starts 2 positions before stop sign
        self.av2_position = 0  # AV2 car starts at the beginning of the top lane
        
        self.road[0][self.av1_position] = 'AV1'  # Place AV1 truck in the top lane
        self.road[0][self.av2_position] = 'AV2'  # Place AV2 car in the top lane
        
        self.collision_occurred = False  # Track if a collision occurred
        
        # Lane divider setup (alternating '-' and ' ')
        self.road[1] = ['-' if i % 2 == 0 else ' ' for i in range(road_length)]

        # Open a file to write the simulation output
        self.output_file = open("ExtendedScenario.txt", "w")

    def write_road_to_file(self, description):
        # Write the description and road state to the file
        self.output_file.write(description + "\n")
        for lane in self.road:
            road_line = ''.join(lane)
            self.output_file.write(road_line + "\n")  # Write each lane to the file
        self.output_file.write('-' * len(self.road[0]) + "\n")  # Separator line
        self.output_file.flush()  # Ensure data is written to the file

    def detect_collision(self):
        # Check if AV1 hits the stop sign in the top lane
        if self.road[0][self.av1_position] == 'S':
            # Collision detected, mark with X
            self.road[0][self.av1_position] = 'X'  # Mark collision with 'X'
            self.collision_occurred = True
            return True
        return False

    def move_av2_car(self):
        # Move AV2 car forward in the top lane (only if no collision occurred)
        if not self.collision_occurred and self.av2_position < self.av1_position - 1:
            self.road[0][self.av2_position] = ' '  # Remove AV2 from current position
            self.av2_position += 1  # Move AV2 forward
            if self.av2_position < len(self.road[0]):
                self.road[0][self.av2_position] = 'AV2'  # Place AV2 in the new position

    def move_av1_truck(self):
        # Move AV1 truck forward in the top lane
        if not self.collision_occurred:
            self.road[0][self.av1_position] = ' '  # Remove AV1 from current position
            self.av1_position += 1  # Move AV1 forward
            if self.av1_position < len(self.road[0]):
                if self.road[0][self.av1_position] == 'S':
                    # Do not update AV1 to 'X' here; collision detection will handle this.
                    pass
                else:
                    self.road[0][self.av1_position] = 'AV1'  # Place AV1 in the new position

    def simulate(self):
        # Step 1: Initial position
        self.write_road_to_file("AV2 = Autonomous Car,\nAV1 = Autonomous Truck,\nS = Stop Sign\n")
        self.write_road_to_file("Initial Position:")

        # Step 2: Move to position right before STOP
        # Move vehicles until AV1 is one step away from stop sign
        stop_sign_position = len(self.road[0]) // 2
        while self.av1_position < stop_sign_position - 1:
            self.move_av2_car()
            self.move_av1_truck()
            time.sleep(0.5)  # Simulate movement delay

        # Write the "Position Right Before STOP" state
        self.write_road_to_file("Position Right Before STOP:")

        # Step 3: Final move - AV1 hits the stop sign
        self.move_av2_car()
        self.move_av1_truck()
        
        # Detect collision and mark with X
        self.detect_collision()

        # Write final position
        self.write_road_to_file("Final Position:")

        self.output_file.write("Simulation ended.\n")  # Write simulation end message
        self.output_file.close()  # Close the file after simulation ends

# Simulation parameters
road_length = 20

# Create an instance of the RoadCollisionSimulator
simulator = RoadCollisionSimulator(road_length)

# Run the simulation
simulator.simulate()