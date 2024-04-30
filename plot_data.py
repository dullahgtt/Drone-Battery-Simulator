import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def read_csvs(folder_path):
    dataframes = []
    for i in range(1, 101):
        file_name = f'battery_consumption_data_{i}.csv'
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path)
            print(f'Read CSV: {file_path}')
            print(df.head())
            dataframes.append(df)
    return dataframes

def plot_drone_motion(dataframes):
    fig = px.line_3d(title='Drone Motion')
    colors = px.colors.qualitative.Set1
    for i, df in enumerate(dataframes):
        current_position = {'X': 0, 'Y': 0, 'Z': 0}
        color = colors[i % len(colors)]
        positions = []
        for index, row in df.iterrows():
            command = row['Command']
            if command in ['takeoff', 'land']:
                continue

            movement = get_movement(command)
            current_position = update_position(current_position, movement)
            positions.append(current_position)

        x_coords = [pos['X'] for pos in positions]
        y_coords = [pos['Y'] for pos in positions]
        z_coords = [pos['Z'] for pos in positions]

        fig.add_trace(go.Scatter3d(
            x=x_coords,
            y=y_coords,
            z=z_coords,
            mode='lines',
            line=dict(color=color, width=4),
            name=f'Flight {i + 1}'
        ))

    fig.write_image('drone_motion_final.png', width=1200, height=800)
    fig.write_html('drone_motion_final.html', full_html=False, include_plotlyjs='cdn')

def get_movement(command):
    movements = {
        'forward': {'X': 0, 'Y': 1, 'Z': 0},
        'back': {'X': 0, 'Y': -1, 'Z': 0},
        'left': {'X': -1, 'Y': 0, 'Z': 0},
        'right': {'X': 1, 'Y': 0, 'Z': 0},
        'up': {'X': 0, 'Y': 0, 'Z': 1},
        'down': {'X': 0, 'Y': 0, 'Z': -1},
        'cw': {'X': 0, 'Y': 0, 'Z': 0},
        'ccw': {'X': 0, 'Y': 0, 'Z': 0},
        'flip': {'X': 0, 'Y': 0, 'Z': 0},
    }
    return movements.get(command, {'X': 0, 'Y': 0, 'Z': 0})

def update_position(current_position, movement):
    new_position = {
        'X': current_position['X'] + movement['X'],
        'Y': current_position['Y'] + movement['Y'],
        'Z': current_position['Z'] + movement['Z'],
    }
    return new_position

def plot_battery_consumption(dataframes):
    consumption_data = {'Command': [], 'Battery Consumption (%)': [], 'Flight': []}
    for i, df in enumerate(dataframes):
        for index, row in df.iterrows():
            command = row['Command']
            consumption = row['Battery Consumption (%)']
            consumption_data['Command'].append(command)
            consumption_data['Battery Consumption (%)'].append(consumption)
            consumption_data['Flight'].append(i + 1)

    avg_consumption = pd.DataFrame(consumption_data).groupby(['Command', 'Flight']).mean().reset_index()
    fig = px.bar(avg_consumption, x='Command', y='Battery Consumption (%)',
                 color='Command', title='Battery Consumption per Command')
    fig.write_image('battery_consumption_final.png', width=1200, height=800)
    fig.write_html('battery_consumption_final.html', full_html=False, include_plotlyjs='cdn')
    
def plot_average_battery_consumption(dataframes):
    avg_consumption = pd.concat(dataframes).groupby('Command')['Battery Consumption (%)'].mean().reset_index()
    fig = px.line(avg_consumption, x='Command', y='Battery Consumption (%)', title='Average Battery Consumption per Command')
    fig.update_traces(mode='lines+markers+text', text=avg_consumption['Battery Consumption (%)'], textposition='top center', textfont_size=8)
    fig.update_layout(xaxis_title='Command', yaxis_title='Average Battery Consumption (%)')
    fig.write_image('./average_battery_consumption/average_battery_consumption.png', width=1200, height=800)
    fig.write_html('./average_battery_consumption/average_battery_consumption.html', full_html=False, include_plotlyjs='cdn')
    return avg_consumption

def write_average_to_csv(avg_data, filename):
    avg_data.to_csv(filename, index=False)

def main():
    folder_path = './battery_consumption'
    dataframes = read_csvs(folder_path)
    
    print('Dataframes:', dataframes)
    print('Number of Dataframes:', len(dataframes))

    plot_drone_motion(dataframes)
    plot_battery_consumption(dataframes)
    write_average_to_csv(plot_average_battery_consumption(dataframes), filename = './average_battery_consumption/average_battery_data.csv')
    
if __name__ == "__main__":
    main()
