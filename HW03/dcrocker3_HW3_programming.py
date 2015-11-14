#!/usr/bin/python
#  CSE6140 HW3
#  Dylan Crocker
#  Submitted 11/09/2015
#

import sys
import argparse
import numpy as np
import timeit


def parse_args(argv):
    """Use the argparse module to define input arguments and a help message for incorrect use.

    :param argv: Input arguments provided by the system
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Calculate the optimal investment period.")

    parser.add_argument("infile",
                        type=argparse.FileType('r'),
                        action="store",
                        help="Path to the input file containing the interest rate data.")

    parser.add_argument("method",
                        type=str,
                        action="store",
                        help="The algorithm to use (dc = Divide and Conquer; dp = Dynamic Programming).",
                        choices=["dc", "dp"])

    return parser.parse_args(argv)


class DataFile(object):
    """Define a simple object to encapsulate the data read form the file."""

    def __init__(self, file_path):
        self.data = np.loadtxt(file_path, skiprows=1, delimiter=',')
        dims = np.shape(self.data)
        self.n = dims[1]
        self.k = dims[0]


class Results(object):
    """A simple object for handling the calculation results."""

    def __init__(self):
        self.max_rates = []
        self.intervals = []
        self.run_times = []


def calculate_optimal_investment_period(data, method="dp"):
    results_obj = Results()

    if method == "dc":
        # Divide and conquer method
        for k in range(0, data.k):
            start_mst = timeit.default_timer()
            max_info = divide_conquer_rec(data.data[k], data.n)
            results_obj.run_times.append((timeit.default_timer() - start_mst) * 1000)
            results_obj.intervals.append((max_info.i, max_info.j))
            results_obj.max_rates.append(max_info.sum)
    else:
        # Dynamic programming method
        for k in range(0, data.k):
            start_mst = timeit.default_timer()
            max_info = dynamic_programming_bottom_up(data.data[k], data.n)
            results_obj.run_times.append((timeit.default_timer() - start_mst) * 1000)
            results_obj.intervals.append((max_info.i, max_info.j))
            results_obj.max_rates.append(max_info.sum)

    return results_obj


def write_results_file(file_name, results):
    with open(file_name, 'w') as outfile:
        for i, t in enumerate(results.run_times):
            outfile.write("{},{},{},{}\n".format(
                results.max_rates[i], results.intervals[i][0] + 1, results.intervals[i][1] + 1, t)
            )


####################################################################################################
# Divide and Conquer
####################################################################################################


class Interval:
    def __init__(self, i, j, s):
        self.i = i
        self.j = j
        self.sum = s

    def increment(self, x):
        self.i += x
        self.j += x

    def __str__(self):
        """Used for debugging."""
        return "{} {} {}".format(self.i, self.j, self.sum)


def linear_search(rates, n):
    """Perform a search for the maximum sum interval with the start in the first half of the rates
    list and the end in the second half. Runs in O(n) time.

    :param rates: List of interest rates.
    :param n: Length of the rates list (must be >= 2).
    :return: An interval object containing the start and stop indexes and the corresponding sum.
    """

    if n < 2:
        return None

    if n < 3:
        return Interval(0, 1, rates[0] + rates[1])

    # Split the list.
    half = int(np.floor(n/2))

    tot_max_sum = 0
    max_indexes = np.zeros(2, dtype=int)
    for k in range(0, 2):  # Look at the left and right sides.
        if k == 1:
            idx_step = 1
            idx_start = half
            half_size = n - half
        else:
            idx_step = -1
            idx_start = half - 1
            half_size = half

        max_idx = idx_start
        cur_sum = rates[idx_start]
        max_sum = cur_sum

        idx = idx_start
        for count in range(1, half_size):
            idx += idx_step
            cur_sum += rates[idx]
            if cur_sum > max_sum:
                max_idx = idx
                max_sum = cur_sum

        # Save the results of the half being evaluated.
        max_indexes[k] = max_idx
        tot_max_sum += max_sum

    # Return an interval object.
    return Interval(max_indexes[0], max_indexes[1], tot_max_sum)


def divide_conquer_rec(rates, n):
    if n == 1:
        return Interval(0, 0, rates[0])

    # Find the midpoint of the list of rates (Note: Python arrays are zero indexed!).
    half = int(np.floor(n/2))

    # Determine the max interval in each half recursively.
    x = divide_conquer_rec(rates[:half], half)
    y = divide_conquer_rec(rates[half:], n-half)
    y.increment(half)  # Adjust the indexes

    # Perform a linear search for the max that starts in the first half and ends in the second half.
    z = linear_search(rates, n)

    # Determine which result is the best and return that.
    m = np.argmax([x.sum, y.sum, z.sum])
    if m == 0:
        return x
    if m == 1:
        return y
    return z


####################################################################################################
# Dynamic Programing
####################################################################################################


def dynamic_programming_bottom_up(rates, n):
    """Solve the max interval using a dynamic programming bottom up approach.

    Implements the given recurrence relation:
    B(j) = 0,                    j == 0
           max(B(j-1) + aj, 0),  j != 0

    :param rates: List of interest rates.
    :param n: Length of the rates list (must be >= 1).
    :return: An interval object containing the start and stop indexes and the corresponding sum.
    """

    if n < 1:
        return None  # Invalid size

    b_j = np.zeros(n)  # Store the B(j) values.
    b_i = 0            # Keep track of the i index...
    max_info = {"sum": 0, "i": 0, "j": 0}
    for i in range(0, n):
        if i == 0:
            b_j[i] = max(rates[0], 0)
        else:
            b_j[i] = max(b_j[i-1] + rates[i], 0)
            # When the value changes from 0 a new section is started. Save the starting index.
            if b_j[i-1] == 0 and b_j[i] != 0:
                b_i = i
        # Save the best parameters found as we go in order to save time.
        if b_j[i] > max_info["sum"]:
            max_info["sum"] = b_j[i]
            max_info["i"] = b_i
            max_info["j"] = i

    return Interval(max_info["i"], max_info["j"], max_info["sum"])


####################################################################################################


if __name__ == "__main__":

    # Parse the input arguments (display error if necessary)
    args = parse_args(sys.argv[1:])

    # Parse the contents into a DataFile object
    data_obj = DataFile(args.infile.name)

    # Perform the analysis
    results_data = calculate_optimal_investment_period(data_obj, method=args.method)

    # Save the data to the results file
    outfile_name = '_'.join(["dcrocker3_output", args.method, str(data_obj.n)]) + ".txt"
    write_results_file("output\\" + outfile_name, results_data)
