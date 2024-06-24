import numpy as np
from copy import deepcopy
import pyvista as pv
import matplotlib.pyplot as plt


#plot a pattern from a np.array of nodes and edges
class plotPattern:
    def __init__(self, vertices, edges):
        self.v = vertices
        self.e = edges
        self.plotPattern()
        
    def plotPattern(self):
        #create a pyvista plotter
        p = pv.Plotter()
        # print(self.v)
        #add the vertices to the plotter
        p.add_points(self.v, style='points')
        #add the edges to the plotter
        nodes = self.v[self.e]
        nodes2 = np.concatenate([nodes[i] for i in range(np.shape(nodes)[0])],axis=0)
        p.add_lines(nodes2, color='b', width=5)
        #show the plotter
        p.show()

#plot a scatter plot of the simulation results and an interpolated surface
class scatter_plot:
    def __init__(self, sim_results, load_magnitude, num_scen, parameters):
        self.sim = sim_results
        self.load_magnitude = load_magnitude
        self.num_scen = num_scen
        self.dparams = parameters
        self.scatter_plot()
    
    def scatter_plot(self):
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            X, Y, Z = [], [], []
            
            for i in range(len(self.dparams)):
                 xs = self.dparams[i]
                 ys = range(1, self.load_magnitude +1, self.load_magnitude//self.num_scen)
                 zs = self.sim[i]
                 ax.scatter(xs, ys, zs)
                 X.append([xs]*self.num_scen)
                 Y.append(ys)
                 Z.append(zs)

            ax.set_xlabel('Design parameter')
            ax.set_ylabel('Load magnitude (N mm)')
            ax.set_zlabel('Maximum displacement norm (mm)')    
            plt.show()