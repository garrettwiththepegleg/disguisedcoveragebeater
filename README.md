### Overview of the project

This is a football project designed to improve reads and decision making for offenses against disguised defenses. Currently the 2 high shell look forces quick decisions and throws into tight windows in the short to intermediate areas of the field which requires the QB to be able to read and diagnose the defense in a very short amount of time which is a very difficult skill that a lot of qbs are simply not developing. The idea behind this project is to help simplify post snap reads with pre snap decisions. By taking the likelihood of where all defenders will be, I made a program to simulate and project the density of coverages per 100 ms based off of the given set to then be able to script these reads and the timing of them. 

### Instructions

# Clicking on the .exe will start the program, if you are unable to run it or the programmed is flagged further instructions to run it from CL will be given

# CL instructions
1) Make sure you have an IDE and updated version of python
2) Run pip install -r requirements.txt
3) Run the python file in the CL

# Using the program

To start the simulation just click the start button

You can move defenders around to better customize the look

When looking at the heatmaps, you can use the arrow keys to view the different coverage looks at different timestamps

### Improvements

Since this is a Work-In-Progress, I still have much to improve upon, a list of things im working on is as follows
More realistic player movement
Better customization with coverages
ML Models to find open spots
Ability to run offensive plays to see the best times to look at certain players 
Have expected probabilities conditioned on movement of a defender

Any additional feedback is appreciated