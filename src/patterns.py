from typing import Protocol
import numpy as np
import numpy.typing as npt
import math

class Pattern(Protocol):
    def __init__(self) -> None:
        super().__init__()
    # vertex, edges, endpoints for BC and loads
    def vertices(self) -> npt.NDArray:
        pass

    def edges(self) -> npt.NDArray:
        pass

    def boundary_vertices(self) -> npt.NDArray:
        pass


class MyPattern(Pattern):
    # create a hexagon with a given radius (mm) and exposed design parameter
    def __init__(self,radius = 30, my_design_parameter = 1):
        self.radius = radius
        verts = [ [0, 0, 0] ]
        startPoint = np.array([radius * math.cos(math.pi/6), 0, 0])
        angles = np.array([1/6, 1/2, 5/6, 7/6, 3/2, 11/6]) * math.pi
        for i in range(np.size(angles)):
            rotMatrix = np.array([ [math.cos(angles[i]), -math.sin(angles[i]), 0],
                                   [math.sin(angles[i]),  math.cos(angles[i]), 0],
                                    [0 , 0 , 1] ])
            newPoint = np.dot(rotMatrix, startPoint).tolist()
            verts.append(newPoint)
        for ii in range(np.size(angles)):
            mid_vert = [x/2 for x in verts[ii+1]]
            alpha = my_design_parameter * math.pi
            rotMatrix = np.array([ [math.cos(alpha), -math.sin(alpha), 0],
                                   [math.sin(alpha),  math.cos(alpha), 0],
                                    [0 , 0 , 1] ])
            rotated_mid_vert = np.dot(rotMatrix, mid_vert).tolist()
            verts.append(rotated_mid_vert)
        self.v = np.array(verts)
        # print(self.v)
        
        self.bV = np.arange(1, 7, 1, dtype=int)
        # print(self.bV)

        self.e = np.insert(self.bV.reshape(6,1)+6,0,0,axis=1)
        self.e = np.append(self.e, np.array([[self.bV[e], self.bV[e]+ 6] for e in range(len(self.bV))]), axis=0)
        # print(self.e)

    # vertex, edges, endpoints for BC and loads
    def vertices(self) -> npt.NDArray:
        return self.v

    def edges(self) -> npt.NDArray:
        return self.e

    def boundary_vertices(self) -> npt.NDArray:
        return self.bV

