import time

class ConstructionZoneSimulator:
    def __init__(self, road_length):
        # Initialize the road with 4 lanes: top (AV), top-middle (cones), 
        # bottom-middle (divider), and bottom (Human car)
        self.road = [[' ' for _ in range(road_length)] for _ in range(4)]  
        
        # Place STOP sign in the construction zone
        stop_sign_position = road_length // 2
        self.road[0][stop_sign_position] = 'S'  # Stop sign in the top lane
        
        # Place traffic cones in the construction zone lane
        for i in range(stop_sign_position - 2, stop_sign_position + 3):
            if i >= 0 and i < road_length:
                self.road[1][i] = 'C'  # Traffic cones
        
        # Initialize vehicle positions
        self.human_car_position = 0  # Human-driven car starts at the beginning of the bottom lane
        self.av_position = 0  # Autonomous vehicle starts at the beginning of the top lane
        
        # Place vehicles on the road
        self.road[3][self.human_car_position] = 'H'  # Place human car in the bottom lane
        self.road[0][self.av_position] = 'AV'  # Place autonomous vehicle in the top lane
        
        # Track collision and simulation state
        self.collision_occurred = False
        
        # Create lane divider (alternating '-' and ' ')
        self.road[2] = ['-' if i % 2 == 0 else ' ' for i in range(road_length)]

        # Open file for simulation output
        self.output_file = open("road_construction_simulation.txt", "w")

    def write_road_to_file(self, description):
        # Write description and current road state to file
        self.output_file.write(description + "\n")
        lane_labels = ["AV Lane:", "Construction Zone:", "Lane Divider:", "Human Car Lane:"]
        for i, lane in enumerate(self.road):
            road_line = ''.join(lane)
            self.output_file.write(f"{lane_labels[i]} {road_line}\n")
        self.output_file.write('-' * len(self.road[0]) + "\n")  # Separator
        self.output_file.flush()

    def detect_collision(self):
        # Collision detection for construction zone
        # Check for stop sign and construction zone obstacles
        if self.road[0][self.av_position] == 'S':
            # AV encounters stop sign
            self.road[0][self.av_position] = 'X'  # Mark collision
            self.write_road_to_file("Collision Detection: AV Stopped at STOP Sign")
            self.collision_occurred = True
            return True
        
        # Check for traffic cones
        if self.road[1][self.av_position] == 'C':
            # AV hits traffic cone
            self.road[0][self.av_position] = 'X'  # Mark collision
            self.write_road_to_file("Collision Detection: AV Hit Traffic Cone")
            self.collision_occurred = True
            return True
        
        return False

    def move_human_car(self):
        # Move human-driven car
        self.road[3][self.human_car_position] = ' '  # Clear current position
        self.human_car_position += 1  # Move forward
        if self.human_car_position < len(self.road[3]):
            self.road[3][self.human_car_position] = 'H'  # Place in new position

    def move_autonomous_vehicle(self):
        # Move autonomous vehicle
        if not self.collision_occurred:
            self.road[0][self.av_position] = ' '  # Clear current position
            self.av_position += 1  # Move forward
            
            if self.av_position < len(self.road[0]):
                # Careful navigation around obstacles
                if self.road[0][self.av_position] in ['S', 'C']:
                    # Stop or avoid obstacles
                    self.road[0][self.av_position] = 'AV'
                else:
                    self.road[0][self.av_position] = 'AV'  # Normal movement

    def simulate(self):
        # Initial setup and simulation
        self.write_road_to_file("Construction Zone Simulation Legend:\n"
                                "H = Human Car, AV = Autonomous Vehicle\n"
                                "S = Stop Sign, C = Traffic Cone")
        
        self.write_road_to_file("Initial Road Configuration:")

        # Simulation loop
        while self.av_position < len(self.road[0]) - 1:
            if self.detect_collision():
                break

            # Snapshot before construction zone
            if self.av_position == len(self.road[0]) // 2 - 2:
                self.write_road_to_file("Approaching Construction Zone:")

            self.move_human_car()
            self.move_autonomous_vehicle()

            time.sleep(0.5)  # Simulate movement delay

        # Continue moving human car after AV stops
        while self.human_car_position < len(self.road[3]) - 1:
            self.move_human_car()
            time.sleep(0.1)

        # Final simulation state
        self.write_road_to_file("Final Road State: Simulation Completed")

        self.output_file.write("Construction Zone Simulation Ended.\n")
        self.output_file.close()

# Simulation parameters
road_length = 25

# Create and run simulation
simulator = ConstructionZoneSimulator(road_length)
simulator.simulate()