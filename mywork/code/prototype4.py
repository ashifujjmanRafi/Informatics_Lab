import random
import time
import sys
import os

class RoadCollisionSimulator:
    def __init__(self):
        # Road layout
        self.road = [
            list("---------------"),  # Top lane
            list("---------------"),  # Bottom lane
        ]
        
        # Vehicle symbols
        self.VEHICLES = {
            'HMC': 'H',   # Human Car
            'AV': 'A',    # Autonomous Vehicle
            'STOP': 'S',  # Stop Sign
            'EMPTY': '-'  # Empty Space
        }
        
        # Initial vehicle placement
        self.road[0][5] = self.VEHICLES['HMC']  # Human Car
        self.road[1][10] = self.VEHICLES['AV']  # Autonomous Vehicle
        self.road[0][8] = self.VEHICLES['STOP']  # Stop Sign

    def move_vehicles(self):
        # Create a copy of the road to avoid simultaneous modification
        new_road = [lane.copy() for lane in self.road]
        
        for lane_idx, lane in enumerate(self.road):
            for spot_idx, spot in enumerate(lane):
                # Move Human Car
                if spot == self.VEHICLES['HMC']:
                    # Move right if possible
                    if spot_idx + 1 < len(lane) and lane[spot_idx + 1] == self.VEHICLES['EMPTY']:
                        new_road[lane_idx][spot_idx] = self.VEHICLES['EMPTY']
                        new_road[lane_idx][spot_idx + 1] = self.VEHICLES['HMC']
                
                # Move Autonomous Vehicle
                if spot == self.VEHICLES['AV']:
                    # Check for stop sign
                    if spot_idx + 1 < len(lane) and lane[spot_idx + 1] == self.VEHICLES['STOP']:
                        print("CRASH: Autonomous Vehicle collided with STOP sign!")
                        new_road[lane_idx][spot_idx] = 'X'  # Collision marker
                    elif spot_idx + 1 < len(lane) and lane[spot_idx + 1] == self.VEHICLES['EMPTY']:
                        new_road[lane_idx][spot_idx] = self.VEHICLES['EMPTY']
                        new_road[lane_idx][spot_idx + 1] = self.VEHICLES['AV']
        
        # Update the road
        self.road = new_road

    def display(self):
        print("\nRoad Simulation")
        print("=" * 20)
        for lane in self.road:
            print(''.join(lane))
        print("=" * 20)

def main():
    # Set up file output
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    output_filename = "road_collision_output.txt"
    output_filepath = os.path.join(script_dir, output_filename)

    # Redirect output
    original_stdout = sys.stdout
    with open(output_filepath, 'w') as f:
        sys.stdout = f

        simulator = RoadCollisionSimulator()

        # Run simulation for 10 steps
        for step in range(10):
            print(f"\nStep {step + 1}:")
            simulator.move_vehicles()
            simulator.display()
            time.sleep(1)

    # Restore standard output
    sys.stdout = original_stdout
    print(f"Simulation output saved to {output_filepath}")

if __name__ == "__main__":
    main()