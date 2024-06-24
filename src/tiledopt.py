from beef import fe
from patterns import Pattern
import math
import numpy as np

class TiledSimulation:
    def __init__(self, pattern: Pattern, visualize_results = False, nonlin = False):
        self.num_tiles = len(pattern)
        self.pattern = pattern
        self.relocate_patterns(pattern)
        self.execute_simulation(nonlinearity = nonlin, visualize = visualize_results)
    
    def relocate_patterns(self, pattern: Pattern, radius = 30, num_tiles=5):
        self.num_tiles = num_tiles
        start_verts = pattern[0].vertices()
        start_edges = pattern[0].edges()
        start_bV = pattern[0].boundary_vertices()
        self.num_verts = start_verts.shape[0]
        self.num_edges = start_edges.shape[0]
        self.apothem = radius * math.cos(math.pi/6)
        transl_vec = np.array([0, 2 * self.apothem, 0])

        new_verts = start_verts
        new_edges = start_edges
        new_bV = start_bV
        for i in range(num_tiles-1):
            moved_verts = pattern[i+1].vertices() + transl_vec * (i+1)
            moved_edges = pattern[i+1].edges() + self.num_verts * (i+1)
            moved_bV =    pattern[i+1].boundary_vertices() + self.num_verts * (i+1)
            new_verts = np.concatenate((new_verts, moved_verts), axis=0)
            new_edges = np.concatenate((new_edges, moved_edges), axis=0)
            new_bV    = np.concatenate((new_bV,    moved_bV), axis=0)
        self.vertices = new_verts
        self.edges = new_edges
        self.boundary_vertices = new_bV
    
    def execute_simulation(self, nonlinearity=False, visualize = False):
        self.create_material()
        self.define_geometry()
        self.create_boundary_conditions_tiled()
        self.plot_tiled(visualize = False)
        self.analyze_tiled(visualize = visualize, include_nonlinearity = nonlinearity)
        self.plot_results()
    
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
        section = fe.Section(**section_params, name='cross section')
        self.section = section
        return section

    # create mesh
    def define_geometry(self):
        parts = []
        for i in range(self.num_tiles):
            v0 = 0 + self.num_verts * i
            v1 =     self.num_verts * (i+1)
            e0 = 0 + self.num_edges * i
            e1 =     self.num_edges * (i+1)
            node_matrix = np.concatenate(   ( np.arange(0 + i * self.num_verts, self.num_verts + i * self.num_verts, 1, dtype=int).reshape(self.num_verts,1), self.vertices[v0:v1,:] ), axis=1)
            element_matrix = np.concatenate(( np.arange(0 + i * self.num_edges, self.num_edges + i * self.num_edges, 1, dtype=int).reshape(self.num_edges,1), self.edges[e0:e1, :]  ), axis=1)
            sections = [self.section] * element_matrix.shape[0]
            part = fe.Part(node_matrix, element_matrix, sections)
            parts.append(part)
        self.parts = parts
        
    def create_boundary_conditions_tiled(self):
        master_nodes = [self.boundary_vertices[1], self.boundary_vertices[7], self.boundary_vertices[13], self.boundary_vertices[19]]
        slave_nodes = [self.boundary_vertices[10], self.boundary_vertices[16], self.boundary_vertices[22], self.boundary_vertices[28]]
        constraints_tie = [fe.Constraint(master_nodes, slave_nodes=slave_nodes, dofs='all', node_type='beam3d')] 
        constraints_roller = [fe.Constraint( [self.boundary_vertices[4]], dofs=[0,2,4,5], node_type='beam3d')]
        constraints_fix = [fe.Constraint( [self.boundary_vertices[1 + 6 * (self.num_tiles-1)]], dofs=[0,1,2,4,5], node_type='beam3d')]
        self.boundary_conditions = constraints_tie + constraints_fix + constraints_roller

    def plot_tiled(self, visualize = False):
        self.assembly = fe.Assembly(self.parts, constraints = self.boundary_conditions)
        if visualize:
            self.assembly.plot(node_labels=True, element_labels=True)
    
    # analyze tiled scenario
    def analyze_tiled(self, visualize = False, include_nonlinearity = False):
        self.connector_nodes = np.arange(2, self.num_verts * (self.num_tiles-1), self.num_verts, dtype=int).reshape(self.num_tiles-1,1) 
        uniform_forces = [fe.Force(self.connector_nodes, 2, 0.05, plotcolor = 'DarkOrange')]
        roller_force = [fe.Force([self.boundary_vertices[4]], 1, 0, plotcolor = 'DarkOrange')]
        moment = [fe.Force([self.boundary_vertices[4]], 3, 0.0001, plotcolor = 'DarkOrange')]
        self.forces = uniform_forces + moment + roller_force
        self.analysis = fe.Analysis(self.assembly, forces = self.forces, dt=0.5, itmax=20)
        if include_nonlinearity:
            self.u = self.analysis.run_static(print_progress=True, return_results=True)
        else:
            self.u = self.analysis.run_lin_static(print_progress=True, return_results=True)
        if visualize:
            sc = self.analysis.eldef.plot(plot_nodes=False, node_labels=True, plot_states=['deformed', 'undeformed'])

    def plot_results(self):
        displ_history = self.u[:,-1]
        displ_per_node = np.split(displ_history, np.shape(self.u)[0]/6)
        norms = []
        for i in range(len(self.connector_nodes)):
            displ_translations = np.array(displ_per_node)[self.connector_nodes[i],0:3]
            norm = np.linalg.norm(displ_translations, axis=1)
            norms.append(norm.tolist())
        self.displ = norms
        self.transl_roller = np.array(displ_per_node)[self.boundary_vertices[4],1]
