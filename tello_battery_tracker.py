import sys
import math
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox

# Simulated Tello Drone class
class SimulatedTello:
    def __init__(self, battery_consumption):
        self.battery_percentage = 100
        self.battery_consumption = battery_consumption
        self.destination = None
        self.landed = True
        self.position = (0, 0, 0)

    def takeoff(self):
        if self.landed:
            self.show_message("Drone is taking off.")
            self.battery_percentage -= self.battery_consumption['takeoff']
            self.landed = False
        else:
            self.show_message("Drone is already in the air. Cannot take off again.")

    def land(self):
        if not self.landed:
            self.show_message("Drone is landing.")
            self.battery_percentage -= self.battery_consumption['land']
            self.landed = True
            self.position = (0, 0, 0)
        else:
            self.show_message("Drone is already on the ground. Cannot land again.")

    def move_up(self):
        if not self.landed:
            self.show_message("Drone is moving up.")
            self.battery_percentage -= self.battery_consumption['up']
            self.position = (self.position[0], self.position[1], self.position[2] + 1)
        else:
            self.show_message("Drone has landed. Cannot execute move.")

    def move_down(self):
        if not self.landed:
            self.show_message("Drone is moving down.")
            self.battery_percentage -= self.battery_consumption['down']
            self.position = (self.position[0], self.position[1], self.position[2] - 1)
        else:
            self.show_message("Drone has landed. Cannot execute move.")

    def move_forward(self):
        if not self.landed:
            self.show_message("Drone is moving forward.")
            self.battery_percentage -= self.battery_consumption['forward']
            self.position = (self.position[0] + 1, self.position[1], self.position[2])
        else:
            self.show_message("Drone has landed. Cannot execute move.")

    def move_backward(self):
        if not self.landed:
            self.show_message("Drone is moving backward.")
            self.battery_percentage -= self.battery_consumption['back']
            self.position = (self.position[0] - 1, self.position[1], self.position[2])
        else:
            self.show_message("Drone has landed. Cannot execute move.")

    def move_left(self):
        if not self.landed:
            self.show_message("Drone is moving left.")
            self.battery_percentage -= self.battery_consumption['left']
            self.position = (self.position[0], self.position[1] - 1, self.position[2])
        else:
            self.show_message("Drone has landed. Cannot execute move.")

    def move_right(self):
        if not self.landed:
            self.show_message("Drone is moving right.")
            self.battery_percentage -= self.battery_consumption['right']
            self.position = (self.position[0], self.position[1] + 1, self.position[2])
        else:
            self.show_message("Drone has landed. Cannot execute move.")

    def rotate_clockwise(self):
        if not self.landed:
            self.show_message("Drone is rotating clockwise.")
            self.battery_percentage -= self.battery_consumption['cw']
        else:
            self.show_message("Drone has landed. Cannot execute move.")

    def rotate_counterclockwise(self):
        if not self.landed:
            self.show_message("Drone is rotating counterclockwise.")
            self.battery_percentage -= self.battery_consumption['ccw']
        else:
            self.show_message("Drone has landed. Cannot execute move.")

    def flip(self):
        if not self.landed:
            self.show_message("Drone is flipping forward.")
            self.battery_percentage -= self.battery_consumption['flip']
        else:
            self.show_message("Drone has landed. Cannot execute move.")

    def print_battery_status(self):
        return f"Battery Percentage: {self.battery_percentage}%"

    def predict_next_move(self):
        if self.destination is not None:
            current_position = self.position
            destination_distance = math.sqrt(sum((x - y) ** 2 for x, y in zip(current_position, self.destination)))
            if destination_distance < 1:
                self.land()
                return "Destination Reached. Drone Landed."
            else:
                movements = ['up', 'down', 'forward', 'back', 'left', 'right', 'cw', 'ccw', 'flip']
                best_move = None
                min_distance = float('inf')
                for move in movements:
                    new_position = self.get_new_position(move)
                    move_distance = math.sqrt(sum((x - y) ** 2 for x, y in zip(new_position, self.destination)))
                    if move_distance < min_distance:
                        min_distance = move_distance
                        best_move = move
                return f"Predicted Next Move: {best_move.capitalize()}"
        else:
            return "No destination set."

    def get_new_position(self, move):
        if move == 'up':
            return self.position[0], self.position[1], self.position[2] + 1
        elif move == 'down':
            return self.position[0], self.position[1], self.position[2] - 1
        elif move == 'forward':
            return self.position[0] + 1, self.position[1], self.position[2]
        elif move == 'back':
            return self.position[0] - 1, self.position[1], self.position[2]
        elif move == 'left':
            return self.position[0], self.position[1] - 1, self.position[2]
        elif move == 'right':
            return self.position[0], self.position[1] + 1, self.position[2]
        else:
            return self.position

    def show_message(self, message):
        print(message)

# Class designed to deploy drone simulation GUI.
class DroneGUI(QWidget):
    def __init__(self, drone):
        super().__init__()
        self.drone = drone
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Drone Simulator")
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QVBoxLayout()

        self.status_label = QLabel("Drone Status:")
        layout.addWidget(self.status_label)

        self.battery_label = QLabel()
        layout.addWidget(self.battery_label)

        self.position_label = QLabel()
        layout.addWidget(self.position_label)

        self.destination_label = QLabel("Enter Destination (comma-separated coordinates):")
        layout.addWidget(self.destination_label)

        self.destination_input = QLineEdit()
        layout.addWidget(self.destination_input)

        self.submit_destination_button = QPushButton("Submit Destination")
        self.submit_destination_button.clicked.connect(self.submit_destination)
        layout.addWidget(self.submit_destination_button)

        self.predict_button = QPushButton("Predict Best Move")
        self.predict_button.clicked.connect(self.predict_move)
        layout.addWidget(self.predict_button)

        self.command_label = QLabel("Enter Command:")
        layout.addWidget(self.command_label)

        self.command_input = QLineEdit()
        layout.addWidget(self.command_input)

        self.command_button_layout = QVBoxLayout()
        layout.addLayout(self.command_button_layout)
        self.create_command_buttons()

        self.setLayout(layout)
        self.update_battery_status()
        self.update_position_status()
        self.show()

    def create_command_buttons(self):
        commands = ['takeoff', 'land', 'move_up', 'move_down', 'move_forward', 'move_backward', 'move_left', 'move_right', 'rotate_clockwise', 'rotate_counterclockwise', 'flip']
        for command in commands:
            button = QPushButton(command.capitalize())
            button.clicked.connect(lambda _, cmd=command: self.execute_command(cmd))
            self.command_button_layout.addWidget(button)

    def submit_destination(self):
        destination_input = self.destination_input.text()
        destination_coords = [int(coord) for coord in destination_input.split(',') if coord.strip().isdigit()]
        if len(destination_coords) == 3:
            self.drone.destination = tuple(destination_coords)
            self.show_message("Destination submitted.")
        else:
            self.show_message("Invalid destination format.")

    def predict_move(self):
        predicted_move = self.drone.predict_next_move()
        self.show_message(predicted_move)

    def execute_command(self, command):
        getattr(self.drone, command)()
        self.update_battery_status()
        self.update_position_status()

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec_()

    def update_battery_status(self):
        battery_status = self.drone.print_battery_status()
        self.battery_label.setText(battery_status)

    def update_position_status(self):
        position_text = f"Position: {self.drone.position}"
        self.position_label.setText(position_text)


def main():
    csv_file = './average_battery_consumption/average_battery_data.csv'
    df = pd.read_csv(csv_file)
    # Hardcoded battery consumption for commands since 'up' was not properly tested and needed a special case.
    command_battery = {'takeoff': df.loc[df['Command'] == 'takeoff', 'Battery Consumption (%)'].iloc[0],
                       'land': df.loc[df['Command'] == 'land', 'Battery Consumption (%)'].iloc[0],
                       'up': 1.01,
                       'down': df.loc[df['Command'] == 'down', 'Battery Consumption (%)'].iloc[0],
                       'forward': df.loc[df['Command'] == 'forward', 'Battery Consumption (%)'].iloc[0],
                       'back': df.loc[df['Command'] == 'back', 'Battery Consumption (%)'].iloc[0],
                       'left': df.loc[df['Command'] == 'left', 'Battery Consumption (%)'].iloc[0],
                       'right': df.loc[df['Command'] == 'right', 'Battery Consumption (%)'].iloc[0],
                       'cw': df.loc[df['Command'] == 'cw', 'Battery Consumption (%)'].iloc[0],
                       'ccw': df.loc[df['Command'] == 'ccw', 'Battery Consumption (%)'].iloc[0],
                       'flip': df.loc[df['Command'] == 'flip', 'Battery Consumption (%)'].iloc[0]}

    simulated_drone = SimulatedTello(command_battery)

    app = QApplication(sys.argv)
    gui = DroneGUI(simulated_drone)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
