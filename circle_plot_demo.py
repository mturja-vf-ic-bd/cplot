import numpy as np
from matplotlib.patches import Wedge
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

def get_box_circle_patches(center, rad, arc_ratio, c_arc, width, window=(0, 360)):
    """
    Helper function
    Returns a list of circular arcs given a center, radius and a window
    """
    patches = []
    start, end = window[0], window[1]
    r = end - start
    arc_l = arc_ratio * r / c_arc
    gap = (1 - arc_ratio) * r / c_arc

    for i in range(0, c_arc):
        patches += [
            Wedge(center, rad, start + i * (gap + arc_l), start + i * (gap + arc_l) + arc_l,
                  width=width)  # Ring sector
        ]

    return patches


def plot_ring(color_list_face, color_list_edge, lobes):
    """
    Creates a ring with given face color and edge(boundary) color.
    """

    fig, ax = plt.subplots(figsize=(10, 10))
    patches = []

    # Some limiting conditions on Wedge
    center = (.5, .5)
    rad = 0.5
    colors_face = []
    colors_edge = []
    lobes = np.array(lobes)
    lobe_gap = 2
    lobes_ratio = lobes / sum(lobes)
    text_coord_patch = []
    for i, color in enumerate(color_list_face):
        start = 0
        total = 360
        new_patches = []
        for j, lobe in enumerate(lobes):
            if j >= len(lobes) / 2 and start < 180:
                start = 180
            end = start + total * lobes_ratio[j] - lobe_gap
            lobe_patch = get_box_circle_patches(center, rad, 0.8, lobe, 0.01,
                                                window=(start, end))
            new_patches += lobe_patch
            # if i == 0:
            #     text_coord_patch.append(lobe_patch[int(len(lobe_patch)/2) - 1])
            start = end + lobe_gap

        patches += new_patches
        rad = rad * 0.97
        colors_face += list(color)
        colors_edge += list(color_list_edge[i])

    p = PatchCollection(patches, facecolors=colors_face, edgecolors=None, alpha=1)
    ax.add_collection(p)
    ax.set_axis_off()

    return new_patches

def get_lobe_wise_color_ring(c=1):
    """
    Returns a list of color with different colors for different lobes.
    """
    lobes_count = [22, 8, 6, 12, 14, 12, 12, 14, 12, 6, 8, 22]
    face_color = []
    color_list = ['#ff0000', '#33F3FF', '#0000ff', '#008000', '#FF33F6', '#fffc33',
                  '#fffc33', '#FF33F6', '#008000', '#0000ff', '#33F3FF', '#ff0000']
    for i, lc in enumerate(lobes_count):
        face_color = face_color + [color_list[i]] * lc

    rings = []
    for i in range(c):
        rings.append(face_color)
    return rings, rings


# Helper function to draw links
def get_edges(coord, links):
    edges = []
    for link in links:
        i, j, w = link
        edges.append((coord[i], coord[j], w))

    return edges

def plot_edges(edges):
    for edge in edges:
        x1, y1 = edge[0]
        x2, y2 = edge[1]
        w = edge[2]
        plt.plot([x1, x2], [y1, y2], marker='.', ls='-',
                 color='#804000', linewidth=w*500, alpha=0.5)


def plot_circle(edges, color_list_face, color_list_edge = None, save=True, fname='circle_plot'):
    lobes_count = [22, 8, 6, 12, 14, 12, 12, 14, 12, 6, 8, 22]
    if color_list_edge is None:
        color_list_edge = color_list_face
    inner_ring = plot_ring(color_list_face, color_list_edge, lobes_count)
    center = (.5, .5)
    coord = []
    for patch in inner_ring:
        theta = (patch.theta2 + patch.theta1) * np.pi / 360
        r = patch.r * 0.95
        x, y = r * np.cos(theta) + center[0], r * np.sin(theta) + center[1]
        coord.append((x, y))

    if edges is not None:
        edges = get_edges(coord, edges)
        plot_edges(edges)
    if save:
        fig = plt.gcf()
        fig.tight_layout()
        fig.savefig(fname + '.png')
    else:
        plt.show()

def read_matrix_from_text_file(fname):
    """
    Helper function to read matrix from text file
    """
    a = []
    fin = open(fname, 'r')
    for line in fin.readlines():
        a.append([float(x) for x in line.split()])

    a = np.asarray(a)
    return a

def get_top_links(connectome, count=100, offset=0, weight=False):
    """
    Returns top count links of a connectome
    """
    connectome = np.array(connectome)
    row, col = connectome.shape
    idx = np.argsort(connectome, axis=None)[::-1]
    idx_row = idx // col
    idx_col = idx % col
    if not weight:
        idx_coord = list(zip(idx_row, idx_col))
    else:
        idx_coord = list(zip(idx_row, idx_col, connectome[idx_row, idx_col]))

    return idx_coord[offset:count + offset]


import json
def sort_matrix(matrix, circular=False):
    """
    This function is used to order the nodes according to lobes around the circle
    """
    pt_name = "parcellationTable_Ordered.json" # parcellation table to edit VisuOrder

    # Read parcellation table to edit VisuOrder
    with open(pt_name) as f:
        pt = json.load(f)
    f.close()
    order = np.argsort([pt[i]["VisuOrder"] for i in range(0, len(pt))])
    l = len(order)
    if not circular:
        order[int(l/2):l] = np.flip(order[int(l/2):l])

    sorted_matrix = matrix[order, :]
    sorted_matrix = sorted_matrix[:, order]
    return sorted_matrix, order


if __name__ == '__main__':
    # Read adjacency matrix
    # data = read_matrix_from_text_file('demo_network.txt')
    # data = (data + data.T) / 2  # symmetry
    # data /= data.sum()  # whole-brain normalization
    #
    # # Sort the matrix lobe-wise so that nodes of the same lobe are adjacent to one another in the matrix
    # data, order = sort_matrix(data)
    #
    # # We only choose top 100 edges to display. If we display all the edges it will look cluttered.
    # # links = get_top_links(data, count=500, offset=0, weight=True)
    # links = []

    # Get lobe-wise coloring of the ring. Change this to apply different coloring scheme.
    face_color, edge_color = get_lobe_wise_color_ring(3)

    # Plot and save
    # Input to this function is the face color and the edge color. I used the same
    # color for both.
    plot_circle(None, face_color, save=True, fname='demo_cplot')