import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Any
import random
import time
import math

@dataclass
class VehicleStatus:
    """
    Comprehensive vehicle status data structure
    """
    vehicle_id: str
    timestamp: float
    
    # Obstacle Detection
    obstacle_presence: bool
    obstacle_type: str
    obstacle_proximity: float  # 0-15 meters
    
    # Traffic Conditions
    traffic_density: str  # light, moderate, heavy
    road_conditions: str  # normal, wet, construction, etc.
    
    # Vehicle Dynamics
    current_speed: float
    direction: str  # forward, backward, stationary
    
    # Intended Action
    intended_action: str  # forward, stop, turn_left, turn_right
    
    # Position for distance calculation
    x_coordinate: float
    y_coordinate: float

class V2VCommunicationSystem:
    def __init__(self, communication_radius: float = 50.0):
        self.communication_radius = communication_radius
        self.vehicles = {}

    def add_vehicle(self, vehicle_id: str, x: float, y: float):
        """
        Add a vehicle to the communication system
        """
        self.vehicles[vehicle_id] = {
            'position': (x, y),
            'status': None
        }

    def calculate_distance(self, vehicle1_id: str, vehicle2_id: str) -> float:
        """
        Calculate distance between two vehicles
        """
        pos1 = self.vehicles[vehicle1_id]['position']
        pos2 = self.vehicles[vehicle2_id]['position']
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def get_nearby_vehicles(self, vehicle_id: str) -> List[str]:
        """
        Find nearby vehicles within communication radius
        """
        nearby_vehicles = []
        for other_id in self.vehicles.keys():
            if other_id != vehicle_id:
                distance = self.calculate_distance(vehicle_id, other_id)
                if distance <= self.communication_radius:
                    nearby_vehicles.append(other_id)
        return nearby_vehicles

class Vehicle2CommunicationAgent:
    def __init__(self, v2v_system: V2VCommunicationSystem):
        self.vehicle_id = "002"  # Vehicle 2 (Sender)
        self.v2v_system = v2v_system
        
        # Position Vehicle 2 at (10, 10)
        self.v2v_system.add_vehicle(self.vehicle_id, 10, 10)
        
        # Tracking received statuses
        self.received_statuses = {}
        self.nearby_vehicles = []
        
        # Open output file for writing
        self.output_file = open("v2v_communication_output.txt", "w")

    def write_to_file(self, message):
        # print(message)
        self.output_file.write(message + "\n")
        self.output_file.flush()

    def send_own_status(self):
        """
        Generate and send Vehicle 2's own status with specific details
        """
        self.write_to_file("\n--- Vehicle 2 Communication Agent: Sending Own Status ---")
        
        # Scan for nearby vehicles
        self.nearby_vehicles = self.v2v_system.get_nearby_vehicles(self.vehicle_id)
        self.write_to_file(f"Nearby Vehicles: {self.nearby_vehicles}")
        
        # Create status with specific requirements
        vehicle_2_status = VehicleStatus(
            vehicle_id="002",
            timestamp=time.time(),
            
            # Obstacle Detection with stop sign
            obstacle_presence=True,
            obstacle_type="stop_sign",
            obstacle_proximity=13.123529423503923,
            
            # Traffic Conditions
            traffic_density="heavy",
            road_conditions=random.choice(['normal', 'wet', 'construction', 'icy']),
            
            # Vehicle Dynamics
            current_speed=random.uniform(0, 60),
            direction='forward',
            
            # Intended Action
            intended_action='stop',
            
            # Position
            x_coordinate=10,
            y_coordinate=10
        )
        
        # Store status in V2V system
        self.v2v_system.vehicles[self.vehicle_id]['status'] = asdict(vehicle_2_status)
        
        self.write_to_file("Vehicle 2 Status Details:")
        self.write_to_file(f" Vehicle ID: {vehicle_2_status.vehicle_id}")
        self.write_to_file(f" Obstacle Presence: {vehicle_2_status.obstacle_presence}")
        self.write_to_file(f" Obstacle Type: {vehicle_2_status.obstacle_type}")
        self.write_to_file(f" Obstacle Proximity: {vehicle_2_status.obstacle_proximity} meters")
        self.write_to_file(f" Traffic Density: {vehicle_2_status.traffic_density}")
        self.write_to_file(f" Intended Action: {vehicle_2_status.intended_action}")
        
        return vehicle_2_status

    def receive_vehicle_status(self, sender_vehicle_id: str):
        """
        Receive status from another vehicle
        """
        self.write_to_file(f"\n--- Vehicle 2 Communication Agent: Receiving Status from Vehicle {sender_vehicle_id} ---")
        
        # Simulate receiving status from the sender vehicle
        sender_status = self.v2v_system.vehicles[sender_vehicle_id]['status']
        
        self.write_to_file("Received Status Details:")
        self.write_to_file(f" Vehicle ID: {sender_status['vehicle_id']}")
        self.write_to_file(f" Obstacle Presence: {sender_status['obstacle_presence']}")
        self.write_to_file(f" Obstacle Type: {sender_status.get('obstacle_type', 'N/A')}")
        self.write_to_file(f" Obstacle Proximity: {sender_status['obstacle_proximity']} meters")
        self.write_to_file(f" Traffic Density: {sender_status['traffic_density']}")
        self.write_to_file(f" Intended Action: {sender_status['intended_action']}")
        
        # Store received status
        self.received_statuses[sender_vehicle_id] = sender_status

    def close_file(self):
        """
        Close the output file
        """
        self.output_file.close()

def simulate_v2v_communication():
    """
    Simulate V2V communication from Vehicle 2's perspective
    """
    # Create V2V communication system
    v2v_system = V2VCommunicationSystem(communication_radius=50.0)
    
    # Create other vehicles
    v2v_system.add_vehicle("001", 5, 5)   # Vehicle 1 close to Vehicle 2
    v2v_system.add_vehicle("003", 20, 20)  # Vehicle 3 at (20, 20)
    
    # Create Vehicle 2's Communication Agent
    vehicle_2_comm = Vehicle2CommunicationAgent(v2v_system)
    
    # Vehicle 2 sends its own status
    vehicle_2_status = vehicle_2_comm.send_own_status()
    
    # Simulate sending status to other vehicles
    # (In a real system, this would be a broadcast)
    v2v_system.vehicles["001"]['status'] = {
        'vehicle_id': "001",
        'timestamp': time.time(),
        'obstacle_presence': random.choice([True, False]),
        'obstacle_type': random.choice(['traffic_light', 'pedestrian', 'none']),
        'obstacle_proximity': random.uniform(0, 15),
        'traffic_density': random.choice(['light', 'moderate', 'heavy']),
        'road_conditions': random.choice(['normal', 'wet', 'construction', 'icy']),
        'current_speed': random.uniform(0, 120),
        'direction': random.choice(['forward', 'stationary']),
        'intended_action': random.choice(['forward', 'stop', 'turn_left', 'turn_right']),
        'x_coordinate': 5,
        'y_coordinate': 5
    }
    
    v2v_system.vehicles["003"]['status'] = {
        'vehicle_id': "003",
        'timestamp': time.time(),
        'obstacle_presence': random.choice([True, False]),
        'obstacle_type': random.choice(['traffic_light', 'pedestrian', 'none']),
        'obstacle_proximity': random.uniform(0, 15),
        'traffic_density': random.choice(['light', 'moderate', 'heavy']),
        'road_conditions': random.choice(['normal', 'wet', 'construction', 'icy']),
        'current_speed': random.uniform(0, 120),
        'direction': random.choice(['forward', 'stationary']),
        'intended_action': random.choice(['forward', 'stop', 'turn_left', 'turn_right']),
        'x_coordinate': 20,
        'y_coordinate': 20
    }
    
    # Vehicle 2 receives statuses from Vehicle 1 and Vehicle 3
    vehicle_2_comm.receive_vehicle_status("001")
    vehicle_2_comm.receive_vehicle_status("003")
    
    # Write simulation completion message
    vehicle_2_comm.write_to_file("\n-V2V Communication Simulation Completed-")
    
    # Close the output file
    vehicle_2_comm.close_file()

# Run the simulation
if __name__ == "__main__":
    simulate_v2v_communication()