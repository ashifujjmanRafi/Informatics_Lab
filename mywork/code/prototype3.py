import random
import time
import sys
import os

class LaneConstructionSimulator:
    def __init__(self):
        # Symbols
        self.SYMBOLS = {
            'P': '🚧',    # Partially Open Lane
            'S': '🛑',    # Stop Sign
            'AV-C': '🚗', # Autonomous Car
            'AV-T': '🚛', # Autonomous Truck
            'H': '🚙',    # Human-driven Car
            'EMPTY': '▫️'  # Empty Space
        }
        
        # Lane configuration
        self.lane = [
            [self.SYMBOLS['EMPTY'], self.SYMBOLS['EMPTY'], self.SYMBOLS['P'], self.SYMBOLS['EMPTY'], self.SYMBOLS['AV-C']],
            [self.SYMBOLS['EMPTY'], self.SYMBOLS['S'], self.SYMBOLS['EMPTY'], self.SYMBOLS['AV-T'], self.SYMBOLS['AV-C']]
        ]
        
        self.vehicles = []
        self.vehicle_id_counter = 1

    def generate_vehicle(self):
        vehicle_types = ['AV-C', 'AV-T', 'H']
        vehicle_type = random.choice(vehicle_types)
        vehicle_id = f"{vehicle_type}-{self.vehicle_id_counter}"
        self.vehicle_id_counter += 1
        
        return {
            'id': vehicle_id,
            'type': vehicle_type,
            'symbol': self.SYMBOLS[vehicle_type]
        }

    def place_vehicle(self, vehicle):
        # Find an empty spot
        for lane_idx, lane_row in enumerate(self.lane):
            for spot_idx, spot in enumerate(lane_row):
                if spot == self.SYMBOLS['EMPTY']:
                    # Check stop sign logic
                    if spot_idx == 1 and vehicle['type'] == 'AV-C':
                        continue  # Autonomous car stops at stop sign
                    
                    if spot_idx == 1 and vehicle['type'] == 'H':
                        # Human driver might proceed
                        if random.choice([True, False]):
                            self.lane[lane_idx][spot_idx] = vehicle['symbol']
                            return f"🚦 {vehicle['id']} proceeded through stop sign"
                    
                    if spot_idx != 1:
                        self.lane[lane_idx][spot_idx] = vehicle['symbol']
                        return f"🅿️ {vehicle['id']} parked successfully"
        
        return f"⏳ {vehicle['id']} waiting to park"

    def remove_vehicle(self):
        # Randomly remove a vehicle
        lane_idx = random.randint(0, len(self.lane) - 1)
        for spot_idx, spot in enumerate(self.lane[lane_idx]):
            if spot in [self.SYMBOLS['AV-C'], self.SYMBOLS['AV-T'], self.SYMBOLS['H']]:
                self.lane[lane_idx][spot_idx] = self.SYMBOLS['EMPTY']
                return f"🚪 Vehicle left the lane"
        return "🚫 No vehicles to remove"

    def display(self):
        print("\n🛣️ Lane Construction Scenario 🚧")
        print("=" * 40)
        
        for lane_idx, lane_row in enumerate(self.lane):
            print(f"Lane {lane_idx + 1}: {' '.join(lane_row)}")
            
            # Highlight special lane features
            features = []
            if 1 in lane_row:
                features.append("🛑 Stop Sign")
            if self.SYMBOLS['P'] in lane_row:
                features.append("🚧 Partially Open Lane")
            
            if features:
                print("Features:", ", ".join(features))
        
        print("=" * 40)

def main():
    # Set up file output
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    output_filename = "lane_construction_symbol_output.txt"
    output_filepath = os.path.join(script_dir, output_filename)

    # Redirect output
    original_stdout = sys.stdout
    with open(output_filepath, 'w') as f:
        sys.stdout = f

        simulator = LaneConstructionSimulator()

        for _ in range(15):
            action = random.choice(['park', 'leave', 'both'])
            
            if action in ['park', 'both']:
                new_vehicle = simulator.generate_vehicle()
                result = simulator.place_vehicle(new_vehicle)
                print(result)

            if action in ['leave', 'both']:
                leave_result = simulator.remove_vehicle()
                print(leave_result)
            
            simulator.display()
            time.sleep(1)

    # Restore standard output
    sys.stdout = original_stdout
    print(f"Simulation output saved to {output_filepath}")

if __name__ == "__main__":
    main()