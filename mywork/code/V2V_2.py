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

class Vehicle2CommunicationAgent:
    def __init__(self, v2v_system: V2VCommunicationSystem):
        self.vehicle_id = "002"  # Vehicle 2 (Sender)
        self.v2v_system = v2v_system
        
        # Position Vehicle 2 at (10, 10)
        self.v2v_system.add_vehicle(self.vehicle_id, 10, 10)
        
        # Tracking received statuses
        self.received_statuses = {}

    def send_own_status(self):
        """
        Generate and send Vehicle 2's own status
        """
        print("\n--- Vehicle 2 Communication Agent: Sending Own Status ---")
        vehicle_2_status = VehicleStatus(
            vehicle_id=self.vehicle_id,
            timestamp=time.time(),
            
            # Obstacle Detection
            obstacle_presence=random.choice([True, False]),
            obstacle_proximity=random.uniform(0, 15),
            
            # Traffic Conditions
            traffic_density=random.choice(['light', 'moderate', 'heavy']),
            road_conditions=random.choice(['normal', 'wet', 'construction', 'icy']),
            
            # Vehicle Dynamics
            current_speed=random.uniform(0, 120),
            direction=random.choice(['forward', 'stationary']),
            
            # Intended Action
            intended_action=random.choice(['forward', 'stop', 'turn_left', 'turn_right']),
            
            # Position
            x_coordinate=10,
            y_coordinate=10
        )
        
        # Store status in V2V system
        self.v2v_system.vehicles[self.vehicle_id]['status'] = asdict(vehicle_2_status)
        
        print("Vehicle 2 Status Details:")
        print(f"  Vehicle ID: {vehicle_2_status.vehicle_id}")
        print(f"  Obstacle Presence: {vehicle_2_status.obstacle_presence}")
        print(f"  Obstacle Proximity: {vehicle_2_status.obstacle_proximity} meters")
        print(f"  Traffic Density: {vehicle_2_status.traffic_density}")
        print(f"  Intended Action: {vehicle_2_status.intended_action}")
        
        return vehicle_2_status

    def receive_vehicle_status(self, sender_vehicle_id: str):
        """
        Receive status from another vehicle
        """
        print(f"\n--- Vehicle 2 Communication Agent: Receiving Status from Vehicle {sender_vehicle_id} ---")
        
        # Simulate receiving status from the sender vehicle
        sender_status = self.v2v_system.vehicles[sender_vehicle_id]['status']
        
        print("Received Status Details:")
        print(f"  Vehicle ID: {sender_status['vehicle_id']}")
        print(f"  Obstacle Presence: {sender_status['obstacle_presence']}")
        print(f"  Obstacle Proximity: {sender_status['obstacle_proximity']} meters")
        print(f"  Traffic Density: {sender_status['traffic_density']}")
        print(f"  Intended Action: {sender_status['intended_action']}")
        
        # Store received status
        self.received_statuses[sender_vehicle_id] = sender_status

def simulate_v2v_communication():
    """
    Simulate V2V communication from Vehicle 2's perspective
    """
    # Create V2V communication system
    v2v_system = V2VCommunicationSystem(communication_radius=50.0)
    
    # Create other vehicles
    v2v_system.add_vehicle("003", 20, 20)  # Vehicle 3 at (20, 20)
    v2v_system.add_vehicle("004", 15, 15)  # Vehicle 4 at (15, 15)
    
    # Create Vehicle 2's Communication Agent
    vehicle_2_comm = Vehicle2CommunicationAgent(v2v_system)
    
    # Vehicle 2 sends its own status
    vehicle_2_status = vehicle_2_comm.send_own_status()
    
    # Simulate sending status to other vehicles
    # (In a real system, this would be a broadcast)
    v2v_system.vehicles["003"]['status'] = {
        'vehicle_id': "003",
        'timestamp': time.time(),
        'obstacle_presence': random.choice([True, False]),
        'obstacle_proximity': random.uniform(0, 15),
        'traffic_density': random.choice(['light', 'moderate', 'heavy']),
        'road_conditions': random.choice(['normal', 'wet', 'construction', 'icy']),
        'current_speed': random.uniform(0, 120),
        'direction': random.choice(['forward', 'stationary']),
        'intended_action': random.choice(['forward', 'stop', 'turn_left', 'turn_right']),
        'x_coordinate': 20,
        'y_coordinate': 20
    }
    
    v2v_system.vehicles["004"]['status'] = {
        'vehicle_id': "004",
        'timestamp': time.time(),
        'obstacle_presence': random.choice([True, False]),
        'obstacle_proximity': random.uniform(0, 15),
        'traffic_density': random.choice(['light', 'moderate', 'heavy']),
        'road_conditions': random.choice(['normal', 'wet', 'construction', 'icy']),
        'current_speed': random.uniform(0, 120),
        'direction': random.choice(['forward', 'stationary']),
        'intended_action': random.choice(['forward', 'stop', 'turn_left', 'turn_right']),
        'x_coordinate': 15,
        'y_coordinate': 15
    }
    
    # Vehicle 2 receives statuses from Vehicle 3 and Vehicle 4
    vehicle_2_comm.receive_vehicle_status("003")
    vehicle_2_comm.receive_vehicle_status("004")

# Run the simulation
if __name__ == "__main__":
    simulate_v2v_communication()