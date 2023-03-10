==================================
  Author
==================================
Doug de Jesus
drd8913@nyu.edu
N14928011


==================================
  Overview
==================================
This is a demonstration of the Vicsek model, which describes active matter.
The resulting motion is similar to swarming behavior seen in birds and fish.
In this simplistic model, the behavior of individual agents is governed by just
two rules, yet complex patterns of collective motion emerge.

At each time step, the heading of each agent is updated to match the average
heading of their neighbors, plus some amount of white noise. Agents move at a 
constant speed.

The environment has a toroidal geometry. That is, when an agent goes off the 
right side of the screen, they reappear on the left. This is taken into account
in the distance calculations (agents at opposite edges are still considered
neighbors).


==================================
  How to run
==================================
Use python version 3.9 or higher
To install the necessary libraries: pip install -r requirements.txt
In order to save the animation as a video, the FFmpeg package must be installed.
Otherwise, set 'save_to_file' to false in the configuration file.

To run: python3 main.py


==================================
  Configuration
==================================
Modify the provided config file, simulation_params.ini, to change the parameters
of the simulation. 

The noise intensity represents the amount of white noise that is added to the
average heading. A value of 0 means no noise, and the heading is determined 
purely by the average of the neighbors. A value of 1 means the heading is 
entirely random.

You can specify the size of the environment, the number of agents, the time step,
duration, agent speed, and neighborhood radius.

Note that the computation time scales quadratically with the number of agents. 
Simulating 500 agents for 1000 time steps takes around 3 minutes on an M1 Pro.

The animation can optionally be saved to a .mp4 file by setting the save_to_file
config option.
