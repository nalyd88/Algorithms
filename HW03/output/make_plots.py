import numpy as np
import matplotlib.pyplot as plt


def make_plots():

    dc_1000 = np.loadtxt('dcrocker3_output_dc_1000.txt', delimiter=',')
    dc_2000 = np.loadtxt('dcrocker3_output_dc_2000.txt', delimiter=',')
    dc_3000 = np.loadtxt('dcrocker3_output_dc_3000.txt', delimiter=',')
    dc_4000 = np.loadtxt('dcrocker3_output_dc_4000.txt', delimiter=',')
    dc_5000 = np.loadtxt('dcrocker3_output_dc_5000.txt', delimiter=',')
    dc_6000 = np.loadtxt('dcrocker3_output_dc_6000.txt', delimiter=',')
    dc_7000 = np.loadtxt('dcrocker3_output_dc_7000.txt', delimiter=',')
    dc_8000 = np.loadtxt('dcrocker3_output_dc_8000.txt', delimiter=',')
    dc_9000 = np.loadtxt('dcrocker3_output_dc_9000.txt', delimiter=',')
    dc_10000 = np.loadtxt('dcrocker3_output_dc_10000.txt', delimiter=',')

    dc_time = [np.average(dc_1000[:, 3]), np.average(dc_2000[:, 3]), np.average(dc_3000[:, 3]),
               np.average(dc_4000[:, 3]), np.average(dc_5000[:, 3]), np.average(dc_6000[:, 3]),
               np.average(dc_7000[:, 3]), np.average(dc_8000[:, 3]), np.average(dc_9000[:, 3]),
               np.average(dc_10000[:, 3])]

    dp_1000 = np.loadtxt('dcrocker3_output_dp_1000.txt', delimiter=',')
    dp_2000 = np.loadtxt('dcrocker3_output_dp_2000.txt', delimiter=',')
    dp_3000 = np.loadtxt('dcrocker3_output_dp_3000.txt', delimiter=',')
    dp_4000 = np.loadtxt('dcrocker3_output_dp_4000.txt', delimiter=',')
    dp_5000 = np.loadtxt('dcrocker3_output_dp_5000.txt', delimiter=',')
    dp_6000 = np.loadtxt('dcrocker3_output_dp_6000.txt', delimiter=',')
    dp_7000 = np.loadtxt('dcrocker3_output_dp_7000.txt', delimiter=',')
    dp_8000 = np.loadtxt('dcrocker3_output_dp_8000.txt', delimiter=',')
    dp_9000 = np.loadtxt('dcrocker3_output_dp_9000.txt', delimiter=',')
    dp_10000 = np.loadtxt('dcrocker3_output_dp_10000.txt', delimiter=',')

    dp_time = [np.average(dp_1000[:, 3]), np.average(dp_2000[:, 3]), np.average(dp_3000[:, 3]),
               np.average(dp_4000[:, 3]), np.average(dp_5000[:, 3]), np.average(dp_6000[:, 3]),
               np.average(dp_7000[:, 3]), np.average(dp_8000[:, 3]), np.average(dp_9000[:, 3]),
               np.average(dp_10000[:, 3])]

    data_sizes = np.array([1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000])

    plt.figure(1)
    line1 = plt.plot(data_sizes, dc_time, "r-", label="Divide and Conquer")
    line2 = plt.plot(data_sizes, dp_time, "b--", label="Dynamic Programming")
    plt.legend(handles=[line1[0], line2[0]], loc=2)
    plt.title("HW #3 Run Times")
    plt.ylabel("Run Time (ms)")
    plt.xlabel("Data Set Size")
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    make_plots()
