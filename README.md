# Metamaterial Design and Optimization
Activity for the SIGCHI Summer School

# Installation
Open a Terminal.
Change the current working directory to the location of your repositories.

~~~
git clone https://github.com/flaccone/metamaterialdesign
~~~

Move to the repository root directory. You can set up a Pyhon virtual environment. The code runs on Python 3.12.....

If you use macOS with ARM, as a first step, install ```pymeshlab``` and ```nlopt``` requiring a wheel:
~~~
pip install ./m1_wheels/...
~~~

Then install all other dependencies:
~~~
pip install -r requirements.txt
~~~

If you use Win make sure you have a C++ compiler installed.

If you use Ubuntu or Win, install all dependencies with:
~~~
pip install -r requirements.txt
~~~


# Task  
The participant is required to conceive a parametric pattern, embedded in a regular hexagon. The pattern will be employed in a tassellated strip made of 5 hexagons that are bent out of plane from the extremities as a metamaterial strip.

The task consists in creating a new pattern class in ```./src/patterns.py``` using the ```Pattern(Protocol)```.

Such class is required to expose a design parameter, that will be later used as optimization variable, see for instance ```MyPattern(Pattern)``` in ```./src/patterns.py```.

It is mandatory to ... vert ids and BC


# Code usage
If the code is run as is, the result will show the bending scenario that optimizes ```MyPattern()``` to achieve the end goal of the project, i.e. a target bending deformation.

In ```./src/main.py```, the participant is asked to replace ```MyPattern``` (line 9, 41 and 58) with his/her own pattern class.

The ```options``` dictionary (line 10 in ```./src/main.py```) allows the user to test his/her design before performing the optimization task.

In particular:

```'pattern preview'``` if True shows a pyvista 3D preview of the pattern with vetices and edges indices.

```'load simulations``` > 0, performs for a given max force the input number of bending scenarios.

```'design parameter sensitivity'``` constructs a 3D design domain showing displacement vs design parameter vs load.

```'optimization scenario'``` if True performs the optimization task of finding the best parameter value so tha the deformed shape of the tassellated strip is close to a target one.

```'save file for 3D print'``` if True outputs a solid mesh.

```opt_init_parameters``` np.array containing the (five) initialization values of the optimization variables, i.e., one design parameter per pattern (hexagon)

```opt_lower_bounds```  np.array containig the lower bounds for the optimization variables

```opt_upper_bounds```  np.array containig the upper bounds for the optimization variables

