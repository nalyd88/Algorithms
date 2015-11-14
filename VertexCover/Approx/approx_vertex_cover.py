#!/usr/bin/python
#  Dylan Crocker
#  CSE 6140
#

import networkx as nx
import numpy as np
import random


def read_graph_file(graph_file_path):
    """Read the given graph file and return a graph object.

    Note: This function utilizes objects from the networkx package.

    :param graph_file_path: Path to the graph text file.
    :return: Graph object (networkx) filled with the graph file contents.
    """

    graph_obj = nx.MultiGraph()

    # Read and parse the graph text file.
    with open(graph_file_path, 'r') as graph_file:

        # Read the header and get the number of nodes and edges.
        header = [int(x) for x in graph_file.readline().split()]
        n, e = header[0], header[1]

        for line in graph_file:
            edge_data = [int(x) for x in line.split()]
            assert(len(edge_data) == 3)
            graph_obj.add_edge(edge_data[0], edge_data[1], weight=edge_data[2])
            # Note: Adding edges will also add the nodes to the graph.

    # Ensure there are no errors with the file.
    assert(graph_obj.number_of_nodes() == n)
    assert(graph_obj.number_of_edges() == e)

    return graph_obj


def approx_vertex_cover(graph_obj, random_selection=False):
    """Calculate a vertex cover for the graph using an approximation algorithm.

    Note: This function utilizes objects from the networkx package.
    Ref: Introduction to Algorithms 3rd. Ed. pg. 1108-1111

    :param graph_obj: Graph object (networkx).
    :return: Approximate vertex cover for the given graph.
    """

    cover = []
    edges = graph_obj.edges()

    while len(edges) > 0:

        # Choose edge in list of edges
        if random_selection:
            uv = edges[random.randint(0, len(edges) - 1)]
        else:
            uv = edges[0]

        # Add nodes to the VC
        cover.append(uv[0])
        cover.append(uv[1])

        # Remove any edges touching the currently chosen nodes.
        edges[:] = [e for e in edges if not (uv[0] in e or uv[1] in e)]

    return cover


def monticarlo_approximation(graph_obj, runs=100):
    results = np.zeros(runs)
    for i in range(0, runs):
        approx_cover = approx_vertex_cover(graph_obj, random_selection=True)
        results[i] = len(approx_cover)
    return results


if __name__ == "__main__":
    """Run the script."""

    # Read the graph text file.
    graph = read_graph_file("rmat0406.gr")

    # Create the approximate vertex cover.
    approx_vc = approx_vertex_cover(graph)

    # For now just print the result to the screen.
    print(approx_vc)
    print(len(approx_vc))

    res = monticarlo_approximation(graph, runs=1000)
    print(max(res))
    print(min(res))
