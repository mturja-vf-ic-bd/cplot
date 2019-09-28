import argparse
from circle_plot_demo import *

parser = argparse.ArgumentParser(description='CIRCLE PLOT FOR BRAIN NETWORK')
parser.add_argument('c', type=int, help='number of rings')
parser.add_argument('-l', '--link', action='store_true', help='if true, shows links inside the circle')
parser.add_argument('-f', '--input_net', default='demo_network.txt',
                    help='input file for adjacency matrix')
parser.add_argument('-o', '--outfile', default='demo_cplot',
                    help='output file for circle plot')


if __name__ == '__main__':
    # Read adjacency matrix
    args = parser.parse_args()
    if args.link:
        data = read_matrix_from_text_file(args.input_net)
        data = (data + data.T) / 2  # symmetry
        data /= data.sum()  # whole-brain normalization

        # Sort the matrix lobe-wise so that nodes of the same lobe are adjacent to one another in the matrix
        data, order = sort_matrix(data)

        # We only choose top 100 edges to display. If we display all the edges it will look cluttered.
        links = get_top_links(data, count=500, offset=0, weight=True)
    else:
        links = None


    # Get lobe-wise coloring of the ring. Change this to apply different coloring scheme.
    face_color, edge_color = get_lobe_wise_color_ring(args.c)

    # Plot and save
    # Input to this function is the face color and the edge color. I used the same
    # color for both.
    plot_circle(links, face_color, save=True, fname=args.outfile)