import time
import math
import heapq
import plotly.graph_objects as go
import pandas as pd

# Simulated Tello Drone class
# All battery consumption values have been taken from test data.
class SimulatedTello:
    def __init__(self, battery_consumption):
        self.battery_percentage = 100
        self.battery_consumption = battery_consumption
        self.position = (0,0,0,0)

    def takeoff(self):
        print("Drone is taking off.")
        self.battery_percentage -= self.battery_consumption['takeoff']

    def land(self):
        print("Drone is landing.")
        self.battery_percentage -= self.battery_consumption['land']

    # Battery consumption of 'up' hardcoded as it wasn't properly tested.
    def move_up(self):
        print("Drone is moving up.")
        self.position = (self.position[0], self.position[1], self.position[2] + 1, self.position[3])
        self.battery_percentage -= 1.01 

    def move_down(self):
        print("Drone is moving down.")
        self.position = (self.position[0], self.position[1], self.position[2] - 1, self.position[3])
        self.battery_percentage -= self.battery_consumption['down']

    def move_forward(self):
        print("Drone is moving forward.")
        self.position = (self.position[0] + 1, self.position[1], self.position[2], self.position[3])
        self.battery_percentage -= self.battery_consumption['forward']

    def move_backward(self):
        print("Drone is moving backward.")
        self.position = (self.position[0] - 1, self.position[1], self.position[2], self.position[3])
        self.battery_percentage -= self.battery_consumption['back']

    def move_left(self):
        print("Drone is moving left.")
        self.position = (self.position[0], self.position[1] - 1, self.position[2], self.position[3])
        self.battery_percentage -= self.battery_consumption['left']

    def move_right(self):
        print("Drone is moving right.")
        self.position = (self.position[0], self.position[1] + 1, self.position[2], self.position[3])
        self.battery_percentage -= self.battery_consumption['right']

    def rotate_clockwise(self):
        print("Drone is rotating clockwise.")
        self.position = (self.position[0], self.position[1], self.position[2], self.position[3] + 1)
        self.battery_percentage -= self.battery_consumption['cw']

    def rotate_counterclockwise(self):
        print("Drone is rotating counterclockwise.")
        self.position = (self.position[0], self.position[1], self.position[2], self.position[3] - 1)
        self.battery_percentage -= self.battery_consumption['ccw']

    def flip(self):
        print("Drone is flipping forward.")
        self.battery_percentage -= self.battery_consumption['flip']

    def print_battery_status(self):
        print(f"Battery Percentage: {self.battery_percentage}%")

    def print_available_commands(self):
        print("Available Commands:")
        print("takeoff, land, up, down, forward, back, left, right, cw, ccw, flip, exit")

def keyboard_control(drone):
    drone.print_available_commands()

    while True:
        command = input("Enter command: ").lower()

        if command == 'exit':
            break
        elif command == 'takeoff':
            drone.takeoff()
        elif command == 'land':
            drone.land()
        elif command == 'up':
            drone.move_up()
        elif command == 'down':
            drone.move_down()
        elif command == 'forward':
            drone.move_forward()
        elif command == 'back':
            drone.move_backward()
        elif command == 'left':
            drone.move_left()
        elif command == 'right':
            drone.move_right()
        elif command == 'cw':
            drone.rotate_clockwise()
        elif command == 'ccw':
            drone.rotate_counterclockwise()
        elif command == 'flip':
            drone.flip()
        else:
            print("Invalid command.")

        drone.print_battery_status()
        time.sleep(1)

# A star path planning algorithm for best path.
def heuristic_cost_estimate(start, goal):
    return abs(goal[0] - start[0]) + abs(goal[1] - start[1]) + abs(goal[2] - start[2]) + abs(goal[3] - start[3])

# Calculate the cost based on movement cost and battery consumption
def cost_function(move, command_battery):
    movement_cost = 1
    if move == 'up':
        battery_cost = 1.01
    else:
        battery_cost = command_battery[move]
    total_cost = movement_cost + battery_cost
    return total_cost

def astar_search(start, goal, drone, command_battery):
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, (0, start, []))

    while open_set:
        f_cost, current_position, path = heapq.heappop(open_set)

        if current_position == goal:
            return path

        if current_position in closed_set:
            continue

        closed_set.add(current_position)

        movements = ['up', 'down', 'forward', 'back', 'left', 'right', 'cw', 'ccw', 'flip']

        for action in movements:
            new_position = current_position + (action,)
            new_path = path + [action]
            g_cost = len(new_path)
            h_cost = heuristic_cost_estimate(new_position, goal)
            f_cost = g_cost + h_cost + cost_function(action, command_battery)
            heapq.heappush(open_set, (f_cost, new_position, new_path))

    return None

def get_destination_input():
    while True:
        try:
            x = int(input("Enter X coordinate for destination: "))
            y = int(input("Enter Y coordinate for destination: "))
            z = int(input("Enter Z coordinate for destination: "))
            bearing = int(input("Enter bearing for destination (set to 0): "))
            return x, y, z, bearing
        except ValueError:
            print("Invalid input. Please enter integers.")

# Plot best path.
def plot_path(path):
    if path:
        x_coords = [0]
        y_coords = [0]
        z_coords = [0]

        for action in path:
            if action == 'up':
                z_coords.append(z_coords[-1] + 1)
            elif action == 'down':
                z_coords.append(z_coords[-1] - 1)
            elif action == 'forward':
                x_coords.append(x_coords[-1] + 1)
            elif action == 'back':
                x_coords.append(x_coords[-1] - 1)
            elif action == 'left':
                y_coords.append(y_coords[-1] - 1)
            elif action == 'right':
                y_coords.append(y_coords[-1] + 1)

        fig = go.Figure(data=[go.Scatter3d(
            x=x_coords,
            y=y_coords,
            z=z_coords,
            mode='lines+markers',
            marker=dict(size=5),
            line=dict(color='blue', width=2)
        )])

        fig.update_layout(
            title="Drone Path",
            scene=dict(
                xaxis_title="X Coordinate",
                yaxis_title="Y Coordinate",
                zaxis_title="Z Coordinate",
            )
        )

        fig.show()
    else:
        print("No valid path found.")

def main():
    csv_file = './average_battery_consumption/average_battery_data.csv'
    df = pd.read_csv(csv_file)
    commands = ['back', 'ccw', 'cw', 'down', 'flip', 'forward', 'land', 'left', 'right', 'takeoff']
    command_battery = {cmd: df.loc[df['Command'] == cmd, 'Battery Consumption (%)'].iloc[0] for cmd in commands}
    
    simulated_drone = SimulatedTello(command_battery)

    print("Please input the destination coordinates for the drone:")
    destination = get_destination_input()

    start_position = (0, 0, 0, 0)
    path = astar_search(start_position, destination, simulated_drone, command_battery)
    
    plot_path(path)
    
    keyboard_control(simulated_drone)

if __name__ == "__main__":
    main()