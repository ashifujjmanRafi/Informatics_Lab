
import random
import time
import sys
import os

class TwoLaneCollisionSimulator:
    def __init__(self):
        # Road layout with two lanes
        self.lanes = [
            list("------H-S------"),  # Top lane
            list("===================="),  # Middle separator
            list(" -----------A---")   # Bottom lane
        ]
        
        # Vehicle and sign symbols
        self.SYMBOLS = {
            'H': 'H',   # Human Car
            'A': 'A',   # Autonomous Vehicle
            'S': 'S',   # Stop Sign
            'EMPTY': '-'  # Empty Space
        }
        
        # Tracking vehicle positions
        self.vehicle_positions = {
            'H': {'lane': 0, 'position': self.lanes[0].index('H')},
            'A': {'lane': 2, 'position': self.lanes[2].index('A')}
        }

    def move_vehicles(self):
        # Create a copy of the lanes
        new_lanes = [lane.copy() for lane in self.lanes]
        
        # Move Human Car (Top Lane)
        h_lane = self.vehicle_positions['H']['lane']
        h_pos = self.vehicle_positions['H']['position']
        
        # Move towards stop sign
        if h_pos + 1 < len(self.lanes[h_lane]):
            if self.lanes[h_lane][h_pos + 1] == self.SYMBOLS['S']:
                print("Human Car approaching STOP sign!")
            elif self.lanes[h_lane][h_pos + 1] == self.SYMBOLS['EMPTY']:
                new_lanes[h_lane][h_pos] = self.SYMBOLS['EMPTY']
                new_lanes[h_lane][h_pos + 1] = self.SYMBOLS['H']
                self.vehicle_positions['H']['position'] += 1
        
        # Move Autonomous Vehicle (Bottom Lane)
        a_lane = self.vehicle_positions['A']['lane']
        a_pos = self.vehicle_positions['A']['position']
        
        # Move towards stop sign
        if a_pos + 1 < len(self.lanes[a_lane]):
            if self.lanes[a_lane][a_pos + 1] == self.SYMBOLS['S']:
                print("COLLISION: Autonomous Vehicle crashed into STOP sign!")
                new_lanes[a_lane][a_pos] = 'X'  # Collision marker
            elif self.lanes[a_lane][a_pos + 1] == self.SYMBOLS['EMPTY']:
                new_lanes[a_lane][a_pos] = self.SYMBOLS['EMPTY']
                new_lanes[a_lane][a_pos + 1] = self.SYMBOLS['A']
                self.vehicle_positions['A']['position'] += 1
        
        # Update lanes
        self.lanes = new_lanes

    def display(self):
        print("\nTwo-Lane Collision Scenario")
        print("=" * 30)
        for lane in self.lanes:
            print(''.join(lane))
        print("=" * 30)

def main():
    # Set up file output
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    output_filename = "two_lane_collision_output.txt"
    output_filepath = os.path.join(script_dir, output_filename)

    # Redirect output
    original_stdout = sys.stdout
    with open(output_filepath, 'w') as f:
        sys.stdout = f

        simulator = TwoLaneCollisionSimulator()

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