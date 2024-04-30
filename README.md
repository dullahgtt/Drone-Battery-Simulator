# Simulation Modeling of Recreational-Use Battery Consumption Tracking for the DJI Tello Quadcopter

This project aims to create a simulated drone testing environment that allows users to track battery usage of their drones using values collected from a 100 drone flight test set. For each drone movement, the amount of battery consumed is calculated by determining how much energy was lost after the movement. Each movement was calculated after a couple seconds and the drone was flown until battery depletion. 

## Data Visualization:

Ensure the python scripts are located in a main folder. Two subfolders are created to hold appropriate data. The **battery_consumption** folder holds all test data generated from drone test flights. The **average_battery_consumption** folder contains average battery consumption calculated by the *plot_data.py* script.

Install the appropriate python libraries for running the modules. All other python libraries should be preinstalled with most python versions.

~~~
pip install pandas
pip install plotly
pip install PyQt5
~~~

Install the *Live Server* extension for visualizing html in the browser with ease. This will be used to visualize the average/regular battery consumption plots in the next step.

Following this, run the *plot_data.py*, which takes all drone test data and generates the appropriate plots to visualize and calculate average battery consumption. Several files are created after this script has been run.

1. *drone_motion_final.png* -> visualizes all drone test flights in image format using plotly library.
2. *drone_motion_final.html* -> renders an interactive 3D html of all test flights
3. *battery_consumption_final.png* -> visualizes total battery consumption of each drone in-flight maneuver in a bar plot.
4. *battery_consumption_final.html* -> html version of the total battery consumption bar plot.
5. *average_battery_consumption.png* -> visualizes average battery consumption of each drone in-flight maneuver in a line plot.
6. *average_battery_consumption.html* -> visualizes the average battery consumption data in a line plot via html.

For 2, 4, and 6, these html files can be rendered by right clicking on the filename on the left-hand toolbar on VSCode and clicking "Open with Live Server". This will automatically open a browser window with the html rendered. 3D plots are interactive and allow the user to scroll and visualize he data. The *drone_motion_final.html* plot allows the user to double click on any drone flight in the map key on the far right to isolate the flight path.

Each of these files are merely for visualizing data and does not serve any additional purpose in the making of the solution.

Alongside the data visualization files is another data file called *average_battery_consumption.csv*. This file should have the following columns rendered:

- **back** represents the drone command for flying backwards
- **ccw** represents the drone command for turning counter clockwise
- **cw** represents the drone command for turning clockwise
- **down** represents the drone command for reducing altitude
- **flip** represents the drone command for flipping 360^o from its original bearing
- **forward** represents the drone command moving forward
- **land** represents the drone command for landing
- **left** represents the drone command for moving towards the left
- **right** represents the drone command for moving towards the right
- **takeoff** represents the drone command for taking off

The file, *average_battery_consumption.csv*, should look something like this:
~~~
Command,Battery Consumption (%)
back,0.9912388023489754
ccw,1.495894063086908
cw,1.4993323474689597
down,1.201448307177061
flip,2.0078600515827425
forward,1.0010765115843205
land,2.57
left,0.9953362256009394
right,0.9943151173038987
takeoff,4.47
~~~

***DISCLAIMER***: The 'up' command was not properly tested as it was not included in the test runs, and hence is not included in any of the test or result data. In the following part of the project, all 'up' data metrics are hard coded into the algorithm, while other sections utilize average battery consumption metrics found in the preliminary tests and displayed as an example above.

## Drone Simulator:

At this stage, there are two main program files, *tello_battery_tracker_astar.py* and *tello_battery_tracker.py*. For all intents and purposes, I only tested the second simulation: *tello_battery_tracker.py*. The first siimulation was an attempt to implement the popular A-Star path planning algorithm to help predict best path and least battery usage to reach a user designated way point. However, after lengthy testing, the algorithm did not work properly and ran infinitely. The second simulation runs a simple Euclidean distance algorithm to determine next best movement to reach the user defined waypoint.

To run *tello_battery_tracker.py*, simply right click anywhere on the code screen and click "Run Code". After this, a Drone Simulator GUI will open, displaying the drone status, including its battery percentage and Cartesian coordinate location, defaulted at (0,0,0) for ease of calculations. 

### Steps to run the *Drone Simulator*:

1. Enter the drone destination into the **Enter Distance (comma-seperated coordinates):** text box. It must be in the format *x,y,z* and all numbers must be positive integers. It is recommended to use smaller integers for ease of testing.
2. Hit **Submit Destination**, which will save your current destination to the program.
3. Either enter **takeoff** into the **Enter Command** text box, or click the **Takeoff** button to have your drone takeoff.
4. Click the **Predict Best Move** button to show next best move to reach destination. A pop up will display the appropriate move.
5. Close the pop up and click the corresponding button to move the drone closer to the destination.
6. The drone can be flown without aid of the **Predict Best Move** button. It is merely an assistance feature of the simulator.
7. Once the drone reaches its destination, it can continue flying, but if the **Predict Best Move** button is clicked, the drone will automatically land as it has reached its destination.
8. To terminate the session, simply click the **x** at the top right corner of the window.

***NOTE***: Relevant messages to the simulator are displayed on the terminal of the IDE, and will be similar to this:

~~~
Drone has landed. Cannot execute move.
Drone is taking off.
Drone is moving up.
Drone is moving right.
Drone is moving up.
Drone is moving forward.
Drone is moving right.
Drone is moving up.
Drone is moving forward.
Drone is moving right.
Drone is landing.
~~~

## Testing:

Various different destination points can be put into the simulator to test the various maneuvers of the drone. Currently, the simulator is unable to properly implement *clockwise*, *counterclockwise*, and *flip* maneuvers as there wasn't time to implement a bearing parameter.

One issue that needs addressing is the drone will continue to fly even after the battery has been depleted. This has not been properly implemented into the system, but battery depletion is accurate through the testing that has been done on the DJI Tello Quadcopter.
