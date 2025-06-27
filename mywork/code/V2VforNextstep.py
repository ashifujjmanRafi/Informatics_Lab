import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Any
import random
import time
import math

@dataclass
class VehicleStatus:
    # Comprehensive vehicle status data structure for human crossing scenario
    vehicle_id: str
    timestamp: float
    
    # Obstacle Detection
    obstacle_presence: bool
    obstacle_type: str
    obstacle_proximity: float
    # 0-30 meters
    
    # Traffic Conditions
    traffic_density: str
    # light, moderate, heavy
    road_conditions: str
    # normal, wet, construction, etc.
    lane_position: str
    # same_lane, opposite_lane, adjacent_left, adjacent_right
    
    # Vehicle Dynamics
    current_speed: float
    direction: str
    # forward, backward, stationary, turning
    
    # Intended Action
    intended_action: str
    # emergency_brake, slow_down, maintain_speed, change_lane, stop
    
    # Position for distance calculation
    x_coordinate: float
    y_coordinate: float
    
    # Emergency status
    emergency_status: bool
    human_detected: bool

class V2VCommunicationSystem:
    def __init__(self, communication_radius: float = 100.0):
        self.communication_radius = communication_radius
        self.vehicles = {}

    def add_vehicle(self, vehicle_id: str, x: float, y: float):
        # Add a vehicle to the communication system
        self.vehicles[vehicle_id] = {
            'position': (x, y),
            'status': None
        }

    def calculate_distance(self, vehicle1_id: str, vehicle2_id: str) -> float:
        # Calculate distance between two vehicles
        pos1 = self.vehicles[vehicle1_id]['position']
        pos2 = self.vehicles[vehicle2_id]['position']
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def get_nearby_vehicles(self, vehicle_id: str) -> List[str]:
        # Find nearby vehicles within communication radius
        nearby_vehicles = []
        for other_id in self.vehicles.keys():
            if other_id != vehicle_id:
                distance = self.calculate_distance(vehicle_id, other_id)
                if distance <= self.communication_radius:
                    nearby_vehicles.append(other_id)
        return nearby_vehicles

class AV2CommunicationAgent:
    def __init__(self, v2v_system: V2VCommunicationSystem):
        self.vehicle_id = "AV2"
        # Following autonomous vehicle
        self.v2v_system = v2v_system
        
        # Position AV2 at (15, 10) - following behind AV1
        self.v2v_system.add_vehicle(self.vehicle_id, 15, 10)
        
        # Tracking received statuses
        self.received_statuses = {}
        self.nearby_vehicles = []
        
        # Open output file for writing
        self.output_file = open("V2VforNextstep.txt", "w")

    def write_to_file(self, message):
        # print(message)  # Commented out to prevent terminal output
        self.output_file.write(message + "\n")
        self.output_file.flush()

    def send_own_status(self):
        # Generate and send AV2's own status when detecting emergency situation
        self.write_to_file("\n--- AV2 Communication Agent: EMERGENCY - Human Crossing Detected ---")
        
        # Scan for nearby vehicles
        self.nearby_vehicles = self.v2v_system.get_nearby_vehicles(self.vehicle_id)
        self.write_to_file(f"Broadcasting to Nearby Vehicles: {self.nearby_vehicles}")
        
        # Create emergency status for AV2 (following vehicle)
        av2_status = VehicleStatus(
            vehicle_id="AV2",
            timestamp=time.time(),
            
            # Obstacle Detection - Human suddenly crossing
            obstacle_presence=True,
            obstacle_type="human_pedestrian",
            obstacle_proximity=8.5,
            # Human is very close
            
            # Traffic Conditions
            traffic_density="moderate",
            road_conditions="normal",
            lane_position="same_lane",
            
            # Vehicle Dynamics - Emergency response
            current_speed=25.0,
            # Reducing speed
            direction="forward",
            
            # Intended Action - Emergency braking
            intended_action="emergency_brake",
            
            # Position
            x_coordinate=15,
            y_coordinate=10,
            
            # Emergency flags
            emergency_status=True,
            human_detected=True
        )
        
        # Store status in V2V system
        self.v2v_system.vehicles[self.vehicle_id]['status'] = asdict(av2_status)
        
        self.write_to_file("AV2 Status Details:")
        self.write_to_file(f" Vehicle ID: {av2_status.vehicle_id}")
        self.write_to_file(f" EMERGENCY STATUS: {av2_status.emergency_status}")
        self.write_to_file(f" Human Detected: {av2_status.human_detected}")
        self.write_to_file(f" Obstacle Type: {av2_status.obstacle_type}")
        self.write_to_file(f" Human Proximity: {av2_status.obstacle_proximity} meters")
        self.write_to_file(f" Current Speed: {av2_status.current_speed} km/h")
        self.write_to_file(f" Intended Action: {av2_status.intended_action}")
        self.write_to_file(f" Lane Position: {av2_status.lane_position}")
        
        return av2_status

    def receive_vehicle_status(self, sender_vehicle_id: str):
        # Receive status from another vehicle in the emergency scenario
        self.write_to_file(f"\n--- AV2 Communication Agent: Receiving Status from {sender_vehicle_id} ---")
        
        # Simulate receiving status from the sender vehicle
        sender_status = self.v2v_system.vehicles[sender_vehicle_id]['status']
        
        self.write_to_file("Received Status Details:")
        self.write_to_file(f" Vehicle ID: {sender_status['vehicle_id']}")
        self.write_to_file(f" Emergency Status: {sender_status.get('emergency_status', False)}")
        self.write_to_file(f" Human Detected: {sender_status.get('human_detected', False)}")
        self.write_to_file(f" Obstacle Presence: {sender_status['obstacle_presence']}")
        self.write_to_file(f" Obstacle Type: {sender_status.get('obstacle_type', 'N/A')}")
        self.write_to_file(f" Obstacle Proximity: {sender_status['obstacle_proximity']} meters")
        self.write_to_file(f" Current Speed: {sender_status['current_speed']} km/h")
        self.write_to_file(f" Intended Action: {sender_status['intended_action']}")
        self.write_to_file(f" Lane Position: {sender_status['lane_position']}")
        
        # Store received status
        self.received_statuses[sender_vehicle_id] = sender_status

    def close_file(self):
        # Close the output file
        self.output_file.close()

def simulate_human_crossing_scenario():
    # Simulate V2V communication when human suddenly crosses road
    # Scenario: AV1 suddenly encounters human, AV2 is following, AV3 and AV4 in different lanes
    # Create V2V communication system with larger radius for emergency
    v2v_system = V2VCommunicationSystem(communication_radius=100.0)
    
    # Create vehicle positions
    # AV1: Leading vehicle that first encounters human at (10, 10)
    v2v_system.add_vehicle("AV1", 10, 10)
    
    # AV3: Approaching from adjacent left lane at (8, 15)
    v2v_system.add_vehicle("AV3", 8, 15)
    
    # AV4: Approaching from opposite direction at (10, 25)
    v2v_system.add_vehicle("AV4", 10, 25)
    
    # AV5: Following AV3 in adjacent left lane at (8, 20)
    v2v_system.add_vehicle("AV5", 8, 20)
    
    # AV6: Following AV3 in adjacent left lane at (8, 25)
    v2v_system.add_vehicle("AV6", 8, 25)
    
    # AV7: Following AV3 in adjacent left lane at (8, 30)
    v2v_system.add_vehicle("AV7", 8, 30)
    
    # Create AV2's Communication Agent (following vehicle perspective)
    av2_comm = AV2CommunicationAgent(v2v_system)
    
    # AV2 detects emergency and sends its status
    av2_status = av2_comm.send_own_status()
    
    # Simulate statuses from other vehicles
    
    # AV1 Status: Leading vehicle with direct human encounter
    v2v_system.vehicles["AV1"]['status'] = {
        'vehicle_id': "AV1",
        'timestamp': time.time(),
        'obstacle_presence': True,
        'obstacle_type': "human_pedestrian",
        'obstacle_proximity': 23.0,
        # Updated to 23 meters
        'traffic_density': "moderate",
        'road_conditions': "normal",
        'lane_position': "same_lane",
        'current_speed': 0.0,
        # Emergency stopped
        'direction': "stationary",
        'intended_action': "emergency_brake",
        'x_coordinate': 10,
        'y_coordinate': 10,
        'emergency_status': True,
        'human_detected': True
    }
    
    # AV3 Status: Adjacent lane vehicle
    v2v_system.vehicles["AV3"]['status'] = {
        'vehicle_id': "AV3",
        'timestamp': time.time(),
        'obstacle_presence': True,
        'obstacle_type': "human_pedestrian",
        'obstacle_proximity': 12.0,
        # Updated to 12 meters
        'traffic_density': "moderate",
        'road_conditions': "normal",
        'lane_position': "adjacent_left",
        'current_speed': 15.0,
        # Slowing down
        'direction': "forward",
        'intended_action': "slow_down",
        'x_coordinate': 8,
        'y_coordinate': 15,
        'emergency_status': False,
        'human_detected': True
    }
    
    # AV4 Status: Opposite direction vehicle
    v2v_system.vehicles["AV4"]['status'] = {
        'vehicle_id': "AV4",
        'timestamp': time.time(),
        'obstacle_presence': True,
        'obstacle_type': "human_pedestrian",
        'obstacle_proximity': 18.7,
        'traffic_density': "light",
        'road_conditions': "normal",
        'lane_position': "opposite_lane",
        'current_speed': 20.0,
        # Reducing speed
        'direction': "forward",
        'intended_action': "slow_down",
        'x_coordinate': 10,
        'y_coordinate': 25,
        'emergency_status': False,
        'human_detected': True
    }
    
    # AV5 Status: Following AV3 in adjacent left lane
    v2v_system.vehicles["AV5"]['status'] = {
        'vehicle_id': "AV5",
        'timestamp': time.time(),
        'obstacle_presence': True,
        'obstacle_type': "human_pedestrian",
        'obstacle_proximity': 16.5,
        'traffic_density': "moderate",
        'road_conditions': "normal",
        'lane_position': "adjacent_left",
        'current_speed': 12.0,
        'direction': "forward",
        'intended_action': "slow_down",
        'x_coordinate': 8,
        'y_coordinate': 20,
        'emergency_status': False,
        'human_detected': True
    }
    
    # AV6 Status: Following AV3 in adjacent left lane
    v2v_system.vehicles["AV6"]['status'] = {
        'vehicle_id': "AV6",
        'timestamp': time.time(),
        'obstacle_presence': True,
        'obstacle_type': "human_pedestrian",
        'obstacle_proximity': 21.2,
        'traffic_density': "moderate",
        'road_conditions': "normal",
        'lane_position': "adjacent_left",
        'current_speed': 10.0,
        'direction': "forward",
        'intended_action': "slow_down",
        'x_coordinate': 8,
        'y_coordinate': 25,
        'emergency_status': False,
        'human_detected': True
    }
    
    # AV7 Status: Following AV3 in adjacent left lane
    v2v_system.vehicles["AV7"]['status'] = {
        'vehicle_id': "AV7",
        'timestamp': time.time(),
        'obstacle_presence': True,
        'obstacle_type': "human_pedestrian",
        'obstacle_proximity': 25.8,
        'traffic_density': "moderate",
        'road_conditions': "normal",
        'lane_position': "adjacent_left",
        'current_speed': 8.0,
        'direction': "forward",
        'intended_action': "slow_down",
        'x_coordinate': 8,
        'y_coordinate': 30,
        'emergency_status': False,
        'human_detected': True
    }
    
    # AV2 receives statuses from all other vehicles
    av2_comm.receive_vehicle_status("AV1")
    av2_comm.receive_vehicle_status("AV3")
    av2_comm.receive_vehicle_status("AV4")
    av2_comm.receive_vehicle_status("AV5")
    av2_comm.receive_vehicle_status("AV6")
    av2_comm.receive_vehicle_status("AV7")
    
    # Write simulation completion message
    av2_comm.write_to_file("\n--- Human Crossing Emergency V2V Communication Completed ---")
    
    # Close the output file
    av2_comm.close_file()

# Run the simulation
if __name__ == "__main__":
    simulate_human_crossing_scenario()