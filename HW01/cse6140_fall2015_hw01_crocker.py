#!/usr/bin/python
#  CSE6140 HW1
#  Dylan Crocker
#  Submitted 9/21/2014

import networkx as nx
import bisect
import timeit
import sys
import os


class RunExperiments:

    def __init__(self):
        self.graph = nx.MultiGraph()
        self.sorted_edges = []
        self.sorted_edge_weights = []

    def read_graph_file(self, file_path, stats=False):
        """Read the given graph file and return a graph object.

        Note: This function utilizes objects from the networkx package.

        :param file_path: Path to the graph text file.
        :return: Graph object (networkx) filled with the graph file contents.
        """

        graph_obj = nx.MultiGraph()

        # Read and parse the graph text file.
        with open(file_path, 'r') as graph_file:

            # Read the header and get the number of nodes and edges.
            header = [int(x) for x in graph_file.readline().split()]
            n, e = header[0], header[1]

            for line in graph_file:
                edge_data = list(map(lambda x: int(x), line.split()))
                assert(len(edge_data) == 3)
                u, v, w = edge_data[0], edge_data[1], edge_data[2]
                graph_obj.add_edge(u, v, weight=w)  # Adding edges will also add the nodes to the graph.

        # Ensure there are no errors with the file.
        assert(graph_obj.number_of_nodes() == n)
        assert(graph_obj.number_of_edges() == e)

        if stats:
            # Print graph statistics.
            print("File = " + file_path)
            print("Nodes = " + str(n))
            print("Edges = " + str(e))

        self.graph = graph_obj

    def compute_mst_networkx(self):
        """ Calculate the weight of the MST for the given graph using Networkx functions (for comparison)."""
        return sum([e[2]['weight'] for e in list(nx.minimum_spanning_edges(self.graph, data=True))])

    def compute_mst(self):
        """Computes the Minimum Spanning Tree (MST) of the given graph object.

        This function implements Kruskal's algorithm. The function utilizes functionality from the Networkx library.

        :param graph: Graph object (networkx) filled with the graph file contents.
        :return: The weight of the MST.
        """

        # Get a sorted list of edges.
        self.sorted_edges = sorted(self.graph.edges(data=True), key=lambda edge: edge[2]['weight'])

        mst_weight = 0             # Keep track of the weight
        uf = nx.utils.UnionFind()  # Utilize Networkx's UnionFind structure.

        # Create the MST using the shortest possible edges.
        for u, v, d in self.sorted_edges:
            if uf[u] != uf[v]:
                uf.union(u, v)
                mst_weight += d['weight']

        # Verify the result here match the networkx implementation.
        # print(mst_weight)
        # print(compute_mst_networkx(self.graph))

        return mst_weight

    def recompute_mst_networkx(self, u, v, weight):
        self.graph.add_edge(u, v, weight=weight)
        return self.compute_mst_networkx()

    def recompute_mst(self, u, v, weight):
        """Recompute the MST given the new edge to add to the graph."""

        # Add the edge to the graph object (not really necessary).
        #self.graph.add_edge(u, v, weight=weight)

        # The edges are already sorted so we can insert the edge into the correct location without re-sorting.
        self.sorted_edges.insert(bisect.bisect_left(self.sorted_edge_weights, weight), (u, v, {'weight': weight}))
        bisect.insort_left(self.sorted_edge_weights, weight)

        mst_weight = 0             # Keep track of the weight
        uf = nx.utils.UnionFind()  # Utilize Networkx's UnionFind structure.

        # Create the MST using the shortest possible edges.
        for u, v, d in self.sorted_edges:
            if uf[u] != uf[v]:
                uf.union(u, v)
                mst_weight += d['weight']

        return mst_weight

    def main(self):
        """Run the experiment."""

        if len(sys.argv) < 4:
            print("Usage: " + sys.argv[0] + " <graph_file> <change_file> <output_file>")
            exit(1)

        # Access the input arguments
        graph_file = sys.argv[1]
        change_file = sys.argv[2]
        output_file = sys.argv[3]

        # Construct graph
        self.read_graph_file(graph_file, stats=True)

        # Calculate the MST and get its weight.
        start_mst = timeit.default_timer()                        # Get the current time in seconds.
        mst_weight = self.compute_mst()                           # Create the MST and get the total weight of the MST.
        total_time = (timeit.default_timer() - start_mst) * 1000  # Calculate the run time and convert to milliseconds.

        # Write initial MST weight and running time to file.
        if not os.path.exists(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file))
        output = open(output_file, 'w')
        output.write(str(mst_weight) + " " + str(total_time) + "\n")
        # Leave the file open so that the dynamic recalculation results can be added.

        # Get a lis of edge weights to be used as keys for the sorted list of edges.
        self.sorted_edge_weights = [edge[2]['weight'] for edge in self.sorted_edges]

        # Open the changes file and process new edges.
        with open(change_file, 'r') as changes:
            num_changes = changes.readline()

            for line in changes:
                # parse edge and weight
                edge_data = list(map(lambda x: int(x), line.split()))
                assert(len(edge_data) == 3)
                u, v, weight = edge_data[0], edge_data[1], edge_data[2]

                # call recomputeMST function
                start_recompute = timeit.default_timer()
                new_weight = self.recompute_mst(u, v, weight)
                total_recompute = (timeit.default_timer() - start_recompute) * 1000  # to convert to milliseconds

                # write new weight and time to output file
                output.write(str(new_weight) + " " + str(total_recompute) + "\n")


if __name__ == '__main__':
    # Run the code
    runexp = RunExperiments()
    runexp.main()
    print("Experiment Complete")
