import numpy as np
import pyclipr
from patterns import Pattern
import triangle
import matplotlib.pyplot as plt
# import pymesh as pm
import igl
import pymeshlab

class printedPattern:
    def __init__(self, pattern: Pattern):
        self.vertices = pattern.vertices #not a function if tiled is used
        self.edges = pattern.edges      #not a function if tiled is used
        self.create_flat_pattern()
        # self.plot_pattern()

    def create_flat_pattern(self):
        path = []
        for e in range(len(self.edges)):
            path.append(( self.vertices[self.edges[e][0]][0:2].tolist(), self.vertices[self.edges[e][1]][0:2].tolist() ))
        # Create an offsetting object
        po = pyclipr.ClipperOffset()

        # Set the scale factor to convert to internal integer representation
        po.scaleFactor = int(100000)

        # add the path - ensuring to use Polygon for the endType argument
        # addPaths is required when working with polygon - this is a list of correctly orientated paths for exterior
        # and interior holes
        po.addPaths(path, pyclipr.JoinType.Miter, pyclipr.EndType.Round) 
        
        #then boolean split with hexagon to remove the round part or split with polyline
        # for p in path:
        #     pp = [np.array(p)]
        #     po.addPaths(pp, pyclipr.JoinType.Miter, pyclipr.EndType.Polygon)
        # po.addPaths(aaa, pyclipr.JoinType.Miter, pyclipr.EndType.Polygon)

        # Apply the offsetting operation using a delta.
        offsetSquare = po.execute(2.0)
        
        # Plot the results
        # plt.figure()
        # plt.axis('equal')
        # plt.fill(offsetSquare[0][:, 0], offsetSquare[0][:, 1], linewidth=1.0, linestyle='solid', edgecolor='#333', facecolor='g')
        # plt.show()



        # Convert offsetSquare to a list of vertices
        scale_factor = 1/100000
        fig_vertices = offsetSquare[0].tolist()

        # Create a dictionary from the offsetSquare edges
        segm = dict(segments = [(i, i + 1) for i in range(len(fig_vertices) - 1)] + [(len(fig_vertices) - 1, 0)])
        # points_for_holes = []
        # for i in range(len(fig_vertices)):
        #     edge = segm['segments'][i]
        #     nodes = fig_vertices[edge[0]], fig_vertices[edge[1]]
        #     tangent = np.array(nodes[1]) - np.array(nodes[0])
        #     tangent = np.append(tangent, 0)
        #     binormal = np.cross(tangent, [0, 0, 1])
        #     points_for_holes.append((np.array(nodes[0]) + 0.5 * tangent[0:2] + 0.05 * binormal[0:2])* scale_factor)
        boundary_verts = np.array(fig_vertices) #* scale_factor
        boundary_edges = [(i, i + 1) for i in range(len(fig_vertices) - 1)] + [(len(fig_vertices) - 1, 0)]
        tri_params = dict(vertices = boundary_verts, 
                          segments = boundary_edges)
        # ,
                        #   holes = points_for_holes)
        mesh = triangle.triangulate(tri_params,'zpqa0.02')


        # Plot the segments
        # plt.figure()
        # plt.axis('equal')
        # for s in segm['segments']:
        #     plt.plot([fig_vertices[s[0]][0] * scale_factor, fig_vertices[s[1]][0] * scale_factor], [fig_vertices[s[0]][1] * scale_factor, fig_vertices[s[1]][1] * scale_factor], color='b')
        # # plt.show()
        
        # Plot the vertices of the points
        # points_for_holes = np.array(points_for_holes)
        # plt.scatter(points_for_holes[:,0], points_for_holes[:, 1], color='r')
        # plt.axis('equal')
        # plt.show()

        # Plot the vertices of the triangle mesh
        # plt.scatter(mesh['vertices'][:, 0], mesh['vertices'][:, 1], color='r')
        # plt.axis('equal')
        # plt.show()

        # Plot the triangle mesh
        # plt.triplot(mesh['vertices'][:, 0], mesh['vertices'][:, 1], mesh['triangles'], color='g')
        # plt.axis('equal')
        # plt.show()

        start_verts = np.insert(mesh['vertices'], 2, 0, axis=1)
        start_faces = mesh['triangles']
        
        m = pymeshlab.Mesh(start_verts, start_faces)
        ms = pymeshlab.MeshSet()
        ms.add_mesh(m, "pattern")
        ms.meshing_isotropic_explicit_remeshing(iterations=30, targetlen = pymeshlab.PercentageValue(1.0))
        # # save the current mesh
        # ms.save_current_mesh("pattern.ply")
        
        rem_verts = ms.current_mesh().vertex_matrix()
        rem_faces = ms.current_mesh().face_matrix()
        num_verts = len(rem_verts)
        
        # duplicate the mesh and offset it
        offset_verts = np.insert(rem_verts[:,0:2], 2, 2, axis=1)
        mesh_verts = np.vstack((rem_verts, offset_verts))

        offset_faces = rem_faces + np.array([num_verts, num_verts, num_verts])
        mesh_faces = np.vstack((rem_faces, offset_faces))
        
        igl.write_triangle_mesh("patternflat.obj", rem_verts, rem_faces)

        loop_vert = igl.boundary_loop(rem_faces)
        offset_loop_vert = loop_vert + len(rem_verts)
        for i in range(len(loop_vert)):
            mesh_faces = np.vstack((mesh_faces, [loop_vert[i-1], loop_vert[i], offset_loop_vert[i-1]]))
            mesh_faces = np.vstack((mesh_faces, [loop_vert[i], offset_loop_vert[i], offset_loop_vert[i-1]]))
        
        igl.write_triangle_mesh("patternSolid.obj", mesh_verts, mesh_faces)

        


