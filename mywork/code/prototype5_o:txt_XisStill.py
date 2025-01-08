# import time

# class RoadCollisionSimulator:
#     def __init__(self, road_length):
#         self.road = [[' ' for _ in range(road_length)] for _ in range(3)]  # Two-lane road with divider
#         self.road[0][road_length // 2] = 'S'  # Stop sign in the top lane
#         self.human_car_position = 0  # Human-driven car starts at the beginning of the bottom lane
#         self.av_position = 0  # Autonomous vehicle starts at the beginning of the top lane
#         self.road[1] = ['-' if i % 2 == 0 else ' ' for i in range(road_length)]  # Lane divider
#         self.road[2][self.human_car_position] = 'H'  # Human car
#         self.road[0][self.av_position] = 'AV'  # Autonomous vehicle

#     def display_road(self):
#         # Display the two-lane road with all elements
#         for lane in self.road:
#             print(''.join(lane))
#         print('-' * len(self.road[0]))

#     def detect_collision(self):
#         # Check if AV hits the stop sign
#         if self.road[0][self.av_position] == 'S':
#             print("Collision detected! AV hit the stop sign.")
#             return True
#         return False

#     def move_human_car(self):
#         # Move the human-driven car forward
#         self.road[2][self.human_car_position] = ' '
#         self.human_car_position += 1
#         if self.human_car_position < len(self.road[2]):
#             self.road[2][self.human_car_position] = 'H'

#     def move_autonomous_vehicle(self):
#         # Move the autonomous vehicle forward unless a collision has occurred
#         if not self.detect_collision():
#             self.road[0][self.av_position] = ' '
#             self.av_position += 1
#             if self.road[0][self.av_position] == 'S':
#                 self.road[0][self.av_position] = 'X'  # Mark collision after moving to S
#             elif self.av_position < len(self.road[0]):
#                 self.road[0][self.av_position] = 'AV'

#     def simulate(self):
#         while self.av_position < len(self.road[0]) - 1:
#             self.display_road()

#             if self.detect_collision():
#                 break

#             self.move_human_car()
#             self.move_autonomous_vehicle()

#             time.sleep(0.5)  # Simulate movement delay

#         self.display_road()
#         print("Simulation ended.")

# # Simulation parameters
# road_length = 20

# # Create a RoadCollisionSimulator instance
# simulator = RoadCollisionSimulator(road_length)

# # Run the simulation
# simulator.simulate()

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
        self.output_file = open("simulation_output.txt", "w")

    def display_road(self):
        # Display the road with all elements (AV, Human car, lane divider, etc.)
        for lane in self.road:
            road_line = ''.join(lane)
            self.output_file.write(road_line + "\n")  # Write each lane to the file
        self.output_file.write('-' * len(self.road[0]) + "\n")  # Separator line
        self.output_file.flush()  # Ensure data is written to the file

    def detect_collision(self):
        # Check if the AV hits the stop sign in the top lane
        if self.road[0][self.av_position] == 'S':
            collision_message = "Collision detected! AV hit the stop sign.\n"
            self.output_file.write(collision_message)  # Write collision message to file
            self.output_file.flush()
            self.road[0][self.av_position] = 'X'  # Mark the collision
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
                    self.road[0][self.av_position] = 'X'  # Mark collision if it hits stop sign
                    self.collision_occurred = True
                else:
                    self.road[0][self.av_position] = 'AV'  # Place AV in the new position

    def simulate(self):
        while self.av_position < len(self.road[0]) - 1:  # Continue until the AV reaches the end of the road
            self.display_road()

            if self.detect_collision():
                break

            self.move_human_car()
            self.move_autonomous_vehicle()

            time.sleep(0.5)  # Simulate movement delay

        # After collision, continue moving only the human car
        while self.human_car_position < len(self.road[2]) - 1:
            self.display_road()
            self.move_human_car()
            time.sleep(0.1)

        self.display_road()
        self.output_file.write("Simulation ended.\n")  # Write simulation end message
        self.output_file.close()  # Close the file after simulation ends

# Simulation parameters
road_length = 20

# Create an instance of the RoadCollisionSimulator
simulator = RoadCollisionSimulator(road_length)

# Run the simulation
simulator.simulate()
