import csv
import random

# Define the list of drone commands and their corresponding battery consumption ranges (percentage per command)
commands_battery = [
    ('up', (0.8, 1.2)),        # Example consumption range for ascending
    ('down', (1.0, 1.4)),      # Example consumption range for descending
    ('left', (0.8, 1.2)),      # Example consumption range for left movement
    ('right', (0.8, 1.2)),     # Example consumption range for right movement
    ('forward', (0.8, 1.2)),   # Example consumption range for forward movement
    ('back', (0.8, 1.2)),      # Example consumption range for backward movement
    ('cw', (1.3, 1.7)),        # Example consumption range for clockwise rotation
    ('ccw', (1.3, 1.7)),       # Example consumption range for counterclockwise rotation
    ('flip', (1.5, 2.5)),      # Example consumption range for flip maneuver
]

# Define the number of simulations to run
num_simulations = 100

# Initialize the CSV file for writing
def initialize_csv(filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Command', 'Battery Consumption (%)'])

def write_to_csv(filename, command, consumption):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([command, consumption])

def simulate_drone(commands_battery, csv_number):
    current_battery = 100
    filename = f'battery_consumption_data_{csv_number}.csv'
    initialize_csv(filename)

    # Takeoff command at the beginning
    write_to_csv(filename, 'takeoff', random.randrange(4, 6))
    current_battery -= random.uniform(*commands_battery[0][1])  # Takeoff consumption

    while current_battery > 0:
        command, (min_consumption, max_consumption) = random.choice(commands_battery[1:])  # Exclude takeoff and land
        consumption = random.uniform(min_consumption, max_consumption)
        write_to_csv(filename, command, consumption)
        current_battery -= consumption

    # Land command at the end
    write_to_csv(filename, 'land', random.randrange(2, 4))

    print(f'Drone simulation completed. CSV file created: {filename}')

# Run the simulations
for csv_number in range(1, num_simulations + 1):
    simulate_drone(commands_battery, csv_number)
