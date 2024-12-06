import random
import random
import time
import sys
import os
from datetime import datetime
class ParkingLot:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.spots = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.waiting = []
        self.next_car_id = 1
        self.disabeledcars = []

    def park(self, car):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.spots[row][col] == ' ':
                    self.spots[row][col] = car
                    return True
        self.waiting.append(car)
        return False

    def leave(self):
        occupied_spots = [(row, col) for row in range(self.rows) for col in range(self.cols) if self.spots[row][col] != ' ']
        if occupied_spots:
            row, col = random.choice(occupied_spots)
            car = self.spots[row][col]
            self.spots[row][col] = ' '
            if car in self.disabeledcars:
                self.disabeledcars.remove(car)
            if self.waiting:
                self.park(self.waiting.pop(0))
            return car
        return None

    def display(self):
        print("┌" + "───────┬" * (self.cols - 1) + "───────┐")
        for row in range(self.rows):
            for _ in range(3):  # Three lines for each row of spots
                print("│", end="")
                for col in range(self.cols):
                    if self.spots[row][col] != ' ':
                        if _ == 0:
                            print(" ┌───┐ │", end="")
                        elif _ == 1:
                            print(f" │ {self.spots[row][col]:^2}│ │", end="")
                        else:
                            print(" └───┘ │", end="")
                    else:
                        print("       │", end="")
                print()
            if row < self.rows - 1:
                print("├" + "───────┴" * (self.cols - 1) + "───────┤")
                for _ in range(5):  # 5-line gap between rows
                    print("│" + " " * (8 * self.cols) + "│")
                print("├" + "───────┬" * (self.cols - 1) + "───────┤")
        print("└" + "───────┴" * (self.cols - 1) + "───────┘")
        
        if self.waiting:
            print("Waiting:", " ".join(map(str, self.waiting)))
        else:
            print("No cars waiting")
        print()
       # if self.car in self.prioritycars:
        #    self.prioritycars.remove(self.car)
        if self.disabeledcars:
            print("Disabeled person cars:", " ".join(map(str, self.disabeledcars)))
        else:
            print("No cars are disabeled persons")
        priority_waiting = [car for car in self.disabeledcars if car in self.waiting]
        if priority_waiting:
            print("Disabled person cars in waiting:", " ".join(map(str, priority_waiting)))
        else:
            print("No disabled person cars are waiting")
        print("=============================================================================================================")
    def generate_car_id(self):
        car_id = self.next_car_id
        choice=random.choice(['disabeled','disabeled', 'ordinary', 'ordinary', 'ordinary'])
        if choice in ['disabeled']:
            self.disabeledcars.append(car_id)
            #print("Disabeled generated", " ".join(map(str, self.prioritycars)))
        self.next_car_id += 1
        return car_id
    
def main():
    # Get the directory and name of the current script
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)

    # Create the output filename
    output_filename = "parkinglotsimulator_output.txt"

    # Create the full path for the output file
    output_filepath = os.path.join(script_dir, output_filename)

    # Redirect standard output to the file
    original_stdout = sys.stdout
    with open(output_filepath, 'w') as f:  # 'w' mode overwrites the file
        sys.stdout = f

        parking_lot = ParkingLot(2, 7)

        for _ in range(30):
            action = random.choice(['park', 'park', 'park', 'park', 'leave', 'both'])
            
            if action in ['park', 'both']:
                new_car = parking_lot.generate_car_id()
                if parking_lot.park(new_car):
                    print(f"Car {new_car} parked successfully.")
                else:
                    print(f"Car {new_car} is waiting to park.")

            if action in ['leave', 'both']:
                car = parking_lot.leave()
                if car:
                    print(f"Car {car} left the parking lot.")
                else:
                    print("No cars to leave.")
            parking_lot.display()
            time.sleep(1)

    # Restore the standard output
    sys.stdout = original_stdout
    print(f"Simulation output has been saved to {output_filepath}")

if __name__ == "__main__":
    main()