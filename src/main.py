from patterns import *
from patternPlot import plotPattern, scatter_plot
from simulation import Simulation
from printpattern import printedPattern
from tiledopt import TiledSimulation
from optimization import Optimization

# define pattern and options
p = MyPattern(my_design_parameter=0.1)
options = {'pattern preview': False,                              # True or False
           'load simulations': 0,                                # 0, or number of simulations
           'design parameter sensitivity': None,                 # None, or list of design parameters [0.1, 0.2, 0.3, 0.5]
           'optimization scenario': False,                       # True or False
           'save file for 3D print': False}                      # True or False
# define optimization parameters
opt_init_parameters = np.array([0.01, 0.05, 0.1, 0.3, 0.35])
opt_lower_bounds = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
opt_upper_bounds = np.array([0.5, 0.5, 0.5, 0.5, 0.5])



# pattern preview
if options['pattern preview']:
    plotPattern(p.vertices(), p.edges())


# simulation with load as variables
if options['load simulations'] > 0:
    sim = Simulation(p, max_force=20, num_scenarios = options['load simulations'],visualize_results=True, visualize_geometry=True, visualize_simulations=True)
    print(sim.node_matrix)
    print(sim.element_matrix)


# design parameter sensitivity
if options['design parameter sensitivity'] is not None:
    design_parameters = options['design parameter sensitivity']
    load_magnitude = 10
    num_scen = 4
    simulation_results = []
    for dp in design_parameters:
        design_pattern = MyPattern(my_design_parameter=dp)
        sim = Simulation(design_pattern, max_force=load_magnitude, num_scenarios = num_scen)
        simulation_results.append(sim.results)
    scatter_plot(simulation_results, load_magnitude, num_scen, design_parameters)


# optimization scenario with five tiled patterns
patterns_list = []
parameters = []
if options['optimization scenario']:
    opt = Optimization(x = opt_init_parameters, opt_lb = opt_lower_bounds, opt_ub = opt_upper_bounds)
    # simulate real behavior of optimized tiled patterns
    parameters = opt.xopt
else:
    parameters = opt_init_parameters

for i in range(len(parameters)):
    p = MyPattern(my_design_parameter = parameters[i])
    patterns_list.append(p)


til = TiledSimulation(patterns_list, visualize_results = True, nonlin = True)
# til = TiledSimulation(patterns_list, visualize_results = False, nonlin = False)

print('Displacement norms of connectors: ', til.displ)
# print('Roller y-translation: ', til.transl_roller)
print('Distance between the supports: ', 2 * til.apothem * til.num_tiles - til.transl_roller)


# create solid pattern for 3D printing
if options['save file for 3D print']:
    printpattern = printedPattern(til)