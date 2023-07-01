# ProjetFinal


## The project is a single windows form program which has the goal to calculate some functionalities of the aircraft related to the air wing.


### Inputs

The program opens the window and contains a list of more than six thousand airfoil information.

The user needs to:

* select the airfoil wanted
* enter the weight
* enter the surface 
* enter the wingspan
* enter the jet thrust
* enter the altitude


#### Extras

The user can enter in one of the fields the interval values, example 100-200.

If there are more than one intervale entered, the program will consider only the first one. The others will be considered as single values, which will be the first value of that interval.


### Functionalities 

The user can use the calculations of:

* Stall speed
* Takeoff speed
* Optimal speed for maximum distance
* Takeoff distance
* Landing distance


### Results

1. If the user entered a single values without intervals, the result calculation will be printed in PyCharm
2. In case when the interface contains the interval values, the visual graphic of the variation will be displayed.
