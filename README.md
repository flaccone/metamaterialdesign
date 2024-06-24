# metamaterialdesign
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
The participant is required to conceive a parametric pattern, embedded in a regular hexagon. The pattern will be employed in a tassellated strip made of 5 hexagons that are bent out of plane from the extremities.
The task consists in creating a new pattern class in ```./src/patterns.py``` using the ```Pattern(Protocol)```.
Such class is required to expose a design parameter, that will be later used as optimization variable, see for instance ```MyPattern(Pattern)``` in ```./src/patterns.py```.

# Code usage


