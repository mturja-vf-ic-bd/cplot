# Circle Plot for Brain Network Visualization

## Input:
The interface to the user is the `plot_circle` function in `circle_plot_demo.py` which takes two mandatory and three optional input.
* Mandatory Input
  * edges: list of edges(links) between nodes to be plotted. Each edges is a 3-tuple (source_index, destination_index, weight)
  * color_list_face: It's a list of `C` rings. Each ring is a list of `N` colors for the faces of the boxes. In the following output `C=1` and `N=148`
* Optional Input
  * color_list_edge: It's a list of `C` rings. Each ring is a list of `N` colors for boundary of the boxes.
  * save: saves the plot if `True`
  * fname: filename where the plot is saved.

## Output:
![Result](demo_cplot.png)
