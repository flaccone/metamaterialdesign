from beef import fe
from patterns import Pattern
import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
pv.set_jupyter_backend('trame')

class Simulation:
    def __init__(self, pattern: Pattern, max_force = 10, num_scenarios = 5, visualize_geometry = False, visualize_simulations = False, visualize_results = False):
        self.vertices = pattern.vertices()
        self.edges = pattern.edges()
        self.create_material()
        self.boundary_vertices = pattern.boundary_vertices()
        self.create_boundary_conditions()
        self.define_geometry()
        self.plot_pattern(visualize = visualize_geometry)
        max_displ_norms = []
        for i in range(1, max_force+1, max_force//num_scenarios):
            self.analyze_scenario(i * max_force/num_scenarios, visualize = visualize_simulations)
            max_displ_norm = self.plot_results()
            max_displ_norms.append(max_displ_norm)
        print('Maximum displacement norms: ', max_displ_norms)
        if visualize_results:
            plt.scatter(range(1, max_force+1, max_force//num_scenarios), max_displ_norms)
            plt.xlabel('Force magnitude (N mm)')
            plt.ylabel('Max Displacement Norm (mm)')
            plt.title('Load sensitivity - Cylinder scenario')
            plt.show()
        self.results = max_displ_norms

    # create material parameters
    def create_material(self):
        section_params = dict(
            A=4,            #mm^2
            m=1.355843e-9,  #ton/mm^3
            I_z=1.3333,     #mm^4
            I_y=1.3333,     #mm^4
            E=1000,         #MPa
            J=2.6667,       #mm^4
            poisson=0.3
            )
        self.section = fe.Section(**section_params, name='cross section')

    # create mesh
    def define_geometry(self):
        self.node_matrix = np.concatenate(( np.arange(0,np.shape(self.vertices)[0], 1).reshape(np.shape(self.vertices)[0],1), self.vertices ), axis=1)
        self.element_matrix = np.concatenate(( np.arange(0,np.shape(self.edges)[0], 1).reshape(np.shape(self.edges)[0],1) , self.edges ), axis=1)
        self.sections = [self.section] * self.element_matrix.shape[0]
        self.part = fe.Part(self.node_matrix, self.element_matrix, self.sections)

    # create boundary conditions, e.g. fixed nodes
    def create_boundary_conditions(self):
        # print(self.boundary_vertices[1])
        constraints_fix = [fe.Constraint( [self.boundary_vertices[1]], dofs=[0,1,2,4,5], node_type='beam3d')]
        constraints_roller = [fe.Constraint( [self.boundary_vertices[4]], dofs=[0,2,4,5], node_type='beam3d')]
        self.boundary_conditions = constraints_fix + constraints_roller

    # assemlby and plot geometry
    def plot_pattern(self, visualize = False):
        self.assembly = fe.Assembly([self.part], constraints = self.boundary_conditions)
        if visualize:
            self.assembly.plot(node_labels=True, element_labels=True)

    # analyze scenario
    def analyze_scenario(self, force_magnitude = 1.0, visualize = False):
        loaded_nodes = np.arange(0, self.vertices.shape[0],1) 
        uniform_forces = [fe.Force(loaded_nodes, 2, 0.1, plotcolor = 'DarkOrange')]
        moments = [fe.Force([self.boundary_vertices[4]], 3, force_magnitude, plotcolor = 'DarkOrange')]
        self.forces = uniform_forces + moments
        self.analysis = fe.Analysis(self.assembly, forces = self.forces, dt=0.15, itmax=100)
        self.u = self.analysis.run_static(print_progress=True, return_results=True)
        if visualize:
            sc = self.analysis.eldef.plot(plot_nodes=False, node_labels=False, plot_states=['deformed', 'undeformed'])

    def plot_results(self):
        displ_history = self.u[:,-1]
        displ_per_node = np.split(displ_history, np.shape(self.u)[0]/6)
        displ_translations = np.array(displ_per_node)[:,0:3]
        self.norms = np.linalg.norm(displ_translations, axis=1)
        return max(self.norms)

