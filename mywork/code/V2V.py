import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Any
import random
import time
import math

@dataclass
class VehicleStatus:
    """
    Comprehensive vehicle status data structure for Vehicle 2
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
    def __init__(self, communication_radius: float = 15.0):
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
        Find vehicles within communication radius
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
        self.vehicle_id = "002"  # Explicitly Vehicle 2
        self.v2v_system = v2v_system
        # Position Vehicle 2 at (10, 10)
        self.v2v_system.add_vehicle(self.vehicle_id, 10, 10)
        
        # Nearby vehicles tracking
        self.nearby_vehicles = []
        self.received_statuses = {}

    def scan_nearby_vehicles(self):
        """
        Scan for vehicles within communication radius
        """
        print("\n--- Vehicle 2 Communication Agent: Scanning Nearby Vehicles ---")
        self.nearby_vehicles = self.v2v_system.get_nearby_vehicles(self.vehicle_id)
        print(f"Nearby Vehicles: {self.nearby_vehicles}")
        return self.nearby_vehicles

    def receive_vehicle_status(self, sender_vehicle_id: str):
        """
        Receive status from a nearby vehicle
        """
        # Simulate vehicle status for Vehicle 1 for demonstration
        sender_status = {
            'vehicle_id': sender_vehicle_id,
            'timestamp': time.time(),
            'obstacle_presence': random.choice([True, False]),
            'obstacle_proximity': random.uniform(0, 15),
            'traffic_density': random.choice(['light', 'moderate', 'heavy']),
            'road_conditions': random.choice(['normal', 'wet', 'construction', 'icy']),
            'current_speed': random.uniform(0, 120),
            'direction': random.choice(['forward', 'stationary']),
            'intended_action': random.choice(['forward', 'stop', 'turn_left', 'turn_right']),
            'x_coordinate': 0,
            'y_coordinate': 0
        }
        
        print(f"\n--- Vehicle 2 Communication Agent: Receiving Status from Vehicle {sender_vehicle_id} ---")
        
        # Process received status
        received_status = VehicleStatus(
            vehicle_id=sender_vehicle_id,
            timestamp=sender_status['timestamp'],
            obstacle_presence=sender_status['obstacle_presence'],
            obstacle_proximity=sender_status['obstacle_proximity'],
            traffic_density=sender_status['traffic_density'],
            road_conditions=sender_status['road_conditions'],
            current_speed=sender_status['current_speed'],
            direction=sender_status['direction'],
            intended_action=sender_status['intended_action'],
            x_coordinate=sender_status['x_coordinate'],
            y_coordinate=sender_status['y_coordinate']
        )
        
        # Store received status
        self.received_statuses[sender_vehicle_id] = asdict(received_status)
        
        print("Status Details:")
        print(f"  Obstacle Presence: {received_status.obstacle_presence}")
        print(f"  Obstacle Proximity: {received_status.obstacle_proximity} meters")
        print(f"  Traffic Density: {received_status.traffic_density}")
        print(f"  Intended Action: {received_status.intended_action}")

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
        
        print("Own Status Details:")
        print(f"  Obstacle Presence: {vehicle_2_status.obstacle_presence}")
        print(f"  Obstacle Proximity: {vehicle_2_status.obstacle_proximity} meters")
        print(f"  Traffic Density: {vehicle_2_status.traffic_density}")
        print(f"  Intended Action: {vehicle_2_status.intended_action}")
        
        return asdict(vehicle_2_status)

def simulate_v2v_communication():
    """
    Simulate V2V communication from Vehicle 2's perspective
    """
    # Create V2V communication system with 15m radius
    v2v_system = V2VCommunicationSystem(communication_radius=15.0)
    
    # Create other vehicles
    v2v_system.add_vehicle("001", 0, 0)  # Vehicle 1 near origin
    v2v_system.add_vehicle("003", 20, 20)  # Vehicle 3 far away
    
    # Create Vehicle 2's Communication Agent
    vehicle_2_comm = Vehicle2CommunicationAgent(v2v_system)
    
    # Scan for nearby vehicles
    nearby_vehicles = vehicle_2_comm.scan_nearby_vehicles()
    
    # Simulate receiving status from nearby Vehicle 1
    if "001" in nearby_vehicles:
        vehicle_2_comm.receive_vehicle_status("001")
    
    # Send Vehicle 2's own status
    vehicle_2_status = vehicle_2_comm.send_own_status()

# Run the simulation
if __name__ == "__main__":
    simulate_v2v_communication()