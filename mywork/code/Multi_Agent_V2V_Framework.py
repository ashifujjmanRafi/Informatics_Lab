import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Any
import random
import time

@dataclass
class VehicleStatus:
    """
    Comprehensive vehicle status data structure
    """
    vehicle_id: str
    timestamp: float
    
    # Obstacle Detection
    obstacle_detected: bool
    obstacle_type: str
    obstacle_distance: float
    obstacle_location: str
    
    # Traffic Conditions
    traffic_density: str  # light, moderate, heavy
    road_conditions: str  # normal, wet, construction, etc.
    
    # Vehicle Dynamics
    current_speed: float
    direction: str  # forward, backward, stationary
    
    # Intended Action
    intended_action: str  # forward, stop, turn_left, turn_right

class CommunicationAgent:
    def __init__(self, vehicle_id: str):
        self.vehicle_id = vehicle_id
        self.status_history = []

    def generate_vehicle_status(self) -> VehicleStatus:
        """
        Simulate generation of vehicle status
        In a real system, this would come from actual vehicle sensors
        """
        return VehicleStatus(
            vehicle_id=self.vehicle_id,
            timestamp=time.time(),
            
            # Obstacle Detection
            obstacle_detected=random.choice([True, False]),
            obstacle_type=random.choice(['pedestrian', 'vehicle', 'construction_cone', 'none']),
            obstacle_distance=random.uniform(0, 100),
            obstacle_location=random.choice(['left', 'right', 'center', 'none']),
            
            # Traffic Conditions
            traffic_density=random.choice(['light', 'moderate', 'heavy']),
            road_conditions=random.choice(['normal', 'wet', 'construction', 'icy']),
            
            # Vehicle Dynamics
            current_speed=random.uniform(0, 120),
            direction=random.choice(['forward', 'stationary']),
            
            # Intended Action
            intended_action=random.choice(['forward', 'stop', 'turn_left', 'turn_right'])
        )

    def broadcast_status(self) -> Dict[str, Any]:
        """
        Broadcast current vehicle status
        """
        status = self.generate_vehicle_status()
        self.status_history.append(status)
        return asdict(status)

class DecisionAgent:
    def __init__(self, vehicle_id: str, communication_agent: CommunicationAgent):
        self.vehicle_id = vehicle_id
        self.communication_agent = communication_agent
        self.nearby_vehicles_status = {}

    def process_vehicle_status(self, status: Dict[str, Any]):
        """
        Process and store status of nearby vehicles
        """
        # Store status based on vehicle ID
        self.nearby_vehicles_status[status['vehicle_id']] = status

    def analyze_surrounding_status(self):
        """
        Analyze statuses of nearby vehicles
        """
        print("\n--- Vehicle Status Analysis ---")
        for vehicle_id, status in self.nearby_vehicles_status.items():
            print(f"\nVehicle ID: {vehicle_id}")
            print("Obstacle Detection:")
            print(f"  Obstacle: {status['obstacle_detected']}")
            print(f"  Type: {status['obstacle_type']}")
            print(f"  Distance: {status['obstacle_distance']} meters")
            print(f"  Location: {status['obstacle_location']}")
            
            print("\nTraffic Conditions:")
            print(f"  Density: {status['traffic_density']}")
            print(f"  Road Conditions: {status['road_conditions']}")
            
            print("\nVehicle Dynamics:")
            print(f"  Speed: {status['current_speed']} km/h")
            print(f"  Direction: {status['direction']}")
            
            print("\nIntended Action:")
            print(f"  Next Move: {status['intended_action']}")

def simulate_v2v_communication():
    """
    Simulate V2V communication between multiple vehicles
    """
    # Create multiple vehicles
    vehicles = [
        CommunicationAgent(f"vehicle_{i:03d}") 
        for i in range(3)
    ]
    
    # Create decision agents for each vehicle
    decision_agents = [
        DecisionAgent(vehicle.vehicle_id, vehicle) 
        for vehicle in vehicles
    ]
    
    # Simulate communication and status sharing
    for i, vehicle in enumerate(vehicles):
        # Broadcast status
        status = vehicle.broadcast_status()
        
        # Other decision agents process the status
        for decision_agent in decision_agents:
            if decision_agent.vehicle_id != vehicle.vehicle_id:
                decision_agent.process_vehicle_status(status)
    
    # Analyze surrounding vehicle statuses
    for decision_agent in decision_agents:
        decision_agent.analyze_surrounding_status()

# Run the simulation
simulate_v2v_communication()